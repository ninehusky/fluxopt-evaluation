#!/usr/bin/env python3
"""Measure one linked ELF: section sizes, panic call sites, panicking functions.

    ./measure.py <elf> <out-prefix>

Writes <out-prefix>.json plus three plain-text dumps you can read to check the
classification by hand.

The two commands it shells out to are the only source of truth:

    $LLVM_BIN/llvm-size -A <elf>
    $LLVM_BIN/llvm-objdump -d --demangle <elf>

Definitions
-----------
panic symbol
    A function symbol whose demangled name matches PANIC_RE below: the panic
    entry points in core, the #[panic_handler], and defmt/panic-probe's.  The
    list is spelled out rather than matched on the substring "panic", because
    (a) several entry points do not contain the word -- core::option::
    unwrap_failed, core::slice::index::slice_index_fail -- and (b) ordinary
    library code does, e.g. xarxa's HardwareAddress::ethernet_or_panic, which
    is a normal function that happens to panic, not part of the machinery.
    To check the list is still complete for a given ELF, run:

        llvm-nm --demangle <elf> | grep -iE 'panic|unwind|_fail'

panic call site
    One branch instruction in the disassembly whose target is a panic symbol,
    where the function containing the branch is NOT itself a panic symbol.
    The exclusion matters: core::panicking::panic calls panic_fmt calls
    rust_begin_unwind, and counting those would measure the size of the panic
    machinery rather than the number of places ordinary code can enter it.
    Both direct calls (bl) and tail calls (b, and conditional branches such as
    the bcs rustc emits for a bounds check) count, since -O turns many panic
    calls into tail branches.

panicking function
    A function containing at least one panic call site.  Counted once no
    matter how many panic call sites it has.  A wrapper like ethernet_or_panic
    shows up here, via the branch to core::panicking::panic inside it.
"""

import json
import os
import re
import subprocess
import sys

PANIC_RE = re.compile(
    r"^(?:__rustc::)?rust_begin_unwind$"                        # the #[panic_handler]
    r"|^core::panicking::"                                      # panic, panic_fmt,
                                                                # panic_bounds_check,
                                                                # panic_const::*, assert_failed
    r"|^core::cell::panic_already_"                             # RefCell
    r"|^core::(?:option|result)::(?:unwrap_failed|expect_failed)$"
    r"|^core::slice::index::slice_index_fail$"
    r"|^core::slice::copy_from_slice_impl::len_mismatch_fail$"
    r"|^(?:_|__)defmt_(?:default_)?panic$"
    r"|^panic_probe::"
)

# `<addr> <name>:` -- start of a function in llvm-objdump output.
FUNC_RE = re.compile(r"^[0-9a-f]+ <(.+)>:$")
# The instruction mnemonic is the first token that is not part of the hex
# encoding; thumb encodings print as 4- or 8-digit groups.
ENCODING_RE = re.compile(r"^[0-9a-f]{4}(?:[0-9a-f]{4})?$")
# b / bl / blx / bx-free conditional branches, optionally .n or .w suffixed.
BRANCH_RE = re.compile(
    r"^b(l|lx|eq|ne|cs|hs|cc|lo|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?(\.[nw])?$"
)
# The branch target symbol, printed last on the instruction: `bl 0x1234 <name>`.
# `.+` rather than `[^>]+` because demangled names contain angle brackets
# themselves (`<T as Trait>::f`); the trailing `@ imm = #0x123` comment that
# llvm-objdump appends is stripped off first, by COMMENT_RE.
TARGET_RE = re.compile(r"<(.+)>\s*$")
COMMENT_RE = re.compile(r"\s+@\s")


def llvm(tool, *args):
    exe = os.path.join(os.environ.get("LLVM_BIN", ""), tool)
    return subprocess.run([exe, *args], capture_output=True, text=True, check=True).stdout


def sections(elf):
    """llvm-size -A output -> {section name: size in bytes}."""
    out = {}
    for line in llvm("llvm-size", "-A", elf).splitlines():
        f = line.split()
        # `.text  12345  67890`; skip headers and the trailing Total line.
        if len(f) >= 2 and f[0].startswith(".") and f[1].isdigit():
            out[f[0]] = int(f[1])
    return out


def panics(elf):
    """Walk the disassembly once, collecting (caller, panic target) pairs."""
    calls = []  # (calling function, panic symbol called)
    func = None
    for line in llvm("llvm-objdump", "-d", "--demangle", elf).splitlines():
        m = FUNC_RE.match(line.strip())
        if m:
            func = m.group(1)
            continue
        if func is None or ":" not in line:
            continue
        line = COMMENT_RE.split(line, 1)[0]
        tokens = line.split(":", 1)[1].split()
        tokens = [t for t in tokens if not ENCODING_RE.match(t)]
        if not tokens or not BRANCH_RE.match(tokens[0]):
            continue
        target = TARGET_RE.search(line)
        if target and PANIC_RE.search(target.group(1)):
            if not PANIC_RE.search(func):  # skip panic machinery calling itself
                calls.append((func, target.group(1)))
    return calls


def main():
    elf, prefix = sys.argv[1], sys.argv[2]
    calls = panics(elf)

    callers = sorted({c for c, _ in calls})
    targets = {}
    for _, t in calls:
        targets[t] = targets.get(t, 0) + 1

    data = {
        "elf": elf,
        "sections": sections(elf),
        "panic_call_sites": len(calls),
        "panicking_function_count": len(callers),
        "panicking_functions": callers,
        "panic_targets": dict(sorted(targets.items(), key=lambda kv: -kv[1])),
    }
    with open(prefix + ".json", "w") as f:
        json.dump(data, f, indent=2)

    with open(prefix + ".sections.txt", "w") as f:
        f.write(llvm("llvm-size", "-A", elf))
    with open(prefix + ".panicking-functions.txt", "w") as f:
        f.write("\n".join(callers) + "\n")
    # Every (caller -> panic symbol) pair, so the PANIC_RE matches above can be
    # checked one by one against the disassembly.
    with open(prefix + ".panic-call-sites.txt", "w") as f:
        f.write("\n".join(f"{c}\t->\t{t}" for c, t in sorted(calls)) + "\n")

    print(
        f"{elf}: {len(calls)} panic call sites in {len(callers)} functions",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
