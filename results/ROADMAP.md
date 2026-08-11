# Roadmap: getting `usb_ethernet` to zero panic sites

Hand-written. The generated companion is [STATUS.md](STATUS.md) (`./status.py`),
which tracks where we actually are; this file says where we are going and in what
order. Numbers here are measured 2026-08-11 unless marked otherwise.

## Definition of done

`panic_call_sites == 0` and `unmatched_panic_refs == []` in `results/modified.json`
for the linked nRF52840 `usb_ethernet` binary. Both already come out of
`measure.py`, so the goal is machine-checkable and needs no new tooling. At zero
the `#[panic_handler]` is unreferenced and the linker drops it, which is the
observable end state.

**Zero is not reachable by working on xarxa.** This is the single most important
planning fact and nothing before today said it out loud.

## Where the 650 sites actually live

| crate | sites | share | reachable by xarxa proofs? |
| --- | ---: | ---: | --- |
| xarxa | 439 | 67.5% | yes — 386 of them |
| embassy-usb | 50 | 7.7% | no |
| core | 35 | 5.4% | no |
| defmt | 25 | 3.8% | no |
| embassy-nrf | 21 | 3.2% | no |
| embassy-sync | 19 | 2.9% | no |
| embassy-net-driver-channel | 17 | 2.6% | no |
| embassy-net | 11 | 1.7% | no |
| embassy-usb-driver | 9 | 1.4% | no |
| nrf-pac, heapless, defmt-rtt, embedded-io-async, byteorder, the example | 24 | 3.7% | no |

Measured: ablating **every** ablatable xarxa panic takes the binary from 650 to
**244** sites (flash -24216 B, -15.58%). So the entire xarxa programme — every
phase below through phase 4 — is worth 62% of the goal, and the last 38% is work
nobody has started or scoped.

## The phases

Ordered by dependency, not by size. Each has an exit criterion that is a number.

### Phase 0 — xarxa CHURN (172 sites) · IN FLIGHT

Ordinary refinement: state a length or range precondition, discharge it, follow it
to the callers. Four agents are on `udp.rs`, `ipv4.rs`, `ndiscoption.rs`,
`sixlowpan/nhc.rs`. Remaining churn files after those: `ipv6.rs` (22),
`icmpv6.rs` (18), `ndisc.rs` (12), `ethernet.rs` (7), `ipv6option.rs` (6),
`mld.rs` (6), plus a long tail.

Fully delegable — this is what agents are for. **Exit: churn count 172 → 0.**

### Phase 1 — close the attribution gap (86 + 53 sites) · DO THIS NEXT

Two blind spots that overlap, and together they are bigger than the PANIC bucket:

- **86 UNATTRIBUTED sites.** The blame data places them in a file but they fall
  outside any function the triage parser recognises — macro bodies, derives,
  closures. They count in the metric and have no Flux obligation attached, so they
  are invisible to every plan we have. `sixlowpan/iphc.rs` is 37 of them.
