# fluxopt-evaluation

Builds the nRF52840 `usb_ethernet` example twice — against upstream
embassy + xarxa, and against the `ninehusky` forks — and diffs section sizes and
panic counts. Issue: ninehusky/fluxopt-evaluation#2.

## Run

```sh
./run.py                            # upstream vs ninehusky/embassy main
./run.py --xarxa ~/research/xarxa   # against a local xarxa, uncommitted edits included
./run.py --modified-rev <sha>       # pinned to one embassy commit
```

Needs rustup toolchain `1.97` with the `thumbv7em-none-eabi` target and
`llvm-tools`, plus network access. Clones and cargo target dirs go in `./work`
(~2 GB); measurements go in `./results`. Both are gitignored — rerun to
regenerate. Re-running reuses the clones.

## What it compares

**Baseline** is upstream embassy pinned at `7c2eac8a`, the commit
`ninehusky/embassy` branched from; that commit pins its own xarxa as a git
dependency. **Modified** is `ninehusky/embassy` `main`, resolved fresh on every
run, which pins `ninehusky/xarxa` as the `third_party/xarxa` submodule.

Baseline is pinned and modified floats on purpose: holding the fork point fixed
is what makes the delta attributable to the fork, and nothing here has to be
edited when the fork moves. Both resolved SHAs are written to
`results/refs.txt`. `--xarxa` is the one way to override the submodule; it flags
the checkout dirty in `refs.txt` if you have uncommitted edits.

Both repos ask for toolchain `1.97` and set `[profile.release] debug = 2`, so
the two builds run the same command with the same profile.

## Reading the results

`results/RESULTS.md` is the table; `results/*.json` has everything behind it.

**Sizes.** `total_flash` is what gets programmed onto the device. `total_ram` is
`.data + .bss + .uninit`. `total_elf` is the whole file including DWARF, which
`debug = 2` makes ~45× the firmware — it is reported only so the `Total` row in
`llvm-size -A` is not mistaken for the firmware size.

**Panics.** A *panic call site* is a branch into one of core's panic entry
points from code that is not itself panic machinery; that is the number to
compare across builds. A *panicking function* is a function containing at least
one such branch — call-graph depth 1, not everything that can reach a panic.

Compare builds using `panic_sites_by_crate`. The panicking-function *lists* move
around between builds because inlining decides which symbol holds a given
branch, so a function appearing on one side only is usually the same panic
attributed elsewhere, not one added or removed.

`unmatched_panic_refs` is a coverage check and should be `[]`. If it is not,
some instruction reaches a panic in a way the site count missed — an indirect
call, a linker veneer — and the count is an undercount. The JSON and the
comparison table both say so rather than being quietly wrong.

To check a classification by hand:

```sh
column -t -s $'\t' results/modified.panic-call-sites.txt   # address, caller, panic symbol
jq '.panic_targets' results/modified.json                  # which panic symbols matched
llvm-nm --demangle <elf> | grep -iE 'panic|unwind|_fail'   # is PANIC_RE still complete?
```

Each row of `panic-call-sites.txt` is one instruction, in the direction
caller → callee, findable at that address in `llvm-objdump -d --demangle`.

## Caveats

* The `.text` delta is small (−504 B) largely because 307 of the ~660 sites are
* The modified example additionally depends on `flux-rs` and sets
  `[package.metadata.flux]`. Plain `cargo build` does not run Flux and the
  attributes expand to nothing, but it is a real difference between the two
  `Cargo.toml`s.
* One build per side, no determinism check here. `sweep.py` does one.

## Per-file ablation: which files are worth verifying

`./sweep.py` answers a different question: for each xarxa source file, how many
bytes of `usb_ethernet` would disappear if that file could not panic at all? It
measures rather than estimates — it rewrites the file's panicking constructs
into unchecked equivalents, rebuilds the real binary, and diffs `.text`.

```sh
./run.py                        # once, to create work/modified
./sweep.py                      # every xarxa file owning >= 1 panic site
./sweep.py src/wire/ipv4.rs     # or just one
```

Results land in `results/per-file-wins.tsv`, tabulated in
`results/PER-FILE-WINS.md` and `results/PER-FILE-WINS-trimmed.md`.

### Reading them

Every number is a **ceiling, not a forecast**. `get_unchecked` removes every
check in the file; Flux will discharge some fraction of them. This ranks
targets, it does not predict the payoff.

Rank by bytes per *distinct source line*, not per site. Sites count
monomorphized copies — `socket_set.rs` has 28 sites across 9 lines — and
verification effort scales with lines.

Deltas do not sum. Two files that each empty part of the same panic bucket will
both claim the machinery that dies when it empties.

Small deltas are noise. Removing checks shifts inlining, so `.text` can move by
more than the panic paths involved, occasionally the wrong way. The sweep
reports the largest increase it saw; treat anything under that as unresolved.

A `partial(n/m left)` status means the rewrite did not actually remove that
file's sites, so the delta does not mean what the row says — usually `const fn`
bodies, which are skipped because `get_unchecked` is not const-stable.
`build-failed` means the mutable-vs-shared guess was wrong. Neither is reported
as a small win. The sweep also confirms determinism before ablating anything,
and restores the checkout between files, including on Ctrl-C.

### The feature flag, which is bigger than all of them

`examples/nrf52840` asks embassy-net for `medium-ieee802154`, because other bins
in that package need it and cargo unifies features per package. So
`usb_ethernet` — a CDC-NCM device that only speaks Ethernet — links the whole
6LoWPAN and 802.15.4 stack.

| | as shipped | feature dropped | delta |
| --- | --- | --- | --- |
| `.text` | 137620 | 117724 | **-19896 (-14.5%)** |
| panic call sites | 657 | 496 | -161 |

No verification involved, and more than twice the total prize from verifying
xarxa in this binary. It does not make the verification pointless — it means the
`sixlowpan/*` and `ieee802154` rows are wins against code a product build would
not ship, so they rank last. `PER-FILE-WINS-trimmed.md` repeats the sweep
without the feature for that reason.

### What to audit

`ablate.py` is the only component that edits code; everything else reads tool
output. Read its rule list, then for any row you intend to act on:

```sh
python3 ablate.py --diff work/modified/third_party/xarxa/src/wire/icmpv6.rs
```

The rewrite is deliberately **unsound** — `get_unchecked` on an index nothing
proved in range is UB. These binaries are measured with `llvm-size` and never
flashed.
