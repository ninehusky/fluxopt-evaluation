# Attack list

190 functions hold 353 of the 453 xarxa panic sites in the firmware; the rest sit outside a function this parser recognises (macro bodies, derives, closures).

## By kind of work

| sites | est. bytes | category | what it is |
| ---: | ---: | --- | --- |
| 172 | 8061 | **CHURN** | state a length/range precondition and discharge it |
| 105 | 4228 | **PANIC** | explicit panic!/unreachable!/assert! -- needs a cross-API precondition |
| 52 | 2938 | **CORE** | core iterator/Option/Result chain Flux cannot see through |
| 12 | 176 | **FLUXBUG** | Flux emits `internal flux error` -- compiler bug, quarantine |
| 7 | 3248 | **ICE** | rustc aborted -- quarantine or compiler fix |
| 5 | 105 | **CLEAN** | no obligation (UPPER BOUND -- see caveats) |

## By file

Sorted by CHURN sites, which is the tractable work.

| file | sites | churn | panic | core | spec | bug/ICE | Δ.text | status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `src/wire/ipv6.rs` | 34 | 22 | 3 | 6 | 0 | 0 | -1180 | partial(4/35 left) |
| `src/wire/ipv4.rs` | 21 | 20 | 1 | 0 | 0 | 0 | -564 | ok |
| `src/wire/icmpv6.rs` | 29 | 18 | 0 | 3 | 0 | 0 | -2604 | ok |
| `src/wire/udp.rs` | 18 | 18 | 0 | 0 | 0 | 0 | -636 | ok |
| `src/wire/ndisc.rs` | 16 | 12 | 0 | 2 | 0 | 0 | -348 | ok |
| `src/wire/sixlowpan/nhc.rs` | 25 | 12 | 3 | 0 | 0 | 0 | -568 | ok |
| `src/wire/arp.rs` | 9 | 9 | 0 | 0 | 0 | 0 | -652 | ok |
| `src/wire/ndiscoption.rs` | 13 | 9 | 0 | 4 | 0 | 0 | -740 | partial(2/13 left) |
| `src/wire/sixlowpan/iphc.rs` | 49 | 8 | 4 | 0 | 0 | 0 | -944 | partial(20/49 left) |
| `src/wire/tcp.rs` | 38 | 8 | 20 | 6 | 0 | 0 | -996 | ok |
| `src/wire/ethernet.rs` | 7 | 7 | 0 | 0 | 0 | 0 | 236 | partial(1/7 left) |
| `src/wire/ipv6option.rs` | 7 | 6 | 0 | 1 | 0 | 0 | -216 | ok |
| `src/wire/mld.rs` | 15 | 6 | 3 | 1 | 0 | 0 | -1072 | ok |
| `src/storage/ring_buffer.rs` | 21 | 4 | 2 | 3 | 0 | 10 | -164 | partial(3/15 left) |
| `src/wire/icmpv4.rs` | 8 | 4 | 0 | 2 | 0 | 0 | -156 | partial(2/8 left) |
| `src/iface/interface/sixlowpan.rs` | 16 | 3 | 7 | 4 | 0 | 0 | -244 | partial(2/16 left) |
| `src/wire/ieee802154.rs` | 34 | 3 | 0 | 5 | 0 | 0 | -256 | partial(6/34 left) |
| `src/wire/ipv6ext_header.rs` | 2 | 2 | 0 | 0 | 0 | 0 | 20 | ok |
| `src/wire/dhcpv4.rs` | 4 | 1 | 0 | 3 | 0 | 0 | 4 | ok |
| `src/iface/interface/ipv6.rs` | 3 | 0 | 2 | 1 | 0 | 0 | 268 | ok |
| `src/iface/interface/mod.rs` | 7 | 0 | 0 | 0 | 0 | 7 | -3248 | ok |
| `src/iface/neighbor.rs` | 4 | 0 | 4 | 0 | 0 | 0 | -424 | ok |
| `src/iface/packet.rs` | 11 | 0 | 12 | 0 | 0 | 0 | -384 | ok |
| `src/iface/route.rs` | 1 | 0 | 2 | 0 | 0 | 0 | -148 | partial(1/1 left) |
| `src/iface/socket_set.rs` | 28 | 0 | 28 | 0 | 0 | 0 | -1240 | ok |
| `src/phy/mod.rs` | 1 | 0 | 1 | 0 | 0 | 0 | -200 | ok |
| `src/socket/dhcpv4.rs` | 3 | 0 | 3 | 0 | 0 | 0 | 64 | ok |
| `src/socket/tcp.rs` | 4 | 0 | 1 | 1 | 0 | 0 | -20 | partial(4/8 left) |
| `src/socket/udp.rs` | 1 | 0 | 1 | 0 | 0 | 0 | 0 | partial(1/1 left) |
| `src/storage/assembler.rs` | 1 | 0 | 0 | 1 | 0 | 0 | -- | build-failed |
| `src/storage/packet_buffer.rs` | 4 | 0 | 1 | 1 | 0 | 2 | -180 | ok |
| `src/wire/ip.rs` | 4 | 0 | 4 | 0 | 0 | 0 | -184 | ok |
| `src/wire/ipv6hbh.rs` | 2 | 0 | 0 | 2 | 0 | 0 | -128 | ok |
| `src/wire/mod.rs` | 4 | 0 | 3 | 1 | 0 | 0 | -- | build-failed |
| `src/wire/sixlowpan/mod.rs` | 9 | 0 | 0 | 5 | 0 | 0 | -1260 | partial(2/10 left) |

