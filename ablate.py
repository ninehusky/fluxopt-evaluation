#!/usr/bin/env python3
"""Mechanically remove the panicking constructs from one Rust source file.

    ./ablate.py --diff  src/wire/ipv4.rs      # show what it would change
    ./ablate.py         src/wire/ipv4.rs      # rewrite in place

*** THIS IS THE PART TO AUDIT. ***  Everything else in this repo reads tool
output; this is the one component that edits code, and if it edits it wrongly
the file's measured "win" is wrong.  Two things make that safe to check:

  - `--diff` prints the exact rewrite, so you can read a file's changes before
    trusting its number.
  - the sweep re-measures panic sites per file afterwards.  An ablated file
    whose site count does not drop to ~0 was not really ablated, and the sweep
    reports it as a failure rather than as a small win.

The output is deliberately UNSOUND.  `get_unchecked` on an index this script
did not prove in range is UB.  That is fine and intended: these binaries exist
to be measured with llvm-size and are never flashed.  Do not run them.

Rewrites, in order of application:

  panic!(..) unreachable!(..) todo!() unimplemented!()
        -> unsafe { core::hint::unreachable_unchecked() }
  assert!(..) assert_eq!(..) assert_ne!(..) debug_assert*!(..)
        -> ()                     [the check is what creates the panic]
  x.unwrap()  x.expect("..")
        -> x.__ablate_unwrap()    [a safe wrapper around unwrap_unchecked,
                                   injected at the top of the file; a plain
                                   textual swap to unwrap_unchecked would need
                                   an unsafe block around an expression whose
                                   extent we would have to parse]
  base[idx]
        -> (*unsafe { base.get_unchecked(idx) })
        -> (*unsafe { base.get_unchecked_mut(idx) })   when MUT_HINT_RE says so

The mut/non-mut choice is the one heuristic here: see MUT_HINT_RE.  Getting it
wrong makes the file fail to compile, which the sweep reports -- it does not
silently produce a wrong number.
"""

import re
import sys

PRELUDE = """
// ---- injected by ablate.py; measurement build only, never flash this ----
// Fully qualified: crates like xarxa define their own `Result<T>` alias, and
// an unqualified `Result<T, E>` here would resolve to that instead.
trait __AblateUnwrap<T> { fn __ablate_unwrap(self) -> T; }
impl<T> __AblateUnwrap<T> for core::option::Option<T> {
    #[inline(always)]
    fn __ablate_unwrap(self) -> T { unsafe { self.unwrap_unchecked() } }
}
impl<T, E> __AblateUnwrap<T> for core::result::Result<T, E> {
    #[inline(always)]
    fn __ablate_unwrap(self) -> T { unsafe { self.unwrap_unchecked() } }
}
// Indexing goes through a method, not an inline `unsafe { .. }` block, for two
// reasons: method syntax gets the same autoref/autoderef that `base[i]` got,
// and a block would shorten the lifetime of temporaries in `&f().x[..]`.
trait __AblateIdx<I> {
    type Out: ?Sized;
    fn __ai(&self, i: I) -> &Self::Out;
    fn __ai_mut(&mut self, i: I) -> &mut Self::Out;
}
impl<T, I: core::slice::SliceIndex<[T]>> __AblateIdx<I> for [T] {
    type Out = I::Output;
    #[inline(always)]
    fn __ai(&self, i: I) -> &I::Output { unsafe { self.get_unchecked(i) } }
    #[inline(always)]
    fn __ai_mut(&mut self, i: I) -> &mut I::Output { unsafe { self.get_unchecked_mut(i) } }
}
// ---- end injected ----
"""

# The prelude is items, so it must go after any inner attributes (`#![..]`) and
# inner doc comments (`//!`), which are only legal at the very top of a file.
INNER_HEAD_RE = re.compile(r"^\s*(//!|//|/\*|\*|#!\[|$)")

ALWAYS_PANIC = ("panic", "unreachable", "todo", "unimplemented")
ASSERTS = ("assert", "assert_eq", "assert_ne",
           "debug_assert", "debug_assert_eq", "debug_assert_ne")

