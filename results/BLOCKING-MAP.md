# Blocking map — xarxa panic sites

439 panic call sites in the linked `usb_ethernet` firmware are in xarxa. This maps each to what
stands between it and a discharged proof.

**Headline.** `Cargo.toml` sets `default_trusted = true`. **376 / 439 sites (86%) are inside bodies
Flux never looks at.** No ICE, no expressiveness limit, no missing spec is stopping them — nobody
has written `#[flux_rs::trusted(no)]` on the function. The 44–54 error counts are *not* a measure of
outstanding panic obligations; they are the residue of the ~50–70 functions opted in so far.

## Verified vs inferred

VERIFIED BY RUNNING (all four logs grepped for `panicked`, count 0 in every one):

| run | errors | `panicked` |
| --- | --- | --- |
| `xarxa-ringbuf` @5275c30 | 48 | 0 |
| `xarxa-icmpv6` @cd73b8f | 54 | 0 |
| `xarxa-socketset` @155a5b5 | 51 | 0 |
| `work/modified/third_party/xarxa` @460e274 | 44 | 0 |

Command: the one in the brief, per worktree. Also verified: the 24-error intersection across the
three worktrees, each worktree's delta, the `trusted(no)` opt-in set per worktree, and the
site→enclosing-function attribution (439/439 blame rows attributed; 81 have no DWARF line and were
resolved by address against `modified.panic-call-sites.txt`, 44 of which have no entry there either
and fall back to file-level blame).

INFERRED BY READING: everything about sites in the 376 not-attempted bucket — no obligation has
ever been generated for them, so their blockers are extrapolated from the three worktrees that
attempted structurally identical code.

## Table

`disch.` = discharged in at least one worktree. `open` = obligation exists and fails.
`none` = default-trusted, no obligation generated.

| file | sites | disch. | open | none | blocker on the remainder | why |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| wire/sixlowpan/iphc.rs | 49 | 0 | 0 | 49 | **B0** not attempted | all 49 land in `Repr::parse`/`emit` after inlining; the `Packet<&T>::payload` piece is **B2** |
| wire/tcp.rs | 34 | 0 | 0 | 34 | **B0**; 14 of them `SeqNumber` arith | `add`/`sub` overflow panics (14 sites) need modular `SeqNumber` order axiomatised → **B6** |
| wire/ipv6.rs | 33 | 0 | 0 | 33 | **B0** | pure `set_*` accessor work; the icmpv6 recipe applies verbatim |
| iface/socket_set.rs | 28 | 9 | 19 | 0 | **B3** ×17, **B6** ×2 | `expect`/`None` arms need per-element facts; `add`'s full-set panic is reachable |
| wire/icmpv6.rs | 26 | 13 | 0 | 13 | **B2** ×5, **B0** ×8 | 13 discharge locally but export 19 preconditions to `ndisc::Repr::emit` (**B4-in-crate**); `payload` is **B2** |
| wire/sixlowpan/nhc.rs | 25 | 0 | 0 | 25 | **B0**; 5 are **B2** | two `Packet<&T>::payload` impls |
| wire/ipv4.rs | 21 | 0 | 0 | 21 | **B0** | `set_*` accessors + `Repr::emit` |
| storage/ring_buffer.rs | 20 | 20 | 0 | 0 | — **done** | all 20 verify in `xarxa-ringbuf`; the 10 residual errors there are at other lines |
| wire/ieee802154.rs | 18 | 0 | 0 | 18 | **B0** | 10 have no DWARF line; `Frame<&T>` accessors are **B2** |
| wire/udp.rs | 18 | 0 | 0 | 18 | **B0** | `set_*` accessors |
| wire/mld.rs | 18 | 0 | 0 | 18 | **B0** | `set_*` accessors; `Repr::emit` also hits `in_bounds` assoc-refinement gap |
| iface/interface/sixlowpan.rs | 16 | 0 | 0 | 16 | **B0** | caller-side length arithmetic on `tx_buf`; genuinely new refinement work |
| wire/ndisc.rs | 16 | 0 | 1 | 15 | **B0**; `emit` is **B4-in-crate** | `Repr::emit` already carries 3 baseline + 19 icmpv6-induced errors |
| wire/ndiscoption.rs | 13 | 0 | 0 | 13 | **B0** | `set_*` accessors |
| iface/packet.rs | 12 | 0 | 0 | 12 | **B0**; 6 `unreachable!()` | the `unreachable!` arms need feature-gated enum reasoning, not lengths |
| wire/sixlowpan/mod.rs | 10 | 0 | 0 | 10 | **B0** | `copy_from_slice` on fixed arrays |
| wire/arp.rs | 9 | 0 | 0 | 9 | **B0** | 9 distinct `set_*`, all one-liners |
| socket/tcp.rs | 8 | 0 | 0 | 8 | **B0**, **B6** | `process` needs a Socket-level window↔`rx_buffer` invariant |
| wire/icmpv4.rs | 8 | 0 | 0 | 8 | **B0** | `set_*` accessors |
| iface/interface/mod.rs | 7 | 0 | 1 | 6 | **B0**, **B1** | `socket_egress` hits ICE `infer.rs:888` in every worktree |
| wire/ethernet.rs | 7 | 0 | 0 | 7 | **B0** | `set_src_addr`/`set_ethertype` |
| wire/ipv6option.rs | 7 | 0 | 0 | 7 | **B0** | `data_mut` + `set_data_len` |
| storage/packet_buffer.rs | 5 | 0 | 0 | 5 | **B0** | `metadata.header.unwrap()` is **B3**-shaped (per-element `Some`) |
| wire/mod.rs | 4 | 0 | 0 | 4 | **B0** | `ethernet_or_panic` — needs the `HardwareAddress[true]` index already in the base |
| iface/neighbor.rs | 4 | 0 | 0 | 4 | **B0** | heapless map `remove().unwrap()` — **B3**-shaped |
| wire/ip.rs | 4 | 0 | 0 | 4 | **B0** | one `unreachable!()` ×4 in `pseudo_header` |
| wire/dhcpv4.rs | 4 | 0 | 0 | 4 | **B0** | `set_*` accessors |
| socket/dhcpv4.rs | 3 | 0 | 0 | 3 | **B0** | 2 are `panic!("non-ethernet hardware address")` — needs the `HardwareAddress` index |
| iface/interface/ipv6.rs | 3 | 0 | 0 | 3 | **B0** | |
| wire/ipv6hbh.rs | 2 | 0 | 0 | 2 | **B0** | |
| wire/ipv6ext_header.rs | 2 | 0 | 0 | 2 | **B0** | |
| iface/route.rs | 2 | 0 | 0 | 2 | **B0** | `max_by_key` unwrap — **B5** (iterator adapter spec) |
| phy/mod.rs | 1 | 0 | 0 | 1 | **B0** | |
| storage/assembler.rs | 1 | 0 | 0 | 1 | **B0** | |
| socket/udp.rs | 1 | 0 | 1 | 0 | **B5** | `copy_from_slice` MightPanic(Transitive) |
| **total** | **439** | **42** | **22** | **375** | | |

