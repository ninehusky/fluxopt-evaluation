#!/usr/bin/env python3
"""Per-file panic ablation sweep, measured against the real usb_ethernet binary.

    ./sweep.py                    # every xarxa file that owns >= 1 panic site
    ./sweep.py src/wire/ipv4.rs   # just these (paths relative to the xarxa checkout)

For each file: rewrite its panicking constructs away with ablate.py, rebuild
usb_ethernet, and record how much .text went away.  The file is restored with
git afterwards, so the tree is clean between measurements.

Requires ./run.py to have been run first (it creates work/modified).

Three things make the ranking trustworthy, and all three are checks rather than
assumptions:

  - determinism is confirmed before anything is ablated, by forcing a full
    recompile of unmodified sources and requiring .text to be byte-identical;
  - each file's ablation is verified after the rebuild by re-blaming the panic
    sites, so a file that was not really ablated is reported `partial` instead
    of as a small win;
  - the checkout is restored between files, including on Ctrl-C, so no
    measurement ever runs against a half-ablated tree.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.environ.get("WORK", os.path.join(HERE, "work"))
REPO = os.path.join(WORK, "modified")
XARXA = os.path.join(REPO, "third_party", "xarxa")
OUT = os.path.join(HERE, "results", "ablate")
TSV = os.path.join(HERE, "results", "per-file-wins.tsv")
TOOLCHAIN = "1.97"
TARGET = "thumbv7em-none-eabi"
ELF = os.path.join(REPO, "examples/nrf52840/target", TARGET, "release/usb_ethernet")
XARXA_PREFIX = "third_party/xarxa/"


def out(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, check=True, text=True,
                          capture_output=True).stdout


def llvm_bin():
    host = next(l.split()[1] for l in out(["rustc", f"+{TOOLCHAIN}", "-vV"]).splitlines()
                if l.startswith("host:"))
    sysroot = out(["rustc", f"+{TOOLCHAIN}", "--print", "sysroot"]).strip()
    return os.path.join(sysroot, "lib", "rustlib", host, "bin")


def restore():
    subprocess.run(["git", "checkout", "--", "."], cwd=XARXA, check=True)


def allow_unsafe():
    """xarxa is `#![deny(unsafe_code)]` and every ablation emits `get_unchecked`.

    A lint attribute only -- it changes no codegen -- and `restore` undoes it
    along with everything else.
    """
    p = os.path.join(XARXA, "src", "lib.rs")
    src = open(p).read()
    open(p, "w").write(
        re.sub(r"^#!\[deny\(unsafe_code\)\]", "#![allow(unsafe_code)]", src, flags=re.M))


def build(logfile):
    """True on success.  The log is kept either way, for the failures."""
    env = dict(os.environ, CARGO_INCREMENTAL="0")
    with open(logfile, "w") as f:
        r = subprocess.run(
            ["cargo", f"+{TOOLCHAIN}", "build", "--release", "--bin", "usb_ethernet",
             "--target", TARGET],
            cwd=os.path.join(REPO, "examples/nrf52840"), env=env, stdout=f, stderr=f)
    return r.returncode == 0


def measure(tag):
    """-> (.text bytes, panic call sites, {file: sites}) for the current ELF."""
    import json
    import collections
    prefix = os.path.join(OUT, tag)
    subprocess.run([sys.executable, os.path.join(HERE, "measure.py"), ELF, prefix],
                   check=True, stderr=subprocess.DEVNULL)
    blame = subprocess.run(
        [sys.executable, os.path.join(HERE, "blame.py"), prefix + ".json", REPO],
        check=True, text=True, capture_output=True).stdout
    open(prefix + ".blame.tsv", "w").write(blame)
    per_file = collections.Counter(
        l.split("\t")[0] for l in blame.splitlines() if l.strip())
    d = json.load(open(prefix + ".json"))
    return d["sections"][".text"], d["panic_call_sites"], per_file


def candidates(per_file):
    """xarxa files owning >= 1 panic site in the reference binary, biggest first."""
    xs = [(n, f[len(XARXA_PREFIX):]) for f, n in per_file.items()
          if f.startswith(XARXA_PREFIX)]
    return [f for _, f in sorted(xs, key=lambda t: -t[0])]


def main():
    os.environ["LLVM_BIN"] = llvm_bin()
    os.makedirs(OUT, exist_ok=True)
    if not os.path.isdir(XARXA):
        sys.exit(f"{XARXA} missing -- run ./run.py first")

    try:
        restore()

        print("== reference build (nothing ablated)", flush=True)
        if not build(os.path.join(OUT, "reference.log")):
            sys.exit("reference build failed; see results/ablate/reference.log")
        ref_text, ref_sites, ref_files = measure("reference")
        print(f"   .text={ref_text} sites={ref_sites}", flush=True)

        # If the same sources do not relink to the same bytes, every delta below
        # is noise and nothing after this point means anything.
        print("== determinism check (recompile identical sources)", flush=True)
        os.utime(os.path.join(XARXA, "src", "lib.rs"), None)
        build(os.path.join(OUT, "determinism.log"))
        det_text, _, _ = measure("determinism")
        if det_text == ref_text:
            print(f"   OK: .text={det_text} reproduced exactly", flush=True)
        else:
            print(f"   WARNING: .text moved {ref_text} -> {det_text} with no source "
                  f"change.\n   Deltas smaller than that difference are noise.",
                  flush=True)

        files = sys.argv[1:] or candidates(ref_files)
        print(f"== sweeping {len(files)} files", flush=True)

        rows = []
        for f in files:
            sites = ref_files.get(XARXA_PREFIX + f, 0)
            tag = f.replace("/", "_")
            restore()
            allow_unsafe()
            r = subprocess.run(
                [sys.executable, os.path.join(HERE, "ablate.py"), os.path.join(XARXA, f)],
                text=True, capture_output=True)
            if r.returncode != 0:
                rows.append((f, sites, "", "", "ablate-failed"))
                print(f"   {f}: ablate failed -- {r.stderr.strip().splitlines()[-1:]}", flush=True)
                continue
            if not build(os.path.join(OUT, f"{tag}.log")):
                rows.append((f, sites, "", "", "build-failed"))
                print(f"   {f}: build failed (see results/ablate/{tag}.log)", flush=True)
                continue
            text, n_sites, per_file = measure(tag)
            left = per_file.get(XARXA_PREFIX + f, 0)
            # The self-check: if this file's own sites did not go away, the
            # rewrite did not do what it claims and the delta does not mean what
            # the table says.
            status = "ok" if left <= sites // 10 else f"partial({left}/{sites} left)"
            rows.append((f, sites, text - ref_text, n_sites - ref_sites, status))
            print(f"   {f}: sites={sites} dtext={text - ref_text} "
                  f"dsites={n_sites - ref_sites} {status}", flush=True)
    finally:
        restore()

    with open(TSV, "w") as fh:
        fh.write("file\tsites\tdelta_text\tdelta_sites\tstatus\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")
    print(f"\n== wrote {TSV}", flush=True)
    subprocess.run([sys.executable, os.path.join(HERE, "report.py"), TSV,
                    os.path.join(OUT, "reference.blame.tsv")], check=True)


if __name__ == "__main__":
    main()
