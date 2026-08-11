#!/usr/bin/env python3
"""Does a discharged precondition actually reach its fan-in cone, or is it absorbed?

    ./cone.py <xarxa-checkout> src/wire/ndiscoption.rs

A `requires` on a function whose callers are all `default_trusted` discharges
NOTHING. It moves the obligation to somewhere nobody is looking, and the output
is byte-identical to the output you get when the obligation is genuinely met:
silence. `check_proof.py` check 2 tries to catch this by name-matching direct
callers, and it does not work -- it reported 179 candidate rows for `ipv4.rs`, all
of them collisions, and it skips same-file callers entirely, which is exactly
where the absorption happens (`ndiscoption::Repr::emit`).

This checks it the only way that cannot be fooled: TURN THE CALLERS ON AND ASK
FLUX. Flux already resolves calls properly, so it is the call graph -- no separate
call-graph tool, no name matching, no type resolution of our own.

    baseline   run as-is, record the errors
    probe      stamp `#[flux_rs::trusted(no)]` on EVERY function in the crate that
               is not already annotated, run again
    verdict    every error the probe adds is an obligation that was previously
               being absorbed by a trusted caller

An added error is not a regression -- it is the proof obligation becoming visible
for the first time. A file whose probe adds ZERO errors is one whose preconditions
are genuinely established by its cone, and only then may a checked operation there
be replaced with `get_unchecked`.

The checkout is restored with `git checkout -- .` on the way out, including on
Ctrl-C. Nothing is committed.
"""

import collections
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FEATURES = ("defmt,socket-tcp,proto-ipv4,medium-ethernet,socket-dhcpv4,socket-udp,"
            "medium-ieee802154,proto-ipv6,auto-icmp-echo-reply,async")
ATTR = '#[flux_rs::trusted(no, reason = "cone probe: is this obligation established?")]'
FN_RE = re.compile(r"\s*(?:pub(?:\([^)]*\))?\s+)?(?:const\s+|async\s+|unsafe\s+)*fn\s+(\w+)")

# `flux_rs::defs! { fn header_len(code: int) -> int { .. } }` declares refinement
# functions, not Rust ones. They match FN_RE, they are not items, and stamping one
# with `#[flux_rs::trusted]` is a syntax error -- the same failure that `SKIP_FILES`
# already handles for `flux_specs.rs`, except a `defs!` block can sit in any file.
DEFS_RE = re.compile(r"^\s*(?:flux_rs::|flux::)?defs!\s*\{")


def functions(path):
    out, src = [], open(path, errors="replace").read().splitlines()
    cur, depth, start = None, 0, 0
    defs_depth = 0
    for i, line in enumerate(src, 1):
        if defs_depth > 0:
            defs_depth += line.count("{") - line.count("}")
            continue
        if DEFS_RE.match(line):
            defs_depth = line.count("{") - line.count("}")
            continue
        m = FN_RE.match(line)
        if m and cur is None:
            cur, start, depth = m.group(1), i, 0
        if cur:
            depth += line.count("{") - line.count("}")
            if depth <= 0 and "{" in "".join(src[start - 1:i]):
                out.append((cur, start, i)); cur = None
    return out


def run(checkout, log):
    with open(log, "w") as f:
        subprocess.run(["cargo", "flux", "check", "-p", "xarxa", "--no-default-features",
                        "--features", FEATURES], cwd=checkout, stdout=f, stderr=f)
    body = open(log, errors="replace").read()
    if "panicked" in body:
        sys.exit(f"REFUSING: {log} contains 'panicked' -- an ICE drops most "
                 "diagnostics, so nothing from this run can be compared.")
    errs = collections.Counter()
    msg = None
    for l in body.splitlines():
        if l.startswith("error["):
            msg = re.sub(r"^error\[[^\]]*\]: ", "", l).strip()
        m = re.match(r"\s*--> (src/[^:]+):(\d+):(\d+)", l)
        if m and msg:
            errs[(m.group(1), int(m.group(2)), int(m.group(3)), msg[:70])] += 1
            msg = None
    return errs


# `flux_specs.rs` is nothing but `extern_spec` blocks and a `defs!` macro. The
# `fn` lines in there are spec declarations, not bodies, and stamping them is a
# syntax error rather than an opt-in.
SKIP_FILES = {"flux_specs.rs"}

# Files quarantined from the probe because opting them in ICEs Flux, which
# aborts rustc and drops the rest of the crate's diagnostics -- making the whole
# comparison unusable rather than merely incomplete. Measured, not assumed:
# `iface/interface/mod.rs` gives `UnsolvedEvar(?98e)` at flux-infer/src/infer.rs:416
# (`dispatch_ip`; also hit independently by the ipv4 agent).
#
# Quarantining means those callers stay trusted, so an obligation absorbed THERE
# is invisible to this check. That is a hole in the gate and it is reported as
# one, rather than being silently counted as a pass.
SKIP_PATHS = {"src/iface/interface/mod.rs"}


