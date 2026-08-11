# Per-file panic ablation, nRF52840 `usb_ethernet`

`.text` bytes that disappear when a file is made panic-free. Produced by `./sweep.py`; see ../README.md for the method.

Reference `.text` reproduced exactly across rebuilds, so the deltas are not build noise. But a single-file rebuild still shifts inlining: the largest *increase* seen was **+268 B**, so treat |delta| under roughly that as unresolved.

| file | sites | what they are | Δ.text | Δsites | status |
| --- | --- | --- | --- | --- | --- |
| `src/iface/interface/mod.rs` | 7 | 3 panic!/unreachable!, 1 assert!, 1 expect | -3248 | -12 | ok |
| `src/wire/icmpv6.rs` | 37 | 25 slice-index, 11 bounds-check, 1 panic!(fmt) | -2604 | -40 | ok |
| `src/wire/sixlowpan/mod.rs` | 10 | 4 slice-index, 3 bounds-check, 2 copy_from_slice | -1260 | -9 | partial(2/10 left) |
| `src/iface/socket_set.rs` | 28 | 11 panic!(fmt), 9 bounds-check, 8 expect | -1240 | -31 | ok |
| `src/wire/ipv6.rs` | 35 | 18 slice-index, 12 bounds-check, 5 panic!/unreachable! | -1180 | -30 | partial(4/35 left) |
| `src/wire/mld.rs` | 21 | 9 bounds-check, 8 slice-index, 2 panic!/unreachable! | -1072 | -16 | ok |
| `src/wire/tcp.rs` | 34 | 16 slice-index, 14 panic!(fmt), 3 bounds-check | -996 | -38 | ok |
| `src/wire/sixlowpan/iphc.rs` | 49 | 44 slice-index, 4 bounds-check, 1 panic!/unreachable! | -944 | -30 | partial(20/49 left) |
| `src/wire/ndiscoption.rs` | 13 | 8 slice-index, 3 bounds-check, 2 copy_from_slice | -740 | -12 | partial(2/13 left) |
| `src/wire/arp.rs` | 9 | 7 slice-index, 2 bounds-check | -652 | -10 | ok |
| `src/wire/udp.rs` | 18 | 18 slice-index | -636 | -18 | ok |
| `src/wire/sixlowpan/nhc.rs` | 25 | 16 slice-index, 9 bounds-check | -568 | -24 | ok |
| `src/wire/ipv4.rs` | 21 | 12 slice-index, 8 bounds-check, 1 panic!/unreachable! | -564 | -23 | ok |
| `src/iface/neighbor.rs` | 4 | 3 panic!/unreachable!, 1 unwrap | -424 | -4 | ok |
| `src/iface/packet.rs` | 12 | 8 panic!/unreachable!, 2 slice-index, 1 copy_from_slice | -384 | -11 | ok |
| `src/wire/ndisc.rs` | 16 | 13 slice-index, 3 bounds-check | -348 | -16 | ok |
| `src/wire/ieee802154.rs` | 34 | 29 slice-index, 3 bounds-check, 2 panic!/unreachable! | -256 | -28 | partial(6/34 left) |
| `src/iface/interface/sixlowpan.rs` | 16 | 13 slice-index, 2 panic!/unreachable!, 1 copy_from_slice | -244 | -13 | partial(2/16 left) |
| `src/wire/ipv6option.rs` | 7 | 4 slice-index, 3 bounds-check | -216 | -7 | ok |
| `src/phy/mod.rs` | 1 | 1 panic!(fmt) | -200 | -1 | ok |
| `src/wire/ip.rs` | 4 | 4 panic!/unreachable! | -184 | -3 | ok |
| `src/storage/packet_buffer.rs` | 2 | 1 slice-index, 1 unwrap | -180 | -3 | ok |
| `src/storage/ring_buffer.rs` | 15 | 10 slice-index, 2 rem-by-zero, 2 panic!/unreachable! | -164 | -12 | partial(3/15 left) |
| `src/wire/icmpv4.rs` | 8 | 5 slice-index, 2 copy_from_slice, 1 bounds-check | -156 | -6 | partial(2/8 left) |
| `src/iface/route.rs` | 1 | 1 panic!/unreachable! | -148 | -2 | partial(1/1 left) |
| `src/wire/ipv6hbh.rs` | 2 | 2 slice-index | -128 | -2 | ok |
| `src/socket/tcp.rs` | 8 | 5 panic!(fmt), 1 unwrap, 1 slice-index | -20 | -4 | partial(4/8 left) |
| `src/wire/mod.rs` | 4 | 3 panic!(fmt), 1 slice-index | — | — | build-failed |
| `src/storage/assembler.rs` | 1 | 1 bounds-check | — | — | build-failed |
| `src/socket/udp.rs` | 1 | 1 copy_from_slice | +0 | 0 | partial(1/1 left) |
| `src/wire/dhcpv4.rs` | 4 | 4 slice-index | +4 | -4 | ok |
| `src/wire/ipv6ext_header.rs` | 2 | 2 bounds-check | +20 | -2 | ok |
| `src/socket/dhcpv4.rs` | 3 | 2 panic!(fmt), 1 panic!/unreachable! | +64 | -1 | ok |
| `src/wire/ethernet.rs` | 7 | 6 slice-index, 1 copy_from_slice | +236 | 1 | partial(1/7 left) |
| `src/iface/interface/ipv6.rs` | 3 | 1 slice-index, 1 panic!/unreachable!, 1 unwrap | +268 | -3 | ok |
