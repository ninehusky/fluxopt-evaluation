# Plan: what to tackle, split by kind of work

Categories are the first Flux error on each panic-holding function, from
`results/TRIAGE.md` (185 functions opted in at once on `flux-triage`).
Bytes come from the per-file ablation sweep, apportioned across a file's
categories by site share. First-order only: the sweep predates the latest
xarxa merge, and negative file deltas (inlining noise) are dropped.

| category | sites | est. bytes | what it is |
| --- | ---: | ---: | --- |
| **CHURN** | 191 | 3,823 | ordinary refinement: state a length/range precondition, discharge it |
| **HARD** | 102 | 3,560 | explicit panic needing a cross-API precondition, or a per-element fact slices cannot express |
| **SPEC** | 37 | 380 | blocked only on an extern spec that ALREADY EXISTS on another branch |
| **ICE** | 20 | 2,750 | rustc/Flux aborts; quarantine or compiler fix |
| **CLEAN** | 18 | 307 | no obligation -- UPPER BOUND, see caveat |

Total categorised: 368 sites

## Start here: biggest CHURN files

| file | churn | spec | hard | file bytes |
| --- | ---: | ---: | ---: | ---: |
| `src/wire/ipv6.rs` | 22 | 7 | 2 | 316 |
| `src/wire/icmpv6.rs` | 20 | 0 | 1 | 2,436 |
| `src/wire/ipv4.rs` | 20 | 0 | 1 | 316 |
| `src/wire/sixlowpan/nhc.rs` | 16 | 0 | 0 | 0 |
| `src/iface/interface/sixlowpan.rs` | 13 | 0 | 1 | 0 |
| `src/wire/udp.rs` | 12 | 6 | 0 | 0 |
| `src/wire/ndisc.rs` | 11 | 2 | 1 | 84 |
| `src/wire/ndiscoption.rs` | 11 | 2 | 0 | 116 |
| `src/wire/tcp.rs` | 10 | 1 | 23 | 1,044 |
| `src/wire/sixlowpan/iphc.rs` | 9 | 2 | 1 | 0 |
