#!/usr/bin/env python3
"""Measurement primitives for the usb_ethernet size/panic-site study.

This module is intentionally free of any hard-coded expected values. Every
number it produces is derived from a binary that was built in the same job.
Nothing here is a fixture.

It exposes two things:

  * ``measure_binary(...)`` -> dict, the full measurement of one ELF, and
  * a small CLI (``python measure.py <elf> ...``) used for local debugging.

The panic-site classifier is deliberately explicit: the exact regexes it
matches against are echoed back into the output under ``match_patterns`` so a
reader never has to guess what "panic-related" meant for a given run. Symbols
that look panic-ish but do not match any explicit pattern are surfaced under
``unclassified_candidates`` rather than being silently folded in or dropped.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from typing import Dict, List, Optional


# --- panic-site classification ------------------------------------------------
#
# Symbols are matched in their raw (v0-mangled) form. The mangled name embeds
# the identifier as a length-prefixed substring, e.g.
#   _RNvNtCs..._4core9panicking9panic_fmt
# so a plain substring/regex search over the mangled symbol is sufficient and
# fully deterministic (no demangler in the trusted path).
#
# These are the patterns named by the task. They are recorded verbatim in the
# JSON output for every run.
PANIC_PATTERNS: Dict[str, str] = {
    "panic": r"panic",
    "panic_fmt": r"panic_fmt",
    "unwrap_failed": r"unwrap_failed",
    "panic_bounds_check": r"panic_bounds_check",
    "slice_index_fail": r"slice_index_fail",
    "expect_failed": r"expect_failed",
}

# A broader net used only to flag symbols that *look* panic-related but do not
# match any explicit pattern above. These go in ``unclassified_candidates`` so
# they are neither counted nor hidden -- a human decides.
CANDIDATE_HINT = re.compile(
    r"(panic|_fail|abort|unwrap|expect|assert|bounds_check|"
    r"out_of_range|_oob|overflow)"
)

# "Panic formatting" machinery, checked for absence under panic=immediate-abort.
PANIC_FMT_MARKERS = (r"panic_fmt", r"9panicking", r"panicking")

# ARM/Thumb mnemonics that transfer control to a labelled target. Suffixes
# ``.w``/``.n`` are stripped before the membership test. ``bic``/``bkpt``/``bfi``
# etc. start with 'b' but are deliberately excluded.
_BRANCH_BASES = {
    "b", "bl", "bx", "blx", "cbz", "cbnz",
    "beq", "bne", "bcs", "bhs", "bcc", "blo", "bmi", "bpl",
    "bvs", "bvc", "bhi", "bls", "bge", "blt", "bgt", "ble", "bal",
}

# Matches a disassembly instruction line that carries a symbolic target:
#   "    e24:      \tbl\t0x1f660 <_RNvNt..panic_fmt> @ imm = #0x1e838"
_INSN_RE = re.compile(
    r"^\s*[0-9a-fA-F]+:\s+(?P<mnem>[a-z][a-z0-9.]*)\b.*?<(?P<sym>[^>]+)>"
)


def _strip_width(mnem: str) -> str:
    for suffix in (".w", ".n"):
        if mnem.endswith(suffix):
            return mnem[: -len(suffix)]
    return mnem


def _run(cmd: List[str]) -> str:
    return subprocess.run(
        cmd, check=True, capture_output=True, text=True
    ).stdout


def section_sizes(size_tool: str, elf: str) -> Dict[str, object]:
    """Return per-section sizes via ``llvm-size -A`` (System V layout).

    Section *sizes* only -- never the on-disk ELF file length. ``.text`` is the
    primary figure. Total is the sum reported by the tool.
    """
    out = _run([size_tool, "-A", elf])
    sections: Dict[str, int] = {}
    total: Optional[int] = None
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0].startswith("."):
            try:
                sections[parts[0]] = int(parts[1])
            except ValueError:
                continue
        elif parts[:1] == ["Total"]:
            try:
                total = int(parts[1])
            except (ValueError, IndexError):
                total = None
    wanted = [".text", ".rodata", ".data", ".bss"]
    result: Dict[str, object] = {name: sections.get(name, 0) for name in wanted}
    result["total"] = total if total is not None else sum(sections.values())
    result["all_sections"] = sections
    result["tool_invocation"] = f"{size_tool} -A {elf}"
    return result


def disassemble(objdump_tool: str, elf: str) -> str:
    """Full disassembly. ``--no-show-raw-insn`` keeps lines stable across runs
    (raw bytes are redundant for symbol matching)."""
    return _run([objdump_tool, "-d", "--no-show-raw-insn", elf])


def symbol_table(nm_tool: str, elf: str) -> str:
    return _run([nm_tool, elf])


def classify_panic_sites(disasm: str) -> Dict[str, object]:
    """Scan a disassembly for branch instructions whose target symbol is
    panic-related, using the explicit ``PANIC_PATTERNS``."""
    compiled = {name: re.compile(pat) for name, pat in PANIC_PATTERNS.items()}

    per_symbol_count: Counter = Counter()
    symbol_patterns: Dict[str, List[str]] = {}
    unclassified: Counter = Counter()
    total_sites = 0

    for line in disasm.splitlines():
        m = _INSN_RE.match(line)
        if not m:
            continue
        if _strip_width(m.group("mnem")) not in _BRANCH_BASES:
            continue
        sym = m.group("sym")

        matched = [name for name, rx in compiled.items() if rx.search(sym)]
        if matched:
            per_symbol_count[sym] += 1
            total_sites += 1
            if sym not in symbol_patterns:
                symbol_patterns[sym] = matched
        elif CANDIDATE_HINT.search(sym):
            unclassified[sym] += 1

    per_symbol = [
        {
            "symbol": sym,
            "count": per_symbol_count[sym],
            "matched_patterns": symbol_patterns[sym],
        }
        for sym in sorted(per_symbol_count, key=lambda s: (-per_symbol_count[s], s))
    ]

    return {
        "match_patterns": PANIC_PATTERNS,
        "branch_call_sites_total": total_sites,
        "distinct_panic_symbol_count": len(per_symbol_count),
        "distinct_panic_symbols": dict(per_symbol_count),
        "per_symbol": per_symbol,
        "unclassified_candidates": dict(unclassified),
    }


def panic_fmt_symbols_present(symtab: str, disasm: str) -> Dict[str, object]:
    """Look for panic-formatting symbols in both the symbol table and the set
    of branch targets. Used to verify that ``panic=immediate-abort`` actually
    stripped the formatting machinery."""
    markers = [re.compile(p) for p in PANIC_FMT_MARKERS]

    in_symtab = sorted(
        {
            line.split()[-1]
            for line in symtab.splitlines()
            if line.split() and any(rx.search(line) for rx in markers)
        }
    )

    branch_targets = set()
    for line in disasm.splitlines():
        m = _INSN_RE.match(line)
        if m and _strip_width(m.group("mnem")) in _BRANCH_BASES:
            branch_targets.add(m.group("sym"))
    in_branch_targets = sorted(
        t for t in branch_targets if any(rx.search(t) for rx in markers)
    )

    return {
        "markers": list(PANIC_FMT_MARKERS),
        "present_in_symbol_table": in_symtab,
        "present_as_branch_target": in_branch_targets,
        "present": bool(in_symtab or in_branch_targets),
    }


def measure_binary(
    elf: str,
    size_tool: str,
    objdump_tool: str,
    nm_tool: str,
) -> Dict[str, object]:
    disasm = disassemble(objdump_tool, elf)
    symtab = symbol_table(nm_tool, elf)
    return {
        "binary": elf,
        "sizes": section_sizes(size_tool, elf),
        "panic_sites": classify_panic_sites(disasm),
        "panic_fmt_check": panic_fmt_symbols_present(symtab, disasm),
        "_disasm": disasm,  # consumed by caller; stripped before results.json
    }


def _main() -> int:
    ap = argparse.ArgumentParser(description="Measure one ELF binary.")
    ap.add_argument("elf")
    ap.add_argument("--size", default="llvm-size")
    ap.add_argument("--objdump", default="llvm-objdump")
    ap.add_argument("--nm", default="llvm-nm")
    ap.add_argument("--disasm-out", help="write full disassembly here")
    args = ap.parse_args()

    result = measure_binary(args.elf, args.size, args.objdump, args.nm)
    disasm = result.pop("_disasm")
    if args.disasm_out:
        with open(args.disasm_out, "w") as fh:
            fh.write(disasm)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
