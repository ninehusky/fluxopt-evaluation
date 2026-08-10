# Per-file panic ablation, nRF52840 `usb_ethernet`

`.text` bytes that disappear when a file is made panic-free. Produced by `./sweep.py`; see ../README.md for the method.

Reference `.text` reproduced exactly across rebuilds, so the deltas are not build noise. But a single-file rebuild still shifts inlining: the largest *increase* seen was **+332 B**, so treat |delta| under roughly that as unresolved.

| file | sites | what they are | Δ.text | Δsites | status |
| --- | --- | --- | --- | --- | --- |
| `src/iface/interface/mod.rs` | 4 | 1 panic!/unreachable!, 1 expect, 1 slice-index | -2660 | -9 | ok |
| `src/wire/icmpv6.rs` | 41 | 27 slice-index, 12 bounds-check, 2 panic!(fmt) | -2436 | -43 | ok |
| `src/wire/tcp.rs` | 34 | 16 slice-index, 14 panic!(fmt), 3 bounds-check | -1044 | -38 | ok |
| `src/iface/socket_set.rs` | 28 | 11 panic!(fmt), 9 bounds-check, 8 expect | -924 | -29 | ok |
| `src/iface/neighbor.rs` | 4 | 3 panic!/unreachable!, 1 unwrap | -760 | -4 | ok |
| `src/wire/mld.rs` | 21 | 9 bounds-check, 8 slice-index, 2 panic!/unreachable! | -436 | -17 | ok |
| `src/wire/dhcpv4.rs` | 4 | 4 slice-index | -428 | -3 | ok |
| `src/wire/ipv6.rs` | 33 | 16 slice-index, 12 bounds-check, 5 panic!/unreachable! | -316 | -22 | partial(4/33 left) |
| `src/wire/ipv4.rs` | 12 | 7 slice-index, 4 bounds-check, 1 panic!/unreachable! | -316 | -12 | ok |
| `src/wire/ipv6option.rs` | 7 | 4 slice-index, 3 bounds-check | -200 | -7 | ok |
| `src/iface/packet.rs` | 9 | 5 slice-index, 2 panic!/unreachable!, 1 copy_from_slice | -184 | -5 | partial(4/9 left) |
| `src/wire/ip.rs` | 4 | 4 panic!/unreachable! | -168 | -4 | ok |
| `src/iface/interface/ipv6.rs` | 3 | 1 slice-index, 1 panic!/unreachable!, 1 unwrap | -156 | -3 | ok |
| `src/wire/icmpv4.rs` | 8 | 5 slice-index, 2 copy_from_slice, 1 bounds-check | -148 | -6 | partial(2/8 left) |
| `src/storage/ring_buffer.rs` | 15 | 10 slice-index, 2 rem-by-zero, 2 panic!/unreachable! | -140 | -10 | partial(2/15 left) |
| `src/iface/route.rs` | 1 | 1 panic!/unreachable! | -120 | -1 | ok |
| `src/wire/ndiscoption.rs` | 13 | 8 slice-index, 3 bounds-check, 2 copy_from_slice | -116 | -9 | partial(2/13 left) |
| `src/phy/mod.rs` | 1 | 1 panic!(fmt) | -88 | -1 | ok |
| `src/wire/ndisc.rs` | 16 | 13 slice-index, 3 bounds-check | -84 | -12 | ok |
| `src/socket/dhcpv4.rs` | 1 | 1 panic!/unreachable! | -44 | -1 | ok |
| `src/storage/packet_buffer.rs` | 2 | 1 slice-index, 1 unwrap | -32 | -1 | ok |
| `src/socket/tcp.rs` | 8 | 5 panic!(fmt), 1 unwrap, 1 slice-index | -20 | -4 | partial(4/8 left) |
| `src/wire/mod.rs` | 1 | 1 slice-index | — | — | build-failed |
| `src/storage/assembler.rs` | 1 | 1 bounds-check | — | — | build-failed |
| `src/socket/udp.rs` | 1 | 1 copy_from_slice | +20 | 0 | partial(1/1 left) |
| `src/wire/ipv6hbh.rs` | 2 | 2 slice-index | +92 | 1 | ok |
| `src/wire/udp.rs` | 8 | 8 slice-index | +96 | -10 | ok |
| `src/wire/ethernet.rs` | 7 | 6 slice-index, 1 copy_from_slice | +232 | 1 | partial(1/7 left) |
| `src/wire/arp.rs` | 9 | 7 slice-index, 2 bounds-check | +332 | -2 | ok |