# An index expression needs `get_unchecked_mut` when it is written through.
# Four signals, all textual, all local to the expression:
#   1. the base already says mut     -- `self.buffer.as_mut()[..]`
#   2. `&mut ` immediately before it -- `&mut buf[..]`
#   3. an assignment after it        -- `buf[3] = x`, `buf[0] ^= 1`
#   4. a mutating method after it    -- `buf[0..3].copy_from_slice(..)`
# Guessing wrong is a compile error, which the sweep reports as a failed file;
# it cannot turn into a quietly wrong number.
MUT_HINT_RE = re.compile(r"as_mut\(\)|_mut\(|\bmut\b")
FOLLOWED_BY_ASSIGN_RE = re.compile(r"^\s*(?:[-+*/%^&|]|<<|>>)?=[^=]")
# The mutating call may sit behind a chain of plain field accesses:
# `self.sockets[h].inner.as_mut()` still needs the index to be mutable.
FOLLOWED_BY_MUT_METHOD_RE = re.compile(
    r"^\s*(?:\.\s*[A-Za-z_]\w*\s*(?!\())*"
    r"\.\s*(copy_from_slice|clone_from_slice|fill|fill_with|swap|sort|"
    r"sort_unstable|sort_by|sort_unstable_by|reverse|rotate_left|rotate_right|"
    r"iter_mut|get_mut|first_mut|last_mut|split_at_mut|make_ascii_uppercase|"
    r"make_ascii_lowercase|copy_within|write|write_all|push|clear|truncate|"
    r"as_mut|take|replace|insert|remove|extend|drain|retain|append|pop|"
    r"resize|dedup|split_off|get_or_insert|get_or_insert_with)\b"
)

IDENT_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")


def spans_to_skip(src):
    """Character ranges covered by strings, chars, comments and attributes.

    Rewrites must not touch these -- `"a[0]"` in a defmt format string is not
    an index expression, and `#[cfg(..)]` is not one either.
    """
    skip, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
            skip.append((i, j + 1)); i = j + 1
        elif c == "'" and i + 2 < n and (src[i + 2] == "'" or src[i + 1] == "\\"):
            j = src.find("'", i + 1)
            if j < 0:
                break
            skip.append((i, j + 1)); i = j + 1
        elif src.startswith("//", i):
            j = src.find("\n", i)
            j = n if j < 0 else j
            skip.append((i, j)); i = j
        elif src.startswith("/*", i):
            j = src.find("*/", i)
            j = n if j < 0 else j + 2
            skip.append((i, j)); i = j
        elif c == "#" and i + 1 < n and src[i + 1] == "[":
            j = match_bracket(src, i + 1)
            if j < 0:
                break
            skip.append((i, j + 1)); i = j + 1
        else:
            i += 1
    return skip


CONST_FN_RE = re.compile(r"\bconst\s+fn\b")
CONST_ITEM_RE = re.compile(r"\bconst\s+[A-Za-z_][A-Za-z0-9_]*\s*:")


def const_spans(src):
    """Ranges covered by `const fn` bodies and `const ITEM: T = ..;` values.

    `get_unchecked` and `unwrap_unchecked` are not const-stable, so rewriting
    inside a const context turns a panic into a compile error.  We leave those
    alone; the sites stay in the binary and the sweep reports the file as
    `partial`, which is the honest outcome -- a const-evaluated index cannot
    panic at runtime anyway.
    """
    spans = []
    for m in CONST_FN_RE.finditer(src):
        brace = src.find("{", m.end())
        if brace < 0:
            continue
        end = match_bracket(src, brace)
        if end > 0:
            spans.append((m.start(), end + 1))
    for m in CONST_ITEM_RE.finditer(src):
        depth, j = 0, m.end()
        while j < len(src):  # stop at the `;` that is not inside brackets
            if src[j] in "([{":
                depth += 1
            elif src[j] in ")]}":
                depth -= 1
            elif src[j] == ";" and depth == 0:
                break
            j += 1
        spans.append((m.start(), j + 1))
    return spans


def all_skips(src):
    return spans_to_skip(src) + const_spans(src)


def in_skip(skip, i):
    return any(a <= i < b for a, b in skip)


def match_bracket(src, i):
    """Index of the bracket closing the one at src[i]; -1 if unbalanced."""
    pairs = {"[": "]", "(": ")", "{": "}"}
    close, depth = pairs[src[i]], 0
    for j in range(i, len(src)):
        if src[j] in pairs and pairs[src[j]] == close:
            depth += 1
        elif src[j] == close:
            depth -= 1
            if depth == 0:
                return j
    return -1


def base_start(src, i):
    """Walk back from an opening `[` over the postfix expression it indexes.

    `self.buffer.as_ref()[field::SRC]` -> start of `self`.  Stops as soon as it
    sees something that cannot be part of a postfix expression.
    """
    j = i
    while j > 0:
        c = src[j - 1]
        if c in IDENT_CHARS or c in ".:":
            j -= 1
        elif c in ")]":
            k = j - 1
            depth, opener = 0, "(" if c == ")" else "["
            while k >= 0:
                if src[k] == c:
                    depth += 1
                elif src[k] == opener:
                    depth -= 1
                    if depth == 0:
                        break
                k -= 1
            if k < 0:
                break
            j = k
        else:
            break
    return j