def attrs_by_fn_line(src):
    """{fn_start_line: attribute-and-doc block preceding it}, by forward pass.

    Two earlier versions of this walked UPWARDS from the `fn` line with textual
    heuristics, and both mis-parsed the same shape: a `#[flux_rs::trusted]`
    sitting above a MULTI-LINE `#[flux_rs::sig(...)]`. The walk stopped at the
    sig's continuation lines, concluded the function was unannotated, stamped a
    second `trusted` on it, and the crate failed to build with `duplicated
    attribute Trusted`.

    Going forwards and tracking bracket depth handles multi-line attributes
    without guessing what a continuation line looks like.
    """
    out, pending, depth = {}, [], 0
    for i, line in enumerate(src, 1):
        if depth > 0:                            # inside a multi-line attribute
            pending.append(line)
            depth += (line.count("(") + line.count("[")
                      - line.count(")") - line.count("]"))
            continue
        s = line.strip()
        if s.startswith("#[") or s.startswith("#!"):
            pending.append(line)
            depth += (line.count("(") + line.count("[")
                      - line.count(")") - line.count("]"))
            continue
        if not s or s.startswith("//"):
            pending.append(line)
            continue
        if FN_RE.match(line):
            out[i] = "".join(pending)
        pending = []
    return out


def stamp_all(checkout):
    """Opt in every function in the crate that is not already annotated."""
    n = 0
    for root, _, files in os.walk(os.path.join(checkout, "src")):
        for fname in files:
            if not fname.endswith(".rs") or fname in SKIP_FILES:
                continue
            p = os.path.join(root, fname)
            if os.path.relpath(p, checkout) in SKIP_PATHS:
                continue
            src = open(p, errors="replace").read().splitlines(True)
            attrs = attrs_by_fn_line(src)
            for name, lo, hi in sorted(functions(p), key=lambda f: -f[1]):
                head = attrs.get(lo, "")
                if "trusted" in head or "ignore" in head:
                    continue
                indent = re.match(r"\s*", src[lo - 1]).group(0)
                src.insert(lo - 1, f"{indent}{ATTR}\n")
                n += 1
            open(p, "w").writelines(src)
    return n


def main():
    checkout = os.path.abspath(sys.argv[1])
    targets = sys.argv[2:]
    # Per-checkout, because several agents run this at once against different
    # worktrees. A shared `/tmp/cone-base.log` meant the second run to start
    # silently compared its own probe against someone else's baseline.
    scratch = os.environ.get("SCRATCH", "/tmp")
    scratch = os.path.join(scratch, "cone-" + os.path.basename(checkout))
    os.makedirs(scratch, exist_ok=True)
    restore = lambda: subprocess.run(["git", "checkout", "--", "."], cwd=checkout,
                                     check=False)
    try:
        restore()
        print(f"== baseline (the branch as committed); logs in {scratch}", flush=True)
        base = run(checkout, os.path.join(scratch, "cone-base.log"))
        print(f"   {sum(base.values())} errors", flush=True)

        n = stamp_all(checkout)
        print(f"== probe: opted in {n} further functions; re-running", flush=True)
        probe = run(checkout, os.path.join(scratch, "cone-probe.log"))
        print(f"   {sum(probe.values())} errors", flush=True)

        # SANITY, and it is not optional. The first version of this script
        # stamped `flux_specs.rs` and double-stamped already-trusted functions;
        # the probe failed to COMPILE, reported 5 errors against a baseline of
        # 42, and the script cheerfully concluded that nothing was absorbed. A
        # probe that opts thousands of functions in cannot legitimately produce
        # fewer errors than the baseline, and a build that did not compile
        # proves nothing at all.
        body = open(os.path.join(scratch, "cone-probe.log"), errors="replace").read()
        broken = [m for m in ("syntax error", "duplicated attribute",
                              "cannot find attribute") if m in body]
        if broken:
            sys.exit(f"PROBE IS BROKEN, not a result: log contains {broken}. "
                     "The stamping damaged the crate; fix stamp_all before "
                     "believing any verdict.")
        if sum(probe.values()) < sum(base.values()):
            sys.exit(f"PROBE IS BROKEN, not a result: opting in {n} functions "
                     f"REDUCED errors {sum(base.values())} -> {sum(probe.values())}. "
                     "That is impossible if the probe compiled and ran.")
    finally:
        restore()

    # Errors the probe ADDS are obligations that a trusted caller was absorbing.
    # Line numbers shift under stamping, so compare on (file, message) and count,
    # never on line -- comparing lines would report the whole crate as new.
    def key(e):
        return collections.Counter((f, m) for (f, _, _, m), c in e.items()
                                   for _ in range(c))
    added = key(probe) - key(base)

    print(f"\n== {sum(added.values())} obligations were being absorbed by trusted callers")
    if SKIP_PATHS:
        print(f"   (blind spot: {sorted(SKIP_PATHS)} stayed trusted -- they ICE Flux "
              f"when opted in, so anything absorbed there is NOT counted here)")
    byfile = collections.Counter()
    for (f, _), c in added.items():
        byfile[f] += c
    for f, c in byfile.most_common(20):
        mark = "  <-- TARGET" if any(f == t for t in targets) else ""
        print(f"   {c:4}  {f}{mark}")

    if targets:
        print()
        bad = 0
        for t in targets:
            c = byfile.get(t, 0)
            bad += c
            print(f"{'FAIL' if c else 'OK  '} {t}: {c} absorbed obligation(s)")
        print("\nAn absorbed obligation is NOT proven. Replacing a checked operation "
              "with get_unchecked on this basis would be unsound.")
        sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
