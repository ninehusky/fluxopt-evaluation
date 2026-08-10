# fluxopt-evaluation

Does the Flux-refined `xarxa` make the `usb_ethernet` firmware smaller, and
does it remove panics?  This repo builds that one example twice and diffs the
two ELFs.  Issue: ninehusky/fluxopt-evaluation#2.

## Run it

```sh
./run.sh
```

Needs `rustup` toolchain `1.97` with the `thumbv7em-none-eabi` target and the
`llvm-tools` component, plus network access (both builds fetch crates).
Clones and cargo target dirs go in `./work` (gitignored, ~2 GB); results go in
`./results`.  Re-running reuses the clones.

## What is compared

| | embassy | xarxa |
| --- | --- | --- |
| baseline | `embassy-rs/embassy` @ `7c2eac8a1450dbfbcc138a03c79aef4b880aff7b` | `embassy-rs/xarxa` @ `1f332ac32cc33d86aefc8e1c1a9749b93234a6de` |
| modified | `ninehusky/embassy` @ `460e274e50c0d799eceedd8e6192f31f6ded5c35` (main) | `ninehusky/xarxa` @ `f42ae2866a63f32b3230a8dc24c95f209ccc22ad` |

Why those refs:

* Baseline embassy is the commit `ninehusky/embassy` forked from, not upstream
  `main`.  Upstream main moves; the fork point holds everything else fixed so
  the delta is attributable to the fork.
* Baseline xarxa is not chosen by this repo at all.  Upstream embassy's
  `embassy-net/Cargo.toml` pins it as a git dependency at that rev, and cargo
  fetches it.
* Modified xarxa is likewise not chosen here: `ninehusky/embassy` main records
  it as the `third_party/xarxa` submodule pin, and `git submodule update
  --init` checks it out.  That commit is the head of the fork's
  `remove-explicit-panics` branch (the current no-panic work), which has also
  been merged to that fork's `main`.

Both repos already ask for toolchain `1.97` and both set
`[profile.release] debug = 2`, so the build is byte-for-byte the same recipe on
both sides:

```sh
cd examples/nrf52840 && CARGO_INCREMENTAL=0 cargo +1.97 build --release \
    --bin usb_ethernet --target thumbv7em-none-eabi
```

## How the numbers are produced

`measure.py <elf> <prefix>` shells out to exactly two commands, both from the
1.97 toolchain's `llvm-tools`:

```sh
llvm-size -A <elf>
llvm-objdump -d --demangle <elf>
```

Definitions, all implemented in ~30 lines of `measure.py`:

* **panic symbol** — a function symbol on the explicit list in `PANIC_RE`:
  `core::panicking::*`, `core::cell::panic_already_*`,
  `core::{option,result}::{unwrap_failed,expect_failed}`,
  `core::slice::index::slice_index_fail`,
  `core::slice::copy_from_slice_impl::len_mismatch_fail`, the
  `#[panic_handler]` `rust_begin_unwind`, `_defmt_panic`, `panic_probe::*`.
  It is a list and not a match on the substring "panic" because several entry
  points do not contain the word (`unwrap_failed`, `slice_index_fail`) while
  ordinary library code does — xarxa's `HardwareAddress::ethernet_or_panic` is
  a normal function that happens to panic, not part of the machinery.  To
  check the list is still complete for an ELF:
  `llvm-nm --demangle <elf> | grep -iE 'panic|unwind|_fail'`.
* **panic call site** — one branch instruction whose target is a panic symbol,
  where the function containing the branch is *not* itself a panic symbol.
  The exclusion is what makes the number mean "places ordinary code can enter a
  panic" rather than "size of the panic machinery" — otherwise
  `core::panicking::panic` → `panic_fmt` → `rust_begin_unwind` would count.
  `bl`, plain `b`, and conditional branches all count, because `-O` turns most
  panic calls into tail branches.
* **panicking function** — a function containing at least one panic call site,
  counted once regardless of how many.  A wrapper like `ethernet_or_panic`
  lands here, via the branch to `core::panicking::panic` inside it.

To audit the classification, read the dumps:

```sh
column -t -s $'\t' results/modified.panic-call-sites.txt   # caller -> panic symbol, one per line
cat results/modified.panicking-functions.txt
cat results/modified.sections.txt                          # raw llvm-size -A
jq '.panic_targets' results/modified.json                  # which panic symbols got matched
```

Every line in `panic-call-sites.txt` corresponds to one instruction you can
find in `llvm-objdump -d --demangle` output.

## Results

See [results/RESULTS.md](results/RESULTS.md) for the table and
[results/refs.txt](results/refs.txt) for the exact SHAs of the run that
produced it.

## Caveats

* Only allocated sections are in the table.  Both builds carry `debug = 2`, so
  `.debug_*` dominates the raw `llvm-size -A` output and is noise for this
  question; it is still in `results/*.sections.txt` and the JSON.
* The modified example additionally depends on `flux-rs` (the attribute crate)
  and sets `[package.metadata.flux]`.  Plain `cargo build` does not run Flux
  and the attributes expand to nothing, so this should not move the numbers —
  but it is a real difference between the two `Cargo.toml`s.
* The fork's embassy-net was ported to xarxa's refined `EthernetAddress` API,
  so the delta covers both the xarxa changes and that port, not xarxa alone.
* Panic classification is name-based.  A panicking path reached through a
  function pointer or an indirect branch is not counted; a symbol that merely
  has "panic" in its name would be.  The dumps exist so both cases are visible.
* The panicking-function *counts* are over raw symbols, but the added/removed
  *lists* strip LLVM's ` (.llvm.<hash>)` suffix, which differs between the two
  builds for the same function.  Without that, a dozen unchanged functions look
  simultaneously added and removed.
* `core::slice::index::slice_index_fail` accounts for 307 of the ~660 call
  sites and is identical on both sides, so most of what is left is slice
  indexing that this work did not target.  `jq '.panic_targets'` on either JSON
  breaks the total down by panic entry point.
* One build each, no rebuild-for-determinism check.  Rust builds of the same
  sources with the same toolchain are stable enough for section sizes, but
  nothing here proves it.
