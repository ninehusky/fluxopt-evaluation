#!/usr/bin/env python3
"""Generate results/WORKLIST.md -- every panic site in the firmware, as spans,
grouped into the ROADMAP phases.

    ./worklist.py

This is the thing you open to start hacking. One row per source line, with a
`path:line` span you can click, how many machine call sites that line compiles
to, the panic kind, the owning function and the source text.

Covers all 650 sites, not just the xarxa ones: phases 5 and 6 are the crates
xarxa proofs cannot reach, and they were unscoped until now.

Inputs are all tool output:
  results/modified.blame.tsv   every site in the linked binary       (blame.py)
  results/TRIAGE-sites.tsv     the Flux obligation per xarxa site    (triage.py)
  results/ablation.json        measured budgets                      (sweep.py)
"""

import collections
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan as P                                                    # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
R = lambda *p: os.path.join(HERE, "results", *p)
XARXA_PREFIX = "third_party/xarxa/"
XARXA = os.environ.get("XARXA", "/Users/andrew/research/xarxa-specs")
REPO = os.path.join(HERE, "work", "modified")

SHORT = {
    "core::slice::index::slice_index_fail": "slice-index",
    "core::panicking::panic_bounds_check": "bounds-check",
    "core::panicking::panic": "panic!/unreachable!",
    "core::panicking::panic_fmt": "panic!(fmt)",
    "core::option::expect_failed": "expect",
    "core::option::unwrap_failed": "unwrap",
    "core::result::unwrap_failed": "unwrap",
    "core::slice::copy_from_slice_impl::len_mismatch_fail": "copy_from_slice",
    "core::cell::panic_already_borrowed": "RefCell",
    "core::cell::panic_already_mutably_borrowed": "RefCell",
    "core::panicking::panic_const::panic_const_rem_by_zero": "rem-by-zero",
    "core::panicking::panic_const::panic_const_async_fn_resumed": "async-resumed",
    "_defmt_panic": "defmt",
}

PHASES = {
    0: ("Phase 0 — xarxa CHURN",
        "State a length or range precondition and discharge it, then follow the "
        "obligation to the callers. Fully delegable; four agents are on udp, ipv4, "
        "ndiscoption and nhc as of 2026-08-11."),
    1: ("Phase 1 — the attribution gap",
        "Sites with no Flux obligation attached: they fall outside any function the "
        "triage parser recognises (macro bodies, derives, closures), or DWARF gave no "
        "statement at all. Diagnosis, not proof. Until these are categorised the xarxa "
        "endgame cannot be costed."),
    2: ("Phase 2 — xarxa PANIC",
        "An explicit panic!/unreachable!/assert!/expect. Needs a REACHABILITY argument, "
        "and the fact that kills the branch usually lives in another module. Blocked on "
        "picking a type invariant, not on effort."),
    3: ("Phase 3 — xarxa CORE",
        "Iterator / Option / Result chains Flux cannot see through. Same shape as the "
        "byteorder work in PR #14: copy the dependency closure from "
        "flux/lib/flux-core/src/ into flux_specs.rs. Do NOT load flux-core wholesale."),
    4: ("Phase 4 — compiler work",
        "Flux itself falls over: `internal flux error`, or rustc aborts. Not delegable. "
        "The `<&T as AsRef<[u8]>>::idx` gap belongs here too -- it has no site of its "
        "own but gates payload() in 16 wire files."),
    5: ("Phase 5 — logging and formatting",
        "defmt, defmt-rtt and core's integer formatting. NOT proof targets: no annotation "
        "removes these, they only go away if the example builds without defmt. A decision "
        "about what the benchmark may be."),
    6: ("Phase 6 — the embassy crates and other dependencies",
        "Outside xarxa entirely, so no xarxa proof reaches them. Lives in "
        "ninehusky/embassy, a fork we control, so the same opt-in method applies -- but "
        "this is async executors and USB state machines, expect it to be harder."),
}

CAT_TO_PHASE = {"CHURN": 0, "CLEAN": 0, "UNATTRIBUTED": 1,
                "PANIC": 2, "CORE": 3, "SPEC": 3, "FLUXBUG": 4, "ICE": 4}
FMT_MARKERS = ("defmt", "/fmt/num.rs", "int_log10", "/fmt/mod.rs", "fmt/builders.rs")


def short(sym):
    return SHORT.get(sym, sym.split("::")[-1] if "::" in sym else sym)


def const_spans_for(rel):
    """Line numbers inside a `const fn` body -- the ablator skips these, and they
    are the leading explanation for a site that survives ablation."""
    try:
        sys.path.insert(0, os.path.join(
            os.environ.get("ABLATE_DIR", ""), ""))
        import ablate                                               # noqa
    except Exception:
        return set()
    path = os.path.join(XARXA, rel)
    if not os.path.exists(path):
        return set()
    src = open(path, errors="replace").read()
    out = set()
    for a, b in ablate.const_spans(src):
        out.update(range(src.count("\n", 0, a) + 1, src.count("\n", 0, b) + 2))
    return out


def source_of(path, line):
    """Best-effort source text. xarxa comes from the checkout, embassy from the
    build tree; registry and rustc paths are read if present, skipped if not."""
    if line <= 0:
        return ""
    # xarxa rows are keyed by a path already relative to the checkout; everything
    # else is relative to the build tree, or absolute (registry / rustc sources).
    rel = path[len(XARXA_PREFIX):] if path.startswith(XARXA_PREFIX) else path
    for cand in (os.path.join(XARXA, rel), os.path.join(REPO, path), path):
        if cand and os.path.exists(cand) and os.path.isfile(cand):
            try:
                lines = open(cand, errors="replace").read().splitlines()
            except OSError:
                continue
            if line <= len(lines):
                return lines[line - 1].strip()
    return ""


