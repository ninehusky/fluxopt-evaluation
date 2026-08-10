#!/usr/bin/env python3
"""Join the sweep results with the panic inventory into one markdown table.

    ./report.py [wins.tsv] [reference.blame.tsv] > results/PER-FILE-WINS.md

Defaults to what sweep.py just wrote: results/per-file-wins.tsv (the measured
deltas) and results/ablate/reference.blame.tsv (which file owns which site).
"""

import collections
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WINS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results/per-file-wins.tsv")
BLAME = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "results/ablate/reference.blame.tsv")
PREFIX = "third_party/xarxa/"

# Shorten the panic entry points to something that fits in a table cell.
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
    "_defmt_panic": "defmt",
}


def short(sym):
    if sym in SHORT:
        return SHORT[sym]
    if "assert_failed" in sym:
        return "assert!"
    return sym.split("::")[-1]


def main():
    kinds = collections.defaultdict(collections.Counter)
    for row in csv.reader(open(BLAME), delimiter="\t"):
        if row[0].startswith(PREFIX):
            kinds[row[0][len(PREFIX):]][short(row[2])] += 1

    rows = list(csv.DictReader(open(WINS), delimiter="\t"))
    ok = [r for r in rows if r["delta_text"] not in ("", None)]
    for r in ok:
        r["dt"] = int(r["delta_text"])

    # Empirical noise floor: ablation can only remove panics, so any file that
    # got BIGGER did so through inlining/layout churn.  The largest such move is
    # a lower bound on how much churn a single-file rebuild can produce.
    noise = max([r["dt"] for r in ok if r["dt"] > 0] or [0])

    print("# Per-file panic ablation, nRF52840 `usb_ethernet`\n")
    print("`.text` bytes that disappear when a file is made panic-free. "
          "Produced by `./sweep.py`; see ../README.md for the method.\n")
    print(f"Reference `.text` reproduced exactly across rebuilds, so the "
          f"deltas are not build noise. But a single-file rebuild still shifts "
          f"inlining: the largest *increase* seen was **+{noise} B**, so treat "
          f"|delta| under roughly that as unresolved.\n")
    print("| file | sites | what they are | Δ.text | Δsites | status |")
    print("| --- | --- | --- | --- | --- | --- |")
    for r in sorted(rows, key=lambda r: r.get("dt", 0)):
        k = ", ".join(f"{n}×{n_}" if False else f"{n_} {n}"
                      for n, n_ in kinds[r["file"]].most_common(3))
        dt = f'{r["dt"]:+}' if "dt" in r else "—"
        ds = r["delta_sites"] or "—"
        print(f'| `{r["file"]}` | {r["sites"]} | {k} | {dt} | {ds} | {r["status"]} |')


if __name__ == "__main__":
    main()
