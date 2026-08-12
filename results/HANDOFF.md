# Handoff: state at the end of 2026-08-11

Everything below is **local** unless marked PUSHED. Nothing was merged.

## The one thing to do first

`flux-specs-slice-index` is **2 commits ahead of its remote**, so
[PR #14](https://github.com/ninehusky/xarxa/pull/14) does not contain the promoted
specs (`05f1967` idx machinery + `Result::is_ok`, `5b5a8fc` `RangeFull` +
`cmp::min`). Every other branch depends on them. Push or the PR misrepresents the
base.

## xarxa branches

Base lineage: `3f51d2f` → `05f1967` → `5b5a8fc` (= `flux-specs-slice-index` HEAD)
→ `cfba148` (= `flux-integration`, 8 branches merged) → `cde95bc`.

| branch | worktree | contains | in integration? |
| --- | --- | --- | --- |
| `flux-specs-slice-index` | `xarxa-specs` | the shared spec base | base — **PUSHED, 2 behind** |
| `flux-integration` | `xarxa-integ` | 8 branches + the `From` fix | — |
| `flux-ndiscoption` | `xarxa-ndiscoption` | 7 sites | yes |
| `flux-udp` | `xarxa-udp` | 13 sites | yes |
| `flux-ethernet` | `xarxa-ethernet` | ethernet 7, ipv6option 2 | yes |
| `flux-ipv6` | `xarxa-ipv6` | 32 sites | yes |
| `flux-icmpv6b` | `xarxa-icmpv6b` | icmpv6 16, ndisc 10 | yes |
| `flux-mld` | `xarxa-mld` | mld 6, icmpv4 4 | yes |
| `flux-ipv4` | `xarxa-ipv4` | 18 sites | **NO — conflicts** |
| `flux-nhc` | `xarxa-nhc` | 7 sites | **NO — conflicts** |
| `flux-iphc` | `xarxa-iphc` | **47 sites**, biggest single win | no (based on `cfba148`) |
| `flux-arp2` | `xarxa-arp2` | arp 5, ipv6ext 2, dhcpv4 1 | no (based on `cfba148`) |
| `flux-ipemit` | `xarxa-ipemit` | `ip::Repr::emit` proven | no (based on `cfba148`) |
| `flux-emitcone` | `xarxa-emitcone` | nothing — negative result | no |
| `flux-txtoken` | `xarxa-txtoken` | nothing — negative result | no |

`flux-ipv4` and `flux-nhc` are the only real merge work: they sit on `3f51d2f`
and conflict on `flux_specs.rs`, `icmpv4.rs`, `icmpv6.rs`. The conflicts are
duplicated spec blocks that are now on the base — resolve by taking the base
side. The other four unmerged branches are already based on `cfba148` and merge
clean.

Recommended merge order: `flux-iphc`, `flux-arp2`, `flux-ipemit`, then rebase
`flux-ipv4` and `flux-nhc` onto `cde95bc` rather than merging them.

`xarxa`, `xarxa-arp`, `xarxa-icmpv6`, `xarxa-ringbuf`, `xarxa-socketset`,
`xarxa-triage*` are pre-existing and were not touched (except reading `arp`/`icmpv6`
as templates).

## Other repos

- **`fluxopt-evaluation`**: 13 unpushed commits on `proof-completeness-check`.
  **`blame.py` is UNTRACKED** — it was rewritten on 2026-08-11 at 14:58 to attribute
  from `core::panic::Location` instead of the DWARF inline stack, which moved 14
  sites between crates (xarxa 439 → 453). That change is in no commit. Track it.
- **`flux`**: branch `ice2-on-wip`, 44 ahead of `origin/main`, **never pushed** —
  `flux-rs/flux` is not a write target. The top 3 commits are this session's:
  ICE-2 (region hole in `AliasReft` args), `match_clauses` region erasure, and
  `enter_exists` reporting an unsolved evar instead of ICEing.

## To run agents against `dispatch_ip`

The installed `~/.flux` is stock and **ICEs on `dispatch_ip`**. A patched sysroot
is at **`~/.flux-ice3`**. Every agent touching `iface/interface/mod.rs` must use:

    FLUX_SYSROOT=$HOME/.flux-ice3 cargo flux check -p xarxa --no-default-features \
      --features "defmt,socket-tcp,proto-ipv4,medium-ethernet,socket-dhcpv4,socket-udp,medium-ieee802154,proto-ipv6,auto-icmp-echo-reply,async"

That feature set is what the firmware builds with; do not change it.

## Where the bubbling-up work actually stands

| chain | state |
| --- | --- |
| **ingress / parse** | **no blocker.** `check_len` → `match` (not `?`) → `Repr::parse` → `process_*` → `poll` all checkable. `ndisc.rs` already reports 0 absorbed. |
| **IP emit** | proven up to `dispatch_ip`. Blocked there by two things: `dispatch_ip`'s obligations sit in **let-bound closures, whose bodies are not checked**, and `<T as AsMut<[u8]>>::idx` is **never grounded** at any call site. |
| **ethernet emit** | blocked at `TxToken::consume` — refining a closure bound whose argument is a reference needs HRTB, absent from Flux surface. |

**Start the new session on ingress.** It is the only chain that can reach
end-to-end today, and `cone.py` will tell you when it has.

## The one Flux gap that dominates everything

`extern_spec` cannot name the `&T` / `&mut T` blanket impl (`E0106` on the elided
lifetime, `E0277`/`E0637` on `?Sized`, or "generic parameters don't match the
external implementation" against core's `PointeeSized` blanket). Verified from
three directions. That single gap blocks: `payload()` in 16 wire files, `nhc`'s
unit-sort erasure, `TxToken::consume`, and the grounding of every emit-path
length. Nothing in xarxa routes around it.

## Traps that cost time yesterday — brief the agents

1. `?` drops a refinement; an explicit `match` keeps it. xarxa has one error type,
   so `Err(e) => Err(e)` is exactly equivalent. 83 such `?` sites.
2. `#[flux_rs::sig]` **without** `#[flux_rs::trusted(no)]` is a trusted shim —
   signature handed to callers, body never checked, indistinguishable from a proof.
   Confirm `1 checked` in the summary.
3. `#[flux_rs::trusted(no)]` inside a `macro_rules!` body does **not** untrust the
   expansion. Declarations (`refined_by`, `variant`, `field`) inside macros *do*
   work. Expand the macro if you need the body checked.
4. `--only-check` with a def path matching nothing **exits 0 silently**. Use full
   runs for negative controls.
5. Flux interprets neither `>>` nor `&`. Rewrite as `/` and `%`.
6. Never quote an error count from a log containing `panicked`.
7. `cone.py` refuses a dirty checkout — commit first.