## Ranked blockers — sites gated

| rank | blocker | sites gated | evidence |
| ---: | --- | ---: | --- |
| 1 | **B0 — body is `default_trusted`; no obligation generated** | **375** | `Cargo.toml:44 default_trusted = true`; only 49–69 functions carry `trusted(no)` per worktree, covering 63 sites |
| 2 | **B3 — slices refined by length only** | **17** (+~10 inferred) | `socket_set.rs` `expect`/`None` arms: 8 need "slot is `T`", 9 need "`inner` is `Some`". Same shape in `packet_buffer.rs` (3) and `neighbor.rs` (2) |
| 3 | **B2 — ICE naming a reference type in a qualified refinement path** | **~16 directly** | `struct_compat.rs:154`. 13 wire types define `payload`/`options`/`data` in an `impl<'a, T: AsRef<[u8]> + ?Sized> X<&'a T>` block; `xarxa-icmpv6` left `icmpv6::Packet::payload` trusted for exactly this (source comment at `xarxa-icmpv6/src/wire/icmpv6.rs:517-522`) |
| 4 | **B6 — needs a semantic/API change** | **~16** | 14 `SeqNumber` add/sub overflow panics (`wire/tcp.rs:44,55,73`), 2 `add()` full-`SocketSet` panics. Also the closure-return bound in `ring_buffer` (blocks invariant *maintenance*, not any of the 20 sites) |
| 5 | **B1 — ICE `ensures` + return borrowing out of `self`** | **1 site** (7 non-site errors) | `infer.rs:888` at `iface/interface/mod.rs:727` in all three worktrees; 7 "assignment might be unsafe" in `ring_buffer`. Gates invariant *maintenance*, not the panic sites — all 20 ring_buffer sites discharged around it |
| 6 | **B5 — missing extern specs** | **1 site** (~12 non-site errors) | `socket/udp.rs:643` `copy_from_slice`. The `byteorder` half is **solved**, not blocked — see corrections |
| 7 | **B4 — obligation exits the crate** | **0 sites today** | see corrections |

Ranks 2–7 together gate **~51 sites**. B0 gates **375**. That is the plan-changing number: the
bottleneck is unwritten annotations, not tool limits.