def main():
    cats = {}
    with open(R("TRIAGE-sites.tsv")) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            m = row["messages"]
            c = ("CLEAN" if not m else
                 "ICE" if m.startswith("rustc aborted") else
                 P.classify("OBLIGATION", m))
            cats[(row["file"], int(row["site_line"]))] = (c, row["fn"])

    # (phase, path, line) -> [kinds]
    rows = collections.defaultdict(list)
    for path, line, sym, addr in csv.reader(open(R("modified.blame.tsv")),
                                            delimiter="\t"):
        line = int(line)
        if path.startswith(XARXA_PREFIX):
            rel = path[len(XARXA_PREFIX):]
            cat, fn = cats.get((rel, line), ("UNATTRIBUTED", ""))
            ph = CAT_TO_PHASE.get(cat, 1)
            rows[(ph, rel, line)].append((short(sym), cat, fn))
        elif any(k in path for k in FMT_MARKERS):
            rows[(5, path, line)].append((short(sym), "", ""))
        else:
            rows[(6, path, line)].append((short(sym), "", ""))

    per_phase = collections.Counter()
    for (ph, _, _), v in rows.items():
        per_phase[ph] += len(v)
    total = sum(per_phase.values())

    A = json.load(open(R("ablation.json")))
    resid = {}   # phase-1 residue: files where sites survive full ablation
    for k, v in A.get("ablation_resistant_by_file", {}).items():
        resid[k] = v

    w = open(R("WORKLIST.md"), "w").write
    w("# Worklist: every panic site, by phase\n\n")
    w(f"All {total} panic sites in the linked nRF52840 `usb_ethernet` binary, "
      "grouped into the phases in [ROADMAP.md](ROADMAP.md). Regenerate with "
      "`./worklist.py`.\n\n")
    w("One row per source **line**; `sites` is how many machine call sites that "
      "line compiles to, because generics and inlining duplicate it. Lines track "
      "effort, sites track the metric. `line 0` means DWARF blamed the file but no "
      "statement.\n\n")

    w("| phase | sites | what |\n| --- | ---: | --- |\n")
    for ph in sorted(PHASES):
        w(f"| [{ph}](#phase-{ph}) | {per_phase[ph]} | {PHASES[ph][0].split('— ')[1]} |\n")
    w(f"| | **{total}** | |\n\n")

    for ph in sorted(PHASES):
        title, blurb = PHASES[ph]
        w(f"---\n\n<a id=\"phase-{ph}\"></a>\n## {title}\n\n")
        w(f"{per_phase[ph]} sites. {blurb}\n\n")
        if ph == 1:
            w("**Also in this phase, and not in the table below:** 53 xarxa sites "
              "survive even a full unsound `get_unchecked` ablation, so they cannot "
              "be removed by any means currently known. 20 are in "
              "`src/wire/sixlowpan/iphc.rs`, 4 each in `wire/mod.rs`, `ipv6.rs` and "
              "`ieee802154.rs`. Named causes so far: `const fn` bodies (the ablator "
              "skips them, `get_unchecked` is not const-stable), `[u8; N]` arrays "
              "(the ablator's index trait covers `[T]` only), and borrowck conflicts "
              "in `assembler.rs`. Rows below marked `const-fn` are inside a const "
              "body and are the prime suspects.\n\n")
        if ph == 4:
            w("**Also in this phase:** the `<&T as AsRef<[u8]>>::idx` gap. Repro is "
              "left uncommitted in `/Users/andrew/research/xarxa-icmpv6` at "
              "`src/wire/icmpv6.rs:529` — 0 `panicked`, exactly 2 errors, one "
              "function. ICE-2 made the signature convert; it still does not "
              "discharge.\n\n")

        byfile = collections.defaultdict(list)
        for (p, path, line), v in rows.items():
            if p == ph:
                byfile[path].append((line, v))
        for path in sorted(byfile, key=lambda f: (-sum(len(v) for _, v in byfile[f]), f)):
            n = sum(len(v) for _, v in byfile[path])
            disp = path[len(XARXA_PREFIX):] if path.startswith(XARXA_PREFIX) else path
            consts = const_spans_for(disp) if ph == 1 and path.startswith(XARXA_PREFIX) else set()
            w(f"### `{disp}` — {n} sites\n\n")
            w("| span | sites | kind | fn | source |\n| --- | ---: | --- | --- | --- |\n")
            for line, v in sorted(byfile[path]):
                kinds = sorted({k for k, _, _ in v})
                fn = next((f for _, _, f in v if f), "")
                src = source_of(path, line).replace("|", "\\|")[:88]
                span = f"`{disp}:{line}`" if line > 0 else f"`{disp}` (no line)"
                note = " **const-fn**" if line in consts else ""
                w(f"| {span} | {len(v)} | {', '.join(kinds)}{note} | `{fn}` | `{src}` |\n")
            w("\n")

    print(f"wrote {R('WORKLIST.md')}")
    for ph in sorted(PHASES):
        print(f"  phase {ph}: {per_phase[ph]:4} sites")
    print(f"  total:   {total:4}")


if __name__ == "__main__":
    main()
