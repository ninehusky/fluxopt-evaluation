# Breadth triage: what happens if every panic-holding function is checked

190 functions, 353 panic sites, 35 files.

| sites | outcome |
| ---: | --- |
| 341 | OBLIGATION |
| 7 | ICE |
| 5 | CLEAN |

| file | fn | line | sites | outcome | first error |
| --- | --- | ---: | ---: | --- | --- |
| `src/wire/sixlowpan/nhc.rs` | `set_ports` | 648 | 3 | CLEAN |  |
| `src/socket/tcp.rs` | `process` | 1603 | 2 | CLEAN |  |
| `src/iface/interface/mod.rs` | `dispatch_ip` | 1238 | 3 | ICE | rustc aborted; quarantine candidate |
| `src/iface/interface/mod.rs` | `new` | 210 | 1 | ICE | rustc aborted; quarantine candidate |
| `src/iface/interface/mod.rs` | `socket_egress` | 706 | 1 | ICE | rustc aborted; quarantine candidate |
| `src/iface/interface/mod.rs` | `check_ip_addrs` | 918 | 1 | ICE | rustc aborted; quarantine candidate |
| `src/iface/interface/mod.rs` | `lookup_hardware_addr` | 1085 | 1 | ICE | rustc aborted; quarantine candidate |
| `src/iface/socket_set.rs` | `get_mut` | 115 | 21 | OBLIGATION | call to core[a8c6]::option::{impl#0}::expect may panic: MightPanic(Tra |
| `src/wire/tcp.rs` | `add` | 43 | 7 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/iface/packet.rs` | `emit_payload` | 74 | 6 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/iface/packet.rs` | `as_sixlowpan_next_header` | 233 | 6 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/wire/tcp.rs` | `sub` | 73 | 6 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/wire/tcp.rs` | `emit` | 743 | 6 | OBLIGATION | refinement type error |
| `src/iface/interface/sixlowpan.rs` | `ipv6_to_sixlowpan` | 425 | 5 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/storage/ring_buffer.rs` | `dequeue_many_with` | 243 | 5 | OBLIGATION | internal flux error: crates/flux-infer/src/infer.rs:888:22 |
| `src/wire/icmpv6.rs` | `payload` | 457 | 5 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/mod.rs` | `resolve` | 66 | 5 | OBLIGATION | call to core[a8c6]::array::{impl#16}::index_mut may panic: MightPanic( |
| `src/storage/ring_buffer.rs` | `get_idx_unchecked` | 110 | 4 | OBLIGATION | assertion might fail: possible remainder with a divisor of zero |
| `src/wire/icmpv6.rs` | `clear_reserved` | 496 | 4 | OBLIGATION | refinement type error |
| `src/wire/ip.rs` | `pseudo_header` | 977 | 4 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/wire/ipv6.rs` | `set_flow_label` | 529 | 4 | OBLIGATION | call to byteorder[387c]::ByteOrder::write_u24 may panic: MightPanic(No |
| `src/iface/interface/sixlowpan.rs` | `decompress_ext_hdr` | 713 | 3 | OBLIGATION | refinement type error |
| `src/iface/interface/sixlowpan.rs` | `decompress_udp` | 750 | 3 | OBLIGATION | refinement type error |
| `src/iface/socket_set.rs` | `get` | 100 | 3 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/storage/ring_buffer.rs` | `dequeue_one_with` | 147 | 3 | OBLIGATION | internal flux error: crates/flux-infer/src/infer.rs:888:22 |
| `src/wire/ethernet.rs` | `set_src_addr` | 287 | 3 | OBLIGATION | refinement type error |
| `src/wire/ethernet.rs` | `set_ethertype` | 295 | 3 | OBLIGATION | refinement type error |
| `src/wire/icmpv6.rs` | `set_msg_code` | 478 | 3 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6.rs` | `set_traffic_class` | 516 | 3 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6.rs` | `set_payload_len` | 539 | 3 | OBLIGATION | refinement type error |
| `src/wire/ipv6.rs` | `set_hop_limit` | 555 | 3 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6.rs` | `set_src_addr` | 563 | 3 | OBLIGATION | refinement type error |
| `src/wire/ipv6.rs` | `set_dst_addr` | 571 | 3 | OBLIGATION | refinement type error |
| `src/wire/ipv6option.rs` | `data_mut` | 252 | 3 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `dst_addr` | 282 | 3 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/nhc.rs` | `payload` | 622 | 3 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `parse` | 658 | 3 | OBLIGATION | refinement type error |
| `src/wire/udp.rs` | `set_src_port` | 168 | 3 | OBLIGATION | refinement type error |
| `src/wire/udp.rs` | `set_dst_port` | 176 | 3 | OBLIGATION | refinement type error |
| `src/wire/udp.rs` | `set_len` | 184 | 3 | OBLIGATION | refinement type error |
| `src/iface/interface/ipv6.rs` | `get_source_address_ipv6` | 31 | 2 | OBLIGATION | call to core[a8c6]::iter::adapters::filter_map::{impl#2}::next may pan |
| `src/iface/interface/sixlowpan.rs` | `dispatch_sixlowpan` | 295 | 2 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/iface/neighbor.rs` | `fill_with_expiration` | 96 | 2 | OBLIGATION | call to heapless[ea1e]::linear_map::{impl#1}::iter may panic: MightPan |
| `src/iface/neighbor.rs` | `lookup` | 151 | 2 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/iface/route.rs` | `lookup` | 173 | 2 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/iface/socket_set.rs` | `add` | 63 | 2 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/iface/socket_set.rs` | `remove` | 128 | 2 | OBLIGATION | call to managed[ba83]::slice::{impl#3}::deref_mut may panic: MightPani |
| `src/socket/dhcpv4.rs` | `process` | 306 | 2 | OBLIGATION | call to core[a8c6]::cmp::PartialEq::ne may panic: MightPanic(Transitiv |
| `src/storage/packet_buffer.rs` | `dequeue_with` | 184 | 2 | OBLIGATION | internal flux error: crates/flux-infer/src/infer.rs:888:22 |
| `src/storage/ring_buffer.rs` | `enqueue_many_with` | 184 | 2 | OBLIGATION | internal flux error: crates/flux-infer/src/infer.rs:888:22 |
| `src/storage/ring_buffer.rs` | `get_allocated` | 359 | 2 | OBLIGATION | refinement type error |
| `src/wire/dhcpv4.rs` | `set_sname_and_boot_file_to_zero` | 427 | 2 | OBLIGATION | refinement type error |
| `src/wire/icmpv4.rs` | `emit` | 492 | 2 | OBLIGATION | refinement type error |
| `src/wire/icmpv6.rs` | `set_msg_type` | 468 | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/icmpv6.rs` | `payload_mut` | 601 | 2 | OBLIGATION | refinement type error |
| `src/wire/icmpv6.rs` | `emit` | 777 | 2 | OBLIGATION | refinement type error |
| `src/wire/ieee802154.rs` | `frame_type` | 370 | 2 | OBLIGATION | refinement type error |
| `src/wire/ieee802154.rs` | `addressing_fields` | 434 | 2 | OBLIGATION | refinement type error |
| `src/wire/ipv4.rs` | `set_version` | 400 | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv4.rs` | `set_dscp` | 414 | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv4.rs` | `set_total_len` | 428 | 2 | OBLIGATION | refinement type error |
| `src/wire/ipv4.rs` | `set_ident` | 436 | 2 | OBLIGATION | refinement type error |
| `src/wire/ipv4.rs` | `clear_flags` | 444 | 2 | OBLIGATION | refinement type error |
| `src/wire/ipv4.rs` | `set_hop_limit` | 481 | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv4.rs` | `set_next_header` | 489 | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv4.rs` | `set_src_addr` | 504 | 2 | OBLIGATION | refinement type error |
| `src/wire/ipv4.rs` | `set_dst_addr` | 512 | 2 | OBLIGATION | refinement type error |
| `src/wire/ipv6.rs` | `mask` | 163 | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6.rs` | `payload_len` | 449 | 2 | OBLIGATION | refinement type error |
| `src/wire/ipv6.rs` | `set_version` | 506 | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6hbh.rs` | `emit` | 100 | 2 | OBLIGATION | call to core[a8c6]::slice::iter::{impl#166}::next may panic: MightPani |
| `src/wire/ipv6option.rs` | `set_data_len` | 239 | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/mld.rs` | `set_mcast_addr` | 290 | 2 | OBLIGATION | call to core[a8c6]::net::ip_addr::{impl#20}::is_multicast may panic: M |
| `src/wire/mod.rs` | `ethernet_or_panic` | 438 | 2 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/wire/ndisc.rs` | `set_target_addr` | 170 | 2 | OBLIGATION | refinement type error |
| `src/wire/ndiscoption.rs` | `set_data_len` | 296 | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ndiscoption.rs` | `data_mut` | 384 | 2 | OBLIGATION | refinement type error |
| `src/wire/ndiscoption.rs` | `emit` | 542 | 2 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `flow_label_field` | 204 | 2 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `set_field` | 486 | 2 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/nhc.rs` | `length` | 179 | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/sixlowpan/nhc.rs` | `payload` | 207 | 2 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/nhc.rs` | `dst_port` | 550 | 2 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/nhc.rs` | `payload_mut` | 631 | 2 | OBLIGATION | refinement type error |
| `src/wire/udp.rs` | `set_checksum` | 192 | 2 | OBLIGATION | refinement type error |
| `src/wire/udp.rs` | `payload_mut` | 222 | 2 | OBLIGATION | refinement type error |
| `src/iface/interface/ipv6.rs` | `process_hopbyhop` | 265 | 1 | OBLIGATION | refinement type error |
| `src/iface/interface/sixlowpan.rs` | `process_sixlowpan` | 53 | 1 | OBLIGATION | call to core[a8c6]::array::{impl#15}::index may panic: MightPanic(Tran |
| `src/phy/mod.rs` | `from_driver` | 60 | 1 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/socket/dhcpv4.rs` | `dispatch` | 565 | 1 | OBLIGATION | call to core[a8c6]::ops::function::FnOnce::call_once may panic: MightP |
| `src/socket/tcp.rs` | `new` | 580 | 1 | OBLIGATION | call to core[a8c6]::num::{impl#11}::leading_zeros may panic: MightPani |
| `src/socket/tcp.rs` | `seq_to_transmit` | 2319 | 1 | OBLIGATION | arithmetic operation may underflow |
| `src/socket/udp.rs` | `process` | 612 | 1 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/storage/assembler.rs` | `add` | 197 | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/storage/packet_buffer.rs` | `dequeue` | 210 | 1 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/storage/packet_buffer.rs` | `peek` | 225 | 1 | OBLIGATION | call to core[a8c6]::option::{impl#0}::unwrap may panic: MightPanic(Tra |
| `src/storage/ring_buffer.rs` | `get_unallocated` | 302 | 1 | OBLIGATION | call to managed[ba83]::slice::{impl#3}::deref_mut may panic: MightPani |
| `src/storage/ring_buffer.rs` | `enqueue_unallocated` | 350 | 1 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/storage/ring_buffer.rs` | `dequeue_allocated` | 405 | 1 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/wire/arp.rs` | `set_hardware_type` | 175 | 1 | OBLIGATION | refinement type error |
| `src/wire/arp.rs` | `set_protocol_type` | 183 | 1 | OBLIGATION | refinement type error |
| `src/wire/arp.rs` | `set_hardware_len` | 191 | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/arp.rs` | `set_protocol_len` | 199 | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/arp.rs` | `set_operation` | 207 | 1 | OBLIGATION | refinement type error |
| `src/wire/arp.rs` | `set_source_hardware_addr` | 217 | 1 | OBLIGATION | refinement type error |
| `src/wire/arp.rs` | `set_source_protocol_addr` | 228 | 1 | OBLIGATION | refinement type error |
| `src/wire/arp.rs` | `set_target_hardware_addr` | 239 | 1 | OBLIGATION | refinement type error |
| `src/wire/arp.rs` | `set_target_protocol_addr` | 250 | 1 | OBLIGATION | refinement type error |
| `src/wire/dhcpv4.rs` | `set_magic_number` | 496 | 1 | OBLIGATION | refinement type error |
| `src/wire/dhcpv4.rs` | `emit` | 843 | 1 | OBLIGATION | call to core[a8c6]::ops::arith::{impl#144}::mul may panic: MightPanic( |
| `src/wire/ethernet.rs` | `from_bytes` | 75 | 1 | OBLIGATION | refinement type error |
| `src/wire/icmpv4.rs` | `set_msg_code` | 307 | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/icmpv4.rs` | `set_echo_ident` | 325 | 1 | OBLIGATION | refinement type error |
| `src/wire/icmpv4.rs` | `set_echo_seq_no` | 336 | 1 | OBLIGATION | refinement type error |
| `src/wire/icmpv4.rs` | `data_mut` | 356 | 1 | OBLIGATION | refinement type error |
| `src/wire/icmpv6.rs` | `set_echo_ident` | 544 | 1 | OBLIGATION | refinement type error |
| `src/wire/icmpv6.rs` | `set_echo_seq_no` | 555 | 1 | OBLIGATION | refinement type error |
| `src/wire/icmpv6.rs` | `parse` | 661 | 1 | OBLIGATION | call to core[a8c6]::result::{impl#0}::map may panic: MightPanic(Transi |
| `src/wire/ieee802154.rs` | `dst_addressing_mode` | 388 | 1 | OBLIGATION | refinement type error |
| `src/wire/ieee802154.rs` | `src_addressing_mode` | 407 | 1 | OBLIGATION | refinement type error |
| `src/wire/ieee802154.rs` | `src_pan_id` | 542 | 1 | OBLIGATION | call to byteorder[387c]::{impl#3}::read_u16 may panic: MightPanic(NoMI |
| `src/wire/ieee802154.rs` | `payload` | 721 | 1 | OBLIGATION | refinement type error |
| `src/wire/ipv4.rs` | `new` | 101 | 1 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/wire/ipv4.rs` | `verify_checksum` | 365 | 1 | OBLIGATION | refinement type error |
| `src/wire/ipv4.rs` | `payload` | 389 | 1 | OBLIGATION | refinement type error |
| `src/wire/ipv6.rs` | `solicited_node` | 179 | 1 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/wire/ipv6.rs` | `src_addr` | 477 | 1 | OBLIGATION | refinement type error |
| `src/wire/ipv6.rs` | `dst_addr` | 485 | 1 | OBLIGATION | refinement type error |
| `src/wire/ipv6.rs` | `payload` | 495 | 1 | OBLIGATION | refinement type error |
| `src/wire/ipv6.rs` | `set_next_header` | 547 | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6.rs` | `payload_mut` | 579 | 1 | OBLIGATION | refinement type error |
| `src/wire/ipv6ext_header.rs` | `set_next_header` | 101 | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6ext_header.rs` | `set_header_len` | 110 | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6option.rs` | `set_option_type` | 228 | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6option.rs` | `emit` | 339 | 1 | OBLIGATION | refinement type error |
| `src/wire/mld.rs` | `mcast_addr` | 51 | 1 | OBLIGATION | refinement type error |
| `src/wire/mld.rs` | `s_flag` | 59 | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/mld.rs` | `qqic` | 74 | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/mld.rs` | `num_srcs` | 82 | 1 | OBLIGATION | refinement type error |
| `src/wire/mld.rs` | `set_qrv` | 138 | 1 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/wire/mld.rs` | `set_qqic` | 147 | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/mld.rs` | `set_num_srcs` | 155 | 1 | OBLIGATION | refinement type error |
| `src/wire/mld.rs` | `set_num_srcs` | 279 | 1 | OBLIGATION | refinement type error |
| `src/wire/mod.rs` | `ieee802154_or_panic` | 448 | 1 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/wire/mod.rs` | `as_bytes` | 551 | 1 | OBLIGATION | call to core[a8c6]::array::{impl#15}::index may panic: MightPanic(Tran |
| `src/wire/ndisc.rs` | `reachable_time` | 58 | 1 | OBLIGATION | refinement type error |
| `src/wire/ndisc.rs` | `retrans_time` | 66 | 1 | OBLIGATION | refinement type error |
| `src/wire/ndisc.rs` | `target_addr` | 82 | 1 | OBLIGATION | call to core[a8c6]::result::{impl#0}::unwrap may panic: MightPanic(Tra |
| `src/wire/ndisc.rs` | `dest_addr` | 109 | 1 | OBLIGATION | refinement type error |
| `src/wire/ndisc.rs` | `set_current_hop_limit` | 123 | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ndisc.rs` | `set_router_flags` | 131 | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ndisc.rs` | `set_router_lifetime` | 138 | 1 | OBLIGATION | refinement type error |
| `src/wire/ndisc.rs` | `set_reachable_time` | 146 | 1 | OBLIGATION | refinement type error |
| `src/wire/ndisc.rs` | `set_retrans_time` | 154 | 1 | OBLIGATION | refinement type error |
| `src/wire/ndisc.rs` | `set_dest_addr` | 196 | 1 | OBLIGATION | refinement type error |
| `src/wire/ndisc.rs` | `parse` | 241 | 1 | OBLIGATION | refinement type error |
| `src/wire/ndisc.rs` | `emit` | 360 | 1 | OBLIGATION | refinement type error |
| `src/wire/ndiscoption.rs` | `set_option_type` | 288 | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ndiscoption.rs` | `set_link_layer_addr` | 307 | 1 | OBLIGATION | refinement type error |
| `src/wire/ndiscoption.rs` | `set_mtu` | 318 | 1 | OBLIGATION | refinement type error |
| `src/wire/ndiscoption.rs` | `clear_prefix_reserved` | 355 | 1 | OBLIGATION | refinement type error |
| `src/wire/ndiscoption.rs` | `set_prefix` | 363 | 1 | OBLIGATION | refinement type error |
| `src/wire/ndiscoption.rs` | `clear_redirected_reserved` | 374 | 1 | OBLIGATION | refinement type error |
| `src/wire/ndiscoption.rs` | `parse` | 449 | 1 | OBLIGATION | call to core[a8c6]::iter::traits::exact_size::ExactSizeIterator::len m |
| `src/wire/sixlowpan/iphc.rs` | `next_header` | 122 | 1 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `hop_limit` | 141 | 1 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `payload` | 449 | 1 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `set_dispatch_field` | 467 | 1 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `buffer_len` | 763 | 1 | OBLIGATION | call to core[a8c6]::array::equality::{impl#2}::eq may panic: MightPani |
| `src/wire/sixlowpan/nhc.rs` | `src_port` | 521 | 1 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/wire/sixlowpan/nhc.rs` | `checksum` | 586 | 1 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/nhc.rs` | `set_dispatch_field` | 638 | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/sixlowpan/nhc.rs` | `set_checksum` | 687 | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `sub` | 55 | 1 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/wire/tcp.rs` | `options` | 393 | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `payload` | 402 | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `set_src_port` | 413 | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `set_dst_port` | 421 | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `set_seq_number` | 429 | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `set_ack_number` | 437 | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `set_window_len` | 580 | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `set_urgent_at` | 595 | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `options_mut` | 620 | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `payload_mut` | 629 | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `emit` | 1014 | 1 | OBLIGATION | call to core[a8c6]::slice::iter::{impl#166}::any may panic: MightPanic |
| `src/wire/udp.rs` | `len` | 93 | 1 | OBLIGATION | refinement type error |
| `src/wire/udp.rs` | `checksum` | 101 | 1 | OBLIGATION | refinement type error |
| `src/wire/udp.rs` | `verify_checksum` | 132 | 1 | OBLIGATION | refinement type error |
| `src/wire/udp.rs` | `payload` | 157 | 1 | OBLIGATION | refinement type error |
| `src/wire/udp.rs` | `fill_checksum` | 203 | 1 | OBLIGATION | refinement type error |