- **53 sites survive full `get_unchecked` ablation.** Even the unsound mechanical
  rewrite cannot remove them. 20 are in `iphc.rs`, 4 each in `wire/mod.rs`,
  `ipv6.rs`, `ieee802154.rs`. Known causes so far: `const fn` bodies the rewriter
  skips, `[u8; N]` arrays (the ablator's index trait covers `[T]` only), and
  `assembler.rs` borrowck conflicts.

Neither is proof work — it is diagnosis, and it is cheap. Until it is done we
cannot say what the xarxa endgame costs, and `iphc.rs` (49 sites, the largest file
in the crate) cannot be planned at all.

**Exit: every one of the 439 xarxa sites carries a category, and the 53 residue
has a named cause per site.**

### Phase 2 — xarxa PANIC (105 sites)

Explicit `panic!` / `unreachable!` / `assert!` / `expect`. Not more refinement
typing: each needs a *reachability* argument, and the fact that makes the branch
dead usually lives in another module. 60 of the 105 sit in three files:

| file | sites | the invariant to choose |
| --- | ---: | --- |
| `iface/socket_set.rs` | 28 | does a live `SocketHandle` always index an occupied slot? |
| `wire/tcp.rs` | 20 | arithmetic preconditions on `TcpSeqNumber` add/sub |
| `iface/packet.rs` | 12 | narrowing the packet enum by facts set elsewhere |

Each is one human decision followed by delegable mechanical work, and each
balloons scope in the way already flagged: an invariant on a type means
un-trusting everywhere that constructs it. **Blocked on three decisions, not on
effort.** Two cheap outliers need no decision at all — `ipv6.rs:163`
`assert!(mask <= 128)` and `neighbor.rs:150` `assert!(protocol_addr.is_unicast())`
are ordinary argument preconditions, 2 sites each.

**Exit: panic count 105 → 0.**

### Phase 3 — xarxa CORE (52 sites)

Iterator / `Option` / `Result` chains Flux cannot see through:
`MightPanic(Transitive | NotInCallGraph | UnresolvedCall)`. Same shape as the
`byteorder` work already landed in PR #14 — copy the needed specs from
`flux/lib/flux-core/src/` into `flux_specs.rs`, one dependency closure at a time.
Do NOT try to load flux-core wholesale; that route is broken in `cargo-flux` and
was deliberately abandoned.

Mostly delegable once the first few specs establish the pattern.
**Exit: core count 52 → 0.**

### Phase 4 — compiler work (19 sites + one blocker)

- **FLUXBUG, 12 sites.** `internal flux error: flux-infer/src/infer.rs:888`, in
  `ring_buffer.rs` and `packet_buffer.rs`.
- **ICE, 7 sites.** All in `iface/interface/mod.rs`. ICE 1
  (`place_ty.rs:112 cannot unfold in NoUnfold mode`) is not fixable as a bug — it
  needs subtyping for blocked locations, a language feature.
- **The `<&T as AsRef<[u8]>>::idx` gap.** Not a site count, but it gates
  `payload()` in 16 wire files (13 churn sites). ICE-2 made the signature
  statable; it still does not discharge.

Not delegable. **Exit: no `panicked` in any log, and `payload()` provable.**

### Phase 5 — the logging and formatting tranche (~60 sites)

`defmt` 25 + `defmt-rtt` 5 + the ~30 core sites in `fmt/num.rs` and `int_log10.rs`
are integer-formatting and logging machinery. **These are not proof targets.**
They disappear if `defmt` logging is compiled out of the example, and no amount of
verification will touch them otherwise.

That makes this a decision about what the benchmark is allowed to be, not an
engineering task, and it should be taken deliberately rather than discovered at
the end: is a firmware that still formats log messages a fair subject, or does the
evaluation build without `defmt`? Roughly 9% of all sites ride on the answer.

**Exit: a decision, recorded here.**

### Phase 6 — the embassy crates (~127 sites)

`embassy-usb` 50, `embassy-nrf` 21, `embassy-sync` 19,
`embassy-net-driver-channel` 17, `embassy-net` 11, `embassy-usb-driver` 9. All
live in `ninehusky/embassy`, a fork we control, so the same
`default_trusted = true` + opt-in method applies. Nothing has been scoped here.

Expect it to be harder than xarxa, not easier: this is async executors, USB state
machines and channel internals rather than byte-slice parsing, and Flux's story
for `async fn` and self-referential state machines is much weaker than for wire
formats.

**Exit: 127 → 0, or a written argument for why some are out of scope.**

## The strategic question this exposes

The phases above are ordered so that the cheap, delegable, well-understood work
runs first — but they add up to a research programme, not a sprint, and phases 5
and 6 are qualitatively different from 0–4.

So it is worth asking explicitly, before phase 2 commits anyone to type
invariants: **is zero the goal, or is the goal a defensible measurement?** This
repo is an evaluation. A result of the form "Flux discharges N% of panic sites in
a real network stack, at a cost of M annotations, for a K% flash saving" may be
the actual deliverable, in which case phases 0–3 are the whole story and 5–6 are
scope to be argued away rather than work to be done.

That choice changes what phase 2 is worth doing at all. It should be made
deliberately.
