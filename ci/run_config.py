#!/usr/bin/env python3
"""Build, measure, and re-measure the usb_ethernet example for one configuration.

Usage:
    python ci/run_config.py <config-name> --out <results-dir> \
        --channel nightly-YYYY-MM-DD [--work <scratch-dir>]

The steps, in order, per the task spec:

  1. Clone the embassy fork at the configured ref, init the xarxa + flux
     submodules, and (if the config names a concrete xarxa ref) check that ref
     out into third_party/xarxa. The example is built exactly where it lives in
     the fork -- no source is modified.
  2. Record environment + provenance verbatim (rustc, rust-toolchain.toml,
     target triple from .cargo/config.toml, tool versions, resolved SHAs and
     merge-bases against upstream for every dependency repo).
  3. cargo tree; confirm xarxa resolves to a path dependency, not crates.io.
     If it resolves to a registry version, fail.
  4. Build (pass 1, verbose) -> measure. cargo clean. Build (pass 2) -> measure.
     Assert .text size and panic-site count are identical across the two passes.
  5. For configs that demand it (immediate-abort), verify the panic formatting
     symbols are absent; if present, fail rather than record the number.
  6. Emit <out>/<config>/{results.json,disasm.txt,cargo-tree.txt,build.log}.

Every recorded number comes from this run. There are no baked-in expectations.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import measure


REPO_ROOT = Path(__file__).resolve().parent.parent


class StepError(RuntimeError):
    """Raised when a step is blocked. Carries the failing command + output so
    the caller can fail loudly and verbatim."""


def run(
    cmd: List[str],
    cwd: Optional[Path] = None,
    env: Optional[dict] = None,
    log: Optional[List[str]] = None,
    check: bool = True,
) -> subprocess.CompletedProcess:
    printable = " ".join(shlex.quote(c) for c in cmd)
    proc = subprocess.run(
        cmd, cwd=cwd, env=env, capture_output=True, text=True
    )
    if log is not None:
        log.append(f"$ {printable}\n{proc.stdout}{proc.stderr}")
    if check and proc.returncode != 0:
        raise StepError(
            f"command failed (exit {proc.returncode}):\n"
            f"  {printable}\n"
            f"--- stdout ---\n{proc.stdout}\n"
            f"--- stderr ---\n{proc.stderr}"
        )
    return proc


def out(cmd: List[str], cwd: Optional[Path] = None) -> str:
    return run(cmd, cwd=cwd).stdout.strip()


# --- config -------------------------------------------------------------------

def load_configs() -> dict:
    with open(REPO_ROOT / "configs.toml", "rb") as fh:
        return tomllib.load(fh)


def read_target_triple(example_dir: Path) -> Tuple[str, str]:
    """Read the target triple from the example's .cargo/config.toml. Never
    guess or override it."""
    cfg_path = example_dir / ".cargo" / "config.toml"
    with open(cfg_path, "rb") as fh:
        cfg = tomllib.load(fh)
    triple = cfg.get("build", {}).get("target")
    if not triple:
        raise StepError(f"no [build] target in {cfg_path}")
    rel = cfg_path.relative_to(example_dir.parent.parent) \
        if example_dir.parent.parent in cfg_path.parents else cfg_path
    return triple, str(rel)


# --- toolchain / tools --------------------------------------------------------

def toolchain_paths(channel: str) -> Dict[str, str]:
    sysroot = out(["rustc", f"+{channel}", "--print", "sysroot"])
    host = None
    for line in out(["rustc", f"+{channel}", "-vV"]).splitlines():
        if line.startswith("host:"):
            host = line.split(":", 1)[1].strip()
    if host is None:
        raise StepError("could not determine host triple from rustc -vV")
    bindir = Path(sysroot) / "lib" / "rustlib" / host / "bin"
    tools = {
        "size": bindir / "llvm-size",
        "objdump": bindir / "llvm-objdump",
        "nm": bindir / "llvm-nm",
    }
    for name, p in tools.items():
        if not p.exists():
            raise StepError(
                f"pinned {name} tool missing at {p}; is the llvm-tools "
                f"component installed for {channel}?"
            )
    return {k: str(v) for k, v in tools.items()}


def tool_versions(tools: Dict[str, str]) -> Dict[str, dict]:
    info = {}
    for name, path in tools.items():
        ver = subprocess.run(
            [path, "--version"], capture_output=True, text=True
        ).stdout.strip()
        info[name] = {"path": path, "version": ver}
    return info


# --- repo setup ---------------------------------------------------------------

def setup_repo(cfg: dict, work: Path, log: List[str]) -> Path:
    embassy = work / "embassy"
    if embassy.exists():
        run(["rm", "-rf", str(embassy)])
    run(
        ["git", "clone", "--branch", cfg["embassy_ref"],
         cfg["embassy_repo"], str(embassy)],
        log=log,
    )
    run(
        ["git", "submodule", "update", "--init",
         "third_party/xarxa", "third_party/flux"],
        cwd=embassy, log=log,
    )

    xarxa_dir = embassy / "third_party" / "xarxa"
    if cfg["xarxa_ref"] != "@submodule":
        # Override the submodule pin with a concrete ref from the xarxa repo.
        run(["git", "fetch", cfg["xarxa_repo"], cfg["xarxa_ref"]],
            cwd=xarxa_dir, log=log)
        run(["git", "checkout", "FETCH_HEAD"], cwd=xarxa_dir, log=log)
    return embassy


def merge_base_provenance(
    repo_dir: Path, ref: str, upstream_repo: str, upstream_ref: str,
    log: List[str],
) -> dict:
    resolved = out(["git", "rev-parse", "HEAD"], cwd=repo_dir)
    prov = {
        "repo_dir": str(repo_dir),
        "ref": ref,
        "resolved_sha": resolved,
        "upstream_repo": upstream_repo,
        "upstream_ref": upstream_ref,
    }
    try:
        run(["git", "fetch", "--depth", "200", upstream_repo, upstream_ref],
            cwd=repo_dir, log=log)
        mb = subprocess.run(
            ["git", "merge-base", resolved, "FETCH_HEAD"],
            cwd=repo_dir, capture_output=True, text=True,
        )
        if mb.returncode == 0:
            prov["merge_base"] = mb.stdout.strip()
        else:
            # Shallow history may not reach the merge-base; retry unshallowed.
            run(["git", "fetch", "--unshallow", upstream_repo, upstream_ref],
                cwd=repo_dir, log=log, check=False)
            run(["git", "fetch", upstream_repo, upstream_ref],
                cwd=repo_dir, log=log, check=False)
            mb = subprocess.run(
                ["git", "merge-base", resolved, "FETCH_HEAD"],
                cwd=repo_dir, capture_output=True, text=True,
            )
            prov["merge_base"] = (
                mb.stdout.strip() if mb.returncode == 0
                else f"UNRESOLVED: {mb.stderr.strip()}"
            )
    except StepError as exc:
        prov["merge_base"] = f"UNRESOLVED: {exc}"
    return prov


def gather_provenance(
    cfg: dict, upstreams: dict, embassy: Path, log: List[str],
) -> dict:
    def up(fork_repo: str) -> Tuple[str, str]:
        key = fork_repo.rstrip("/").removeprefix("https://github.com/")
        entry = upstreams[key]
        return entry["repo"], entry["ref"]

    xarxa_dir = embassy / "third_party" / "xarxa"
    flux_dir = embassy / "third_party" / "flux"

    emb_up, emb_up_ref = up(cfg["embassy_repo"])
    xar_up, xar_up_ref = up(cfg["xarxa_repo"])
    flux_up, flux_up_ref = up("https://github.com/ninehusky/flux")

    xarxa_ref_display = (
        cfg["xarxa_ref"] if cfg["xarxa_ref"] != "@submodule"
        else "@submodule (embassy fork pin)"
    )

    return {
        "embassy": merge_base_provenance(
            embassy, cfg["embassy_ref"], emb_up, emb_up_ref, log),
        "xarxa": merge_base_provenance(
            xarxa_dir, xarxa_ref_display, xar_up, xar_up_ref, log),
        "flux": merge_base_provenance(
            flux_dir, "@submodule (embassy fork pin)",
            flux_up, flux_up_ref, log),
    }


# --- build --------------------------------------------------------------------

def build_command(cfg: dict, channel: str, bin_name: str,
                  verbose: bool) -> List[str]:
    cmd = ["cargo", f"+{channel}", "build", "--release", "--bin", bin_name]
    cmd += list(cfg.get("cargo_flags", []))
    if cfg.get("build_std"):
        cmd += ["-Z", "build-std=" + ",".join(cfg["build_std"])]
    if cfg.get("build_std_features"):
        cmd += ["-Z", "build-std-features=" + ",".join(cfg["build_std_features"])]
    if verbose:
        cmd += ["-v"]
    return cmd


def build_env(cfg: dict) -> dict:
    env = os.environ.copy()
    rustflags = " ".join(cfg.get("rustflags", []))
    if rustflags:
        env["RUSTFLAGS"] = rustflags
    for key, val in cfg.get("profile_overrides", {}).items():
        env_key = "CARGO_PROFILE_RELEASE_" + key.upper().replace("-", "_")
        env[env_key] = str(val)
    return env


_C_FLAG_RE = re.compile(r"-C\s*([a-z0-9_-]+(=\S+)?)")


def extract_bin_rustc_flags(verbose_log: str, bin_name: str) -> List[str]:
    """Pull the -C flags from the final bin-crate rustc invocation -- the
    ground truth of what the crate was compiled with."""
    for line in verbose_log.splitlines():
        if f"--crate-name {bin_name}" in line and "--crate-type bin" in line:
            return sorted(set("-C " + m.group(1) for m in _C_FLAG_RE.finditer(line)))
    return []


def effective_profile(
    bin_flags: List[str], target_panic_strategy: str,
) -> Dict[str, dict]:
    """Resolve the effective release-profile values. Fields explicitly emitted
    by cargo/rustc are marked ``emitted``; the rest fall back to documented
    defaults (with the source recorded), never left as "unset"."""
    flat = {}
    for f in bin_flags:
        body = f[len("-C "):]
        if "=" in body:
            k, v = body.split("=", 1)
            flat[k] = v
        else:
            flat[k] = True

    def field(name: str, default, default_source: str):
        if name in flat:
            return {"value": str(flat[name]), "source": "emitted"}
        return {"value": str(default), "source": default_source}

    # Cargo `release` profile defaults (documented, stable):
    #   opt-level=3, debug=0, debug-assertions=false, overflow-checks=false,
    #   lto=false, codegen-units=16, strip=none, panic=<unwind, but the target
    #   spec's panic-strategy governs when cargo does not pass -C panic>.
    return {
        "opt-level": field("opt-level", 3, "cargo-release-default"),
        "lto": field("lto", "false", "cargo-release-default"),
        "codegen-units": field("codegen-units", 16, "cargo-release-default"),
        "panic": field("panic", target_panic_strategy, "target-spec-default"),
        "debug-assertions": field(
            "debug-assertions", "false", "cargo-release-default"),
        "overflow-checks": field(
            "overflow-checks", "false", "cargo-release-default"),
        "strip": field("strip", "none", "cargo-release-default"),
        "debug": field("debuginfo", 0, "cargo-release-default"),
    }


def target_panic_strategy(channel: str, triple: str) -> str:
    spec = out([
        "rustc", f"+{channel}", "--print", "target-spec-json",
        "-Z", "unstable-options", "--target", triple,
    ])
    return json.loads(spec).get("panic-strategy", "unwind")


# --- dependency graph ---------------------------------------------------------

def cargo_tree(cfg: dict, channel: str, example_dir: Path,
               log: List[str]) -> Tuple[str, dict]:
    env = build_env(cfg)
    proc = run(["cargo", f"+{channel}", "tree"], cwd=example_dir,
               env=env, log=log)
    tree = proc.stdout

    xarxa_lines = [ln for ln in tree.splitlines()
                   if re.search(r"\bxarxa v", ln)]
    # A path dep prints "xarxa vX.Y.Z (/abs/path...)"; a registry dep would not
    # carry a filesystem path (it would be bare or "(registry+...)").
    path_lines = [ln for ln in xarxa_lines if "third_party/xarxa" in ln]
    is_path = bool(path_lines)
    resolution = "NOT FOUND"
    if xarxa_lines:
        m = re.search(r"xarxa v\S+\s+\(([^)]+)\)", xarxa_lines[0])
        resolution = m.group(1) if m else xarxa_lines[0].strip()
    graph = {
        "xarxa_lines": [ln.strip() for ln in xarxa_lines],
        "xarxa_resolution": resolution,
        "xarxa_is_path_dep": is_path,
    }
    if not is_path:
        raise StepError(
            "xarxa did not resolve to the third_party/xarxa path dependency "
            f"(refusing to add a patch section). cargo tree said:\n"
            + "\n".join(xarxa_lines or ["<no xarxa node>"])
        )
    return tree, graph


# --- measurement pass ---------------------------------------------------------

def measure_pass(tools: Dict[str, str], binary: Path) -> dict:
    m = measure.measure_binary(
        str(binary), tools["size"], tools["objdump"], tools["nm"])
    disasm = m.pop("_disasm")
    return m, disasm


def do_config(name: str, channel: str, work: Path, out_dir: Path) -> dict:
    conf = load_configs()
    upstreams = conf["upstreams"]
    example_rel = conf["example"]["path"]
    bin_name = conf["example"]["bin"]
    if name not in conf["configs"]:
        raise StepError(f"unknown config '{name}'")
    cfg = conf["configs"][name]

    log: List[str] = []
    cfg_out = out_dir / name
    cfg_out.mkdir(parents=True, exist_ok=True)

    tools = toolchain_paths(channel)

    # 1. repo
    embassy = setup_repo(cfg, work, log)
    example_dir = embassy / example_rel

    triple, triple_src = read_target_triple(example_dir)
    binary = example_dir / "target" / triple / "release" / bin_name

    # Provision exactly the target the example declares -- read, never guessed.
    run(["rustup", "target", "add", triple, "--toolchain", channel], log=log)

    # 2. provenance / environment
    rustc_verbose = out(["rustc", f"+{channel}", "--version", "--verbose"])
    toolchain_toml = (embassy / "rust-toolchain.toml").read_text()
    panic_strategy = target_panic_strategy(channel, triple)
    provenance = gather_provenance(cfg, upstreams, embassy, log)

    environment = {
        "runner_image": os.environ.get("RUNNER_IMAGE_LABEL", "unknown"),
        "github_runner_os": os.environ.get("ImageOS", "unknown"),
        "rustc_version_verbose": rustc_verbose,
        "rust_toolchain_toml_path": "rust-toolchain.toml (embassy fork)",
        "rust_toolchain_toml": toolchain_toml,
        "target_triple": triple,
        "target_triple_source": triple_src,
        "target_panic_strategy": panic_strategy,
        "tools": tool_versions(tools),
    }

    # 3. dependency graph
    tree, graph = cargo_tree(cfg, channel, example_dir, log)
    (cfg_out / "cargo-tree.txt").write_text(tree)

    env = build_env(cfg)

    # 4. pass 1 (verbose)
    log.append("\n===== BUILD PASS 1 =====\n")
    p1 = run(build_command(cfg, channel, bin_name, verbose=True),
             cwd=example_dir, env=env, log=log)
    if not binary.exists():
        raise StepError(f"pass 1 produced no binary at {binary}")
    bin_flags = extract_bin_rustc_flags(p1.stdout + p1.stderr, bin_name)
    eff_profile = effective_profile(bin_flags, panic_strategy)
    m1, disasm1 = measure_pass(tools, binary)
    (cfg_out / "disasm.txt").write_text(disasm1)

    # 4b. clean + pass 2
    log.append("\n===== CARGO CLEAN =====\n")
    run(["cargo", f"+{channel}", "clean"], cwd=example_dir, env=env, log=log)
    log.append("\n===== BUILD PASS 2 =====\n")
    run(build_command(cfg, channel, bin_name, verbose=False),
        cwd=example_dir, env=env, log=log)
    if not binary.exists():
        raise StepError(f"pass 2 produced no binary at {binary}")
    m2, _ = measure_pass(tools, binary)

    # determinism
    t1 = m1["sizes"][".text"]
    t2 = m2["sizes"][".text"]
    ps1 = m1["panic_sites"]["branch_call_sites_total"]
    ps2 = m2["panic_sites"]["branch_call_sites_total"]
    determinism = {
        "text_size_pass1": t1,
        "text_size_pass2": t2,
        "text_size_match": t1 == t2,
        "panic_sites_pass1": ps1,
        "panic_sites_pass2": ps2,
        "panic_sites_match": ps1 == ps2,
    }

    # 5. immediate-abort symbol-absence verification
    verification = {"required": bool(cfg.get("verify_panic_symbols_absent", False))}
    if verification["required"]:
        present = m1["panic_fmt_check"]["present"] or m2["panic_fmt_check"]["present"]
        verification["panic_fmt_absent"] = not present
        verification["detail"] = m1["panic_fmt_check"]

    result = {
        "config": name,
        "description": cfg.get("description", ""),
        "enabled": cfg.get("enabled", False),
        "generated_by": "ci/run_config.py",
        "environment": environment,
        "provenance": provenance,
        "build": {
            "cargo_flags": list(cfg.get("cargo_flags", [])),
            "build_std": list(cfg.get("build_std", [])),
            "build_std_features": list(cfg.get("build_std_features", [])),
            "rustflags": " ".join(cfg.get("rustflags", [])),
            "profile_overrides": dict(cfg.get("profile_overrides", {})),
            "build_command_pass2": " ".join(
                build_command(cfg, channel, bin_name, verbose=False)),
            "bin_crate_rustc_flags": bin_flags,
        },
        "effective_profile": eff_profile,
        "dependency_graph": {
            "cargo_tree_file": "cargo-tree.txt",
            **graph,
        },
        "passes": [
            {"pass": 1, **m1},
            {"pass": 2, **m2},
        ],
        "determinism": determinism,
        "verification": verification,
    }

    (cfg_out / "results.json").write_text(json.dumps(result, indent=2))
    (cfg_out / "build.log").write_text("\n".join(log))

    # Fail loudly on the hard success conditions.
    failures = []
    if not determinism["text_size_match"]:
        failures.append(
            f".text size differs between passes: {t1} vs {t2}")
    if not determinism["panic_sites_match"]:
        failures.append(
            f"panic-site count differs between passes: {ps1} vs {ps2}")
    if verification["required"] and not verification.get("panic_fmt_absent"):
        failures.append(
            "immediate-abort did not remove panic formatting symbols: "
            f"{m1['panic_fmt_check']}")
    if failures:
        raise StepError(
            "measurement invariants violated for config "
            f"'{name}':\n  - " + "\n  - ".join(failures))

    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--out", required=True, help="output root dir")
    ap.add_argument("--channel", required=True, help="pinned toolchain channel")
    ap.add_argument("--work", default="_work", help="scratch clone dir")
    args = ap.parse_args()

    work = Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    out_dir = Path(args.out).resolve()

    try:
        do_config(args.config, args.channel, work, out_dir)
    except StepError as exc:
        print(f"::error::[{args.config}] {exc}", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1
    print(f"[{args.config}] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