## Rows: every CHURN function, biggest first

| file | fn | line | sites | first error |
| --- | --- | ---: | ---: | --- |
| `src/wire/icmpv6.rs` | `payload` | 457 | 5 | refinement type error |
| `src/storage/ring_buffer.rs` | `get_idx_unchecked` | 110 | 4 | assertion might fail: possible remainder with a divisor of zero |
| `src/wire/icmpv6.rs` | `clear_reserved` | 496 | 4 | assertion might fail: possible out-of-bounds access ;; refinement type error |
| `src/iface/interface/sixlowpan.rs` | `decompress_ext_hdr` | 713 | 3 | refinement type error |
| `src/wire/ethernet.rs` | `set_src_addr` | 287 | 3 | refinement type error |
| `src/wire/ethernet.rs` | `set_ethertype` | 295 | 3 | refinement type error |
| `src/wire/icmpv6.rs` | `set_msg_code` | 478 | 3 | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6.rs` | `set_traffic_class` | 516 | 3 | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6.rs` | `set_payload_len` | 539 | 3 | refinement type error |
| `src/wire/ipv6.rs` | `set_hop_limit` | 555 | 3 | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6.rs` | `set_src_addr` | 563 | 3 | refinement type error |
| `src/wire/ipv6.rs` | `set_dst_addr` | 571 | 3 | refinement type error |
| `src/wire/ipv6option.rs` | `data_mut` | 252 | 3 | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `dst_addr` | 282 | 3 | refinement type error |
| `src/wire/sixlowpan/nhc.rs` | `payload` | 622 | 3 | refinement type error |
| `src/wire/udp.rs` | `set_src_port` | 168 | 3 | refinement type error |
| `src/wire/udp.rs` | `set_dst_port` | 176 | 3 | refinement type error |
| `src/wire/udp.rs` | `set_len` | 184 | 3 | refinement type error |
| `src/wire/icmpv6.rs` | `set_msg_type` | 468 | 2 | assertion might fail: possible out-of-bounds access |
| `src/wire/icmpv6.rs` | `payload_mut` | 601 | 2 | refinement type error |
| `src/wire/ieee802154.rs` | `addressing_fields` | 434 | 2 | refinement type error |
| `src/wire/ipv4.rs` | `set_version` | 400 | 2 | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv4.rs` | `set_dscp` | 414 | 2 | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv4.rs` | `set_total_len` | 428 | 2 | refinement type error |
| `src/wire/ipv4.rs` | `set_ident` | 436 | 2 | refinement type error |
| `src/wire/ipv4.rs` | `clear_flags` | 444 | 2 | refinement type error |
| `src/wire/ipv4.rs` | `set_hop_limit` | 481 | 2 | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv4.rs` | `set_next_header` | 489 | 2 | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv4.rs` | `set_src_addr` | 504 | 2 | refinement type error |
| `src/wire/ipv4.rs` | `set_dst_addr` | 512 | 2 | refinement type error |
| `src/wire/ipv6.rs` | `payload_len` | 449 | 2 | refinement type error |
| `src/wire/ipv6.rs` | `set_version` | 506 | 2 | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6option.rs` | `set_data_len` | 239 | 2 | assertion might fail: possible out-of-bounds access |
| `src/wire/ndisc.rs` | `set_target_addr` | 170 | 2 | refinement type error |
| `src/wire/ndiscoption.rs` | `set_data_len` | 296 | 2 | assertion might fail: possible out-of-bounds access |
| `src/wire/ndiscoption.rs` | `data_mut` | 384 | 2 | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `set_field` | 486 | 2 | refinement type error |
| `src/wire/sixlowpan/nhc.rs` | `length` | 179 | 2 | assertion might fail: possible out-of-bounds access |
| `src/wire/sixlowpan/nhc.rs` | `payload` | 207 | 2 | refinement type error |
| `src/wire/sixlowpan/nhc.rs` | `payload_mut` | 631 | 2 | refinement type error |
| `src/wire/udp.rs` | `set_checksum` | 192 | 2 | refinement type error |
| `src/wire/udp.rs` | `payload_mut` | 222 | 2 | refinement type error |
| `src/wire/arp.rs` | `set_hardware_type` | 175 | 1 | refinement type error |
| `src/wire/arp.rs` | `set_protocol_type` | 183 | 1 | refinement type error |
| `src/wire/arp.rs` | `set_hardware_len` | 191 | 1 | assertion might fail: possible out-of-bounds access |
| `src/wire/arp.rs` | `set_protocol_len` | 199 | 1 | assertion might fail: possible out-of-bounds access |
| `src/wire/arp.rs` | `set_operation` | 207 | 1 | refinement type error |
| `src/wire/arp.rs` | `set_source_hardware_addr` | 217 | 1 | refinement type error |
| `src/wire/arp.rs` | `set_source_protocol_addr` | 228 | 1 | refinement type error |
| `src/wire/arp.rs` | `set_target_hardware_addr` | 239 | 1 | refinement type error |
| `src/wire/arp.rs` | `set_target_protocol_addr` | 250 | 1 | refinement type error |
| `src/wire/dhcpv4.rs` | `set_magic_number` | 496 | 1 | refinement type error |
| `src/wire/ethernet.rs` | `from_bytes` | 75 | 1 | refinement type error |
| `src/wire/icmpv4.rs` | `set_msg_code` | 307 | 1 | assertion might fail: possible out-of-bounds access |
| `src/wire/icmpv4.rs` | `set_echo_ident` | 325 | 1 | refinement type error |
| `src/wire/icmpv4.rs` | `set_echo_seq_no` | 336 | 1 | refinement type error |
| `src/wire/icmpv4.rs` | `data_mut` | 356 | 1 | refinement type error |
| `src/wire/icmpv6.rs` | `set_echo_ident` | 544 | 1 | refinement type error |
| `src/wire/icmpv6.rs` | `set_echo_seq_no` | 555 | 1 | refinement type error |
| `src/wire/ieee802154.rs` | `payload` | 721 | 1 | refinement type error |
| `src/wire/ipv4.rs` | `verify_checksum` | 365 | 1 | refinement type error |
| `src/wire/ipv4.rs` | `payload` | 389 | 1 | refinement type error |
| `src/wire/ipv6.rs` | `payload` | 495 | 1 | refinement type error |
| `src/wire/ipv6.rs` | `set_next_header` | 547 | 1 | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6.rs` | `payload_mut` | 579 | 1 | refinement type error |
| `src/wire/ipv6ext_header.rs` | `set_next_header` | 101 | 1 | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6ext_header.rs` | `set_header_len` | 110 | 1 | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6option.rs` | `set_option_type` | 228 | 1 | assertion might fail: possible out-of-bounds access |
| `src/wire/mld.rs` | `s_flag` | 59 | 1 | assertion might fail: possible out-of-bounds access |
| `src/wire/mld.rs` | `qqic` | 74 | 1 | assertion might fail: possible out-of-bounds access |
| `src/wire/mld.rs` | `num_srcs` | 82 | 1 | refinement type error |
| `src/wire/mld.rs` | `set_qqic` | 147 | 1 | assertion might fail: possible out-of-bounds access |
| `src/wire/mld.rs` | `set_num_srcs` | 155 | 1 | refinement type error |
| `src/wire/mld.rs` | `set_num_srcs` | 279 | 1 | refinement type error |
| `src/wire/ndisc.rs` | `reachable_time` | 58 | 1 | refinement type error |
| `src/wire/ndisc.rs` | `retrans_time` | 66 | 1 | refinement type error |
| `src/wire/ndisc.rs` | `set_current_hop_limit` | 123 | 1 | assertion might fail: possible out-of-bounds access |
| `src/wire/ndisc.rs` | `set_router_flags` | 131 | 1 | assertion might fail: possible out-of-bounds access |
| `src/wire/ndisc.rs` | `set_router_lifetime` | 138 | 1 | refinement type error |
| `src/wire/ndisc.rs` | `set_reachable_time` | 146 | 1 | refinement type error |
| `src/wire/ndisc.rs` | `set_retrans_time` | 154 | 1 | refinement type error |
| `src/wire/ndisc.rs` | `set_dest_addr` | 196 | 1 | refinement type error |
| `src/wire/ndisc.rs` | `parse` | 241 | 1 | refinement type error |
| `src/wire/ndisc.rs` | `emit` | 360 | 1 | refinement type error |
| `src/wire/ndiscoption.rs` | `set_option_type` | 288 | 1 | assertion might fail: possible out-of-bounds access |
| `src/wire/ndiscoption.rs` | `set_link_layer_addr` | 307 | 1 | refinement type error |
| `src/wire/ndiscoption.rs` | `set_mtu` | 318 | 1 | refinement type error |
| `src/wire/ndiscoption.rs` | `clear_prefix_reserved` | 355 | 1 | refinement type error |
| `src/wire/ndiscoption.rs` | `set_prefix` | 363 | 1 | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `next_header` | 122 | 1 | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `payload` | 449 | 1 | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `set_dispatch_field` | 467 | 1 | refinement type error |
| `src/wire/sixlowpan/nhc.rs` | `checksum` | 586 | 1 | refinement type error |
| `src/wire/sixlowpan/nhc.rs` | `set_dispatch_field` | 638 | 1 | assertion might fail: possible out-of-bounds access |
| `src/wire/sixlowpan/nhc.rs` | `set_checksum` | 687 | 1 | refinement type error |
| `src/wire/tcp.rs` | `options` | 393 | 1 | refinement type error |
| `src/wire/tcp.rs` | `payload` | 402 | 1 | refinement type error |
| `src/wire/tcp.rs` | `set_src_port` | 413 | 1 | refinement type error |
| `src/wire/tcp.rs` | `set_dst_port` | 421 | 1 | refinement type error |
| `src/wire/tcp.rs` | `set_window_len` | 580 | 1 | refinement type error |
| `src/wire/tcp.rs` | `set_urgent_at` | 595 | 1 | refinement type error |
| `src/wire/tcp.rs` | `options_mut` | 620 | 1 | refinement type error |
| `src/wire/tcp.rs` | `payload_mut` | 629 | 1 | refinement type error |
| `src/wire/udp.rs` | `len` | 93 | 1 | refinement type error |
| `src/wire/udp.rs` | `checksum` | 101 | 1 | refinement type error |
| `src/wire/udp.rs` | `verify_checksum` | 132 | 1 | refinement type error |
| `src/wire/udp.rs` | `payload` | 157 | 1 | refinement type error |
| `src/wire/udp.rs` | `fill_checksum` | 203 | 1 | refinement type error |

## Caveats

- **The byte columns DO NOT ADD UP, by construction.** Each file's Δ.text was measured by making that one file panic-free against the same reference build, so the deltas overlap and double-count shared panic machinery. They sum to -18756 B, which is 14% of `.text` -- not a number anything is going to deliver. Use the byte columns to RANK files against each other and ignore their totals.
- **Δ.text is the weakest number here.** It comes from the per-file ablation sweep, which predates the xarxa merge that moved the benchmark from -504 to -1504 B, and a single-file rebuild shifts inlining by up to ~268 B on its own. Use it to rank, not to promise.
- **Bytes per category are apportioned by site share within a file**, so they assume every site in a file is worth the same. They are not measured per site.
- **CLEAN is an upper bound.** A function with no error may simply have had no obligation generated for it.
- **Categories are the FIRST error on a function.** A function counted CHURN can still hold a PANIC obligation behind it.
- Sites here are attributed to functions by line range; sites in macro bodies and derives are counted in the file total but appear in no row.