## Sites blocked by nothing known — the available work

These are the highest-fan-in cones, by post-inlining calling symbol (`modified.panic-call-sites.txt`).
Proving a cone's `buffer_len()` contract retires its whole column. The `xarxa-icmpv6` worktree proved
the recipe works (refine `Packet<T>` by `buf`, add `AsRef::idx`, `requires idx(buf) >= N`) — it
discharged 13 sites with no ICE and no expressiveness wall.

| fan-in cone | sites | note |
| --- | ---: | --- |
| `iphc::Repr::parse` | 41 | single largest cone in the crate |
| `ipv4::Repr::emit` | 18 | |
| `ipv6::Repr::emit` | 17 | |
| `mld::Repr::emit` | 16 | |
| `ndisc::Repr::emit` | 15 | already has 3 baseline errors; icmpv6's work added 19 more here |
| `nhc::UdpNhcRepr::emit` | 12 | |
| `icmpv6::Repr::emit` | 11 | |
| `tcp::Repr::emit` | 10 | |
| `arp::Repr::emit` | 9 | 9 one-line `set_*`, no shared state |
| `InterfaceInner::process_ieee802154` | 9 | |
| `InterfaceInner::ipv6_to_sixlowpan` | 9 | |
| `icmpv4::Repr::emit` | 8 | |

**Cheapest first real target: `wire/arp.rs` (9 sites).** Nine independent one-line `set_*` accessors,
one `Repr::emit` caller, no `&T` accessor, no iterator, no closure. It is the icmpv6 recipe with none
of the complications.

**Caveat on the recipe.** `xarxa-icmpv6` went 44 → 54 errors: it discharged 13 icmpv6 sites and 9
baseline errors but *created* 19 new `refinement type error`s in `ndisc::Repr::emit`, all of them the
callee `requires` now unmet at the call site. Adding `requires` to accessors moves the obligation up
the cone; it does not retire it until the cone's root is proven too. Budget for that.

## Corrections to the stated categories

1. **B4 "obligation exits the crate" is not the blocker it was described as — and the correction to
   the previous correction is that embassy-net is *also* not checked today.**
   `embassy-net/Cargo.toml:143` does set `enabled = true` with no `no_panic` and no `default_trusted`,
   so its bodies would be checked and any `requires` on a xarxa function *would* be discharged there
   — preconditions are checked independently of `no_panic`. But VERIFIED: `cargo flux check` from
   `work/modified/embassy-net` never reaches embassy-net. It checks the `xarxa` dependency first,
   fails with 44 errors, and cargo halts. Retried with `--keep-going`: same, zero diagnostics in any
   `embassy-net/src/*` file, 0 `panicked`. So today the `requires h < len` on `SocketSet::get`
   records an obligation that **nothing checks** — not because Flux is absent from embassy-net, but
   because embassy-net is downstream of a crate that does not verify. This unblocks itself the
   moment xarxa is clean; it is not a category that needs separate work.
2. **`byteorder` is solved, not blocked.** Category 5 lists `byteorder::write_u16/u32` as
   `MightPanic(NoMIRAvailable)` that "flux-core will never cover". `xarxa-icmpv6` wrote the spec
   locally in `src/flux_specs.rs` (its bodies are all `buf[..N]`, so `requires n >= N` is the whole
   panic condition) and the three `write_u16/u32` errors are gone from that run. It is a solved
   problem to be copied forward, not a blocker.
3. **B1 does not gate any panic site.** It gates invariant *maintenance*, which is a different
   deliverable. `xarxa-ringbuf` discharged all 20 `ring_buffer.rs` panic sites while the ICE was
   live; the 7 "assignment might be unsafe" it leaves behind are at `self.length += …` lines, none
   of which is a panic site. Counting B1 as a panic-site blocker overstates it by 20.
4. **B3's count in `socket_set.rs` is 17, not 19.** 8 `expect` ("slot is a `T`") + 9 `None => panic!`
   ("`inner` is `Some`"). The other 2 of the quoted 19 are `add`'s full-set panic, which is B6 — a
   different fix. 9 of the file's 28 sites *are* discharged (the three `sockets[handle.0]` bounds
   checks, which monomorphise to 1 + 7 + 1).
5. **A category is missing: `unreachable!()` on feature-gated enum variants.** `iface/packet.rs` (6),
   `wire/ip.rs` (4), `iface/interface/mod.rs` (2), `iface/interface/sixlowpan.rs` (2),
   `socket/tcp.rs` (1) — 15 sites where the arm is dead because a Cargo feature is off, not because
   of any length or element fact. Neither a length refinement nor an extern spec touches these; they
   need the enum indexed by variant. Cheap and entirely unstarted.