def rewrite_macros(src, skip):
    """panic!/assert! family -> unreachable_unchecked / nothing."""
    out, counts = src, {}
    for name in ALWAYS_PANIC + ASSERTS:
        pat = re.compile(r"\b" + name + r"!\s*[\(\[\{]")
        while True:
            skip_now = all_skips(out)  # once per replacement, not per match
            m = next((c for c in pat.finditer(out)
                      if not in_skip(skip_now, c.start())), None)
            if not m:
                break
            end = match_bracket(out, m.end() - 1)
            if end < 0:
                break
            repl = ("()" if name in ASSERTS
                    else "unsafe { core::hint::unreachable_unchecked() }")
            out = out[: m.start()] + repl + out[end + 1 :]
            counts[name] = counts.get(name, 0) + 1
    return out, counts


def rewrite_unwrap(src):
    """x.unwrap() / x.expect("..") -> x.__ablate_unwrap()."""
    skip = all_skips(src)
    edits, counts = [], {"unwrap": 0, "expect": 0}
    for kind, pat in (("unwrap", r"\.unwrap\s*\("), ("expect", r"\.expect\s*\(")):
        for m in re.finditer(pat, src):
            if in_skip(skip, m.start()):
                continue
            end = match_bracket(src, m.end() - 1)
            if end < 0:
                continue
            edits.append((m.start(), end + 1, ".__ablate_unwrap()"))
            counts[kind] += 1
    for s, e, t in sorted(edits, reverse=True):
        src = src[:s] + t + src[e:]
    return src, counts


def rewrite_index(src):
    """base[idx] -> (*unsafe { base.get_unchecked[_mut](idx) })."""
    skip = all_skips(src)
    edits, count = [], 0
    for i, c in enumerate(src):
        if c != "[" or in_skip(skip, i):
            continue
        # An index expression is preceded by the end of an expression.  A `[`
        # after whitespace, `(`, `,`, `:`, `=` or `&` opens a slice/array
        # literal or a type, not an index.
        if i == 0 or src[i - 1] not in IDENT_CHARS and src[i - 1] not in ")]":
            continue
        end = match_bracket(src, i)
        if end < 0:
            continue
        start = base_start(src, i)
        base, idx = src[start:i], src[i + 1 : end]
        if not base.strip() or not idx.strip():
            continue
        after = src[end + 1 :]
        mut = (MUT_HINT_RE.search(base)
               or FOLLOWED_BY_ASSIGN_RE.match(after)
               or FOLLOWED_BY_MUT_METHOD_RE.match(after)
               or src[max(0, start - 5) : start].endswith("&mut "))
        method = "__ai_mut" if mut else "__ai"
        edits.append((start, end + 1, f"(*{base}.{method}({idx}))"))
        count += 1
    # Apply back to front so earlier offsets stay valid.  Nested indexes
    # (`a[i][j]`) overlap; keep only the outermost of any overlapping pair.
    edits.sort(key=lambda e: (e[0], -e[1]))
    applied, last_end = [], -1
    for s, e, t in edits:
        if s >= last_end:
            applied.append((s, e, t)); last_end = e
    for s, e, t in reversed(applied):
        src = src[:s] + t + src[e:]
    return src, {"index": len(applied)}


def ablate(src):
    counts = {}
    src, c = rewrite_macros(src, spans_to_skip(src)); counts.update(c)
    src, c = rewrite_unwrap(src); counts.update(c)
    src, c = rewrite_index(src); counts.update(c)
    if any(counts.get(k) for k in ("unwrap", "expect", "index")):
        lines = src.splitlines(True)
        i = 0
        while i < len(lines) and INNER_HEAD_RE.match(lines[i]):
            i += 1
        src = "".join(lines[:i]) + PRELUDE + "".join(lines[i:])
    return src, counts


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    diff = "--diff" in sys.argv
    path = args[0]
    original = open(path).read()
    new, counts = ablate(original)
    print(" ".join(f"{k}={v}" for k, v in sorted(counts.items()) if v),
          file=sys.stderr)
    if diff:
        import difflib
        sys.stdout.writelines(difflib.unified_diff(
            original.splitlines(True), new.splitlines(True), path, path + " (ablated)"))
    else:
        open(path, "w").write(new)


if __name__ == "__main__":
    main()
