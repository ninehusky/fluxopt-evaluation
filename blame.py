#!/usr/bin/env python3
"""Attribute each panic call site to the source file that owns it.

    ./blame.py results/modified.json work/modified > results/modified.blame.tsv

Reads the addresses measure.py recorded, asks llvm-symbolizer for the inline
stack at each one, and picks the blamed frame.

Blame rule -- the only judgement call in here, worth reading:

    Walk the inline stack from the innermost frame outwards and take the first
    frame whose file is NOT inside the Rust standard library source
    (rustlib/src/rust/library/...).  A bounds check reported at
    core/src/slice/index.rs:443 is not something you can fix in core; the frame
    below it is the code that did the indexing, and that is what you would
    refine.  If every frame is in the standard library the site is blamed to
    "<std>" and shows up in the output as such.

Paths are printed relative to the build root passed as the second argument, so
`third_party/xarxa/src/wire/ipv4.rs` rather than an absolute path.

Output is TSV: file, line, panic symbol, address -- one row per call site.
Aggregate it however you like:

    cut -f1 results/modified.blame.tsv | sort | uniq -c | sort -rn
"""

import json
import os
import shutil
import subprocess
import sys

STD_MARKER = "rustlib/src/rust/library/"
SYMBOLIZER = os.environ.get("LLVM_SYMBOLIZER") or shutil.which("llvm-symbolizer")


def symbolize(elf, addrs):
    """One llvm-symbolizer process for all addresses; yields the inline stack."""
    if not SYMBOLIZER:
        sys.exit("llvm-symbolizer not found; set LLVM_SYMBOLIZER (Homebrew LLVM has it)")
    query = "".join(f"0x{a}\n" for a in addrs)
    out = subprocess.run(
        [SYMBOLIZER, f"--obj={elf}", "--inlines", "--demangle", "--output-style=LLVM"],
        input=query, capture_output=True, text=True, check=True,
    ).stdout
    # Each address prints its stack as alternating function / file:line:col
    # lines, terminated by a blank line.  Split on the blank lines first, then
    # take every second line -- doing it in one pass desynchronises.
    record = []
    for line in out.splitlines():
        if not line.strip():
            if record:
                yield record[1::2]
                record = []
            continue
        record.append(line.strip())
    if record:
        yield record[1::2]


def blame(stack, root):
    """First frame outside the Rust standard library; see the rule above."""
    for frame in stack:
        if STD_MARKER in frame:
            continue
        path, _, rest = frame.partition(":")
        line = rest.split(":")[0]
        return os.path.relpath(path, root) if path.startswith(root) else path, line
    return "<std>", "0"


def main():
    data = json.load(open(sys.argv[1]))
    root = os.path.abspath(sys.argv[2])
    sites = data["sites"]

    stacks = list(symbolize(data["elf"], [a for a, _, _ in sites]))
    if len(stacks) != len(sites):
        sys.exit(f"symbolizer returned {len(stacks)} stacks for {len(sites)} sites")

    for (addr, _, target), stack in zip(sites, stacks):
        f, line = blame(stack, root)
        print(f"{f}\t{line}\t{target}\t0x{addr}")


if __name__ == "__main__":
    main()
