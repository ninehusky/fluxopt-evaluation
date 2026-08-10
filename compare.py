#!/usr/bin/env python3
"""Turn two measure.py JSON files into one markdown table.

    ./compare.py results/baseline.json results/modified.json
"""

import json
import re
import sys

# LLVM appends ` (.llvm.<hash>)` to internal symbols, and the hash changes
# between the two builds for what is otherwise the same function.  Strip it
# before diffing the two name sets, or every such function looks both added
# and removed.  The counts above the diff use the raw symbols.
LLVM_SUFFIX_RE = re.compile(r" \(\.llvm\.\d+\)$")

# Allocated sections only.  The .debug_* sections are large and are an artifact
# of `[profile.release] debug = 2`, which both repos set; they are in the JSON
# and in the .sections.txt dumps if you want them.
SECTIONS = [".text", ".rodata", ".data", ".bss"]


def row(name, a, b):
    d = b - a
    pct = f"{100.0 * d / a:+.1f}%" if a else "n/a"
    return f"| {name} | {a} | {b} | {d:+} | {pct} |"


def main():
    a = json.load(open(sys.argv[1]))
    b = json.load(open(sys.argv[2]))

    print("| metric | baseline | modified | delta | delta % |")
    print("| --- | --- | --- | --- | --- |")
    for s in SECTIONS:
        print(row(s, a["sections"].get(s, 0), b["sections"].get(s, 0)))
    # Flash footprint: what the linker actually puts in ROM (.bss is RAM-only).
    flash = lambda m: sum(m["sections"].get(s, 0) for s in (".text", ".rodata", ".data"))
    print(row("flash (.text+.rodata+.data)", flash(a), flash(b)))
    print(row("panic call sites", a["panic_call_sites"], b["panic_call_sites"]))
    print(row("panicking functions",
              a["panicking_function_count"], b["panicking_function_count"]))

    names = lambda m: {LLVM_SUFFIX_RE.sub("", f) for f in m["panicking_functions"]}
    only_a = sorted(names(a) - names(b))
    only_b = sorted(names(b) - names(a))
    print(f"\nPanicking in baseline but not modified ({len(only_a)}):")
    for f in only_a:
        print(f"  - {f}")
    print(f"\nPanicking in modified but not baseline ({len(only_b)}):")
    for f in only_b:
        print(f"  - {f}")
    print("\nFull lists: results/*.panicking-functions.txt; "
          "every call site: results/*.panic-call-sites.txt")


if __name__ == "__main__":
    main()
