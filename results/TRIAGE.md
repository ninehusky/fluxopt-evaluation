# Breadth triage: what happens if every panic-holding function is checked

190 functions, 353 panic sites, 35 files.

| sites | outcome |
| ---: | --- |
| 342 | OBLIGATION |
| 18 | CLEAN |
| 8 | ICE |

| file | fn | sites | outcome | first error |
| --- | --- | ---: | --- | --- |
| `src/wire/sixlowpan/nhc.rs` | `set_ports` | 3 | CLEAN |  |
| `src/wire/tcp.rs` | `parse` | 3 | CLEAN |  |
| `src/socket/tcp.rs` | `process` | 2 | CLEAN |  |
| `src/wire/mld.rs` | `set_mcast_addr` | 2 | CLEAN |  |
| `src/wire/sixlowpan/nhc.rs` | `payload_mut` | 2 | CLEAN |  |
| `src/socket/tcp.rs` | `new` | 1 | CLEAN |  |
| `src/wire/dhcpv4.rs` | `emit` | 1 | CLEAN |  |
| `src/wire/mld.rs` | `num_srcs` | 1 | CLEAN |  |
| `src/wire/mld.rs` | `mcast_addr` | 1 | CLEAN |  |
| `src/wire/mod.rs` | `as_bytes` | 1 | CLEAN |  |
| `src/wire/sixlowpan/nhc.rs` | `set_dispatch_field` | 1 | CLEAN |  |
| `src/iface/interface/mod.rs` | `dispatch_ip` | 3 | ICE | rustc aborted; quarantine candidate |
| `src/iface/interface/mod.rs` | `new` | 1 | ICE | rustc aborted; quarantine candidate |
| `src/iface/interface/mod.rs` | `new` | 1 | ICE | rustc aborted; quarantine candidate |
| `src/iface/interface/mod.rs` | `socket_egress` | 1 | ICE | rustc aborted; quarantine candidate |
| `src/iface/interface/mod.rs` | `check_ip_addrs` | 1 | ICE | rustc aborted; quarantine candidate |
| `src/iface/interface/mod.rs` | `lookup_hardware_addr` | 1 | ICE | rustc aborted; quarantine candidate |
| `src/iface/socket_set.rs` | `get_mut` | 21 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/wire/tcp.rs` | `add` | 7 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/iface/packet.rs` | `emit_payload` | 6 | OBLIGATION | refinement type error |
| `src/iface/packet.rs` | `as_sixlowpan_next_header` | 6 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/wire/tcp.rs` | `sub` | 6 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/wire/tcp.rs` | `sub` | 6 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/iface/interface/sixlowpan.rs` | `ipv6_to_sixlowpan` | 5 | OBLIGATION | refinement type error |
| `src/storage/ring_buffer.rs` | `dequeue_many_with` | 5 | OBLIGATION | internal flux error: crates/flux-infer/src/infer.rs:888:22 |
| `src/wire/icmpv6.rs` | `payload` | 5 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/mod.rs` | `resolve` | 5 | OBLIGATION | call to core[a8c6]::slice::{impl#0}::copy_from_slice may panic: MightP |
| `src/storage/ring_buffer.rs` | `get_idx_unchecked` | 4 | OBLIGATION | assertion might fail: possible remainder with a divisor of zero |
| `src/wire/icmpv6.rs` | `clear_reserved` | 4 | OBLIGATION | refinement type error |
| `src/wire/ip.rs` | `pseudo_header` | 4 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/wire/ipv6.rs` | `set_flow_label` | 4 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/iface/interface/sixlowpan.rs` | `decompress_ext_hdr` | 3 | OBLIGATION | refinement type error |
| `src/iface/interface/sixlowpan.rs` | `decompress_udp` | 3 | OBLIGATION | refinement type error |
| `src/iface/socket_set.rs` | `get` | 3 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/storage/ring_buffer.rs` | `dequeue_one_with` | 3 | OBLIGATION | internal flux error: crates/flux-infer/src/infer.rs:888:22 |
| `src/wire/ethernet.rs` | `set_src_addr` | 3 | OBLIGATION | refinement type error |
| `src/wire/ethernet.rs` | `set_ethertype` | 3 | OBLIGATION | refinement type error |
| `src/wire/icmpv6.rs` | `set_msg_code` | 3 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6.rs` | `set_traffic_class` | 3 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6.rs` | `set_payload_len` | 3 | OBLIGATION | refinement type error |
| `src/wire/ipv6.rs` | `set_hop_limit` | 3 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6.rs` | `set_src_addr` | 3 | OBLIGATION | refinement type error |
| `src/wire/ipv6.rs` | `set_dst_addr` | 3 | OBLIGATION | call to core[a8c6]::slice::{impl#0}::copy_from_slice may panic: MightP |
| `src/wire/ipv6option.rs` | `data_mut` | 3 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `dst_addr` | 3 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/nhc.rs` | `payload` | 3 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/nhc.rs` | `payload` | 3 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `parse` | 3 | OBLIGATION | call to core[a8c6]::iter::traits::iterator::Iterator::for_each may pan |
| `src/wire/udp.rs` | `set_src_port` | 3 | OBLIGATION | call to byteorder[387c]::{impl#2}::write_u16 may panic: MightPanic(NoM |
| `src/wire/udp.rs` | `set_dst_port` | 3 | OBLIGATION | call to byteorder[387c]::{impl#2}::write_u16 may panic: MightPanic(NoM |
| `src/wire/udp.rs` | `set_len` | 3 | OBLIGATION | refinement type error |
| `src/iface/interface/ipv6.rs` | `get_source_address_ipv6` | 2 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/iface/interface/sixlowpan.rs` | `dispatch_sixlowpan` | 2 | OBLIGATION | refinement type error |
| `src/iface/neighbor.rs` | `fill_with_expiration` | 2 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/iface/neighbor.rs` | `lookup` | 2 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/iface/route.rs` | `lookup` | 2 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/iface/socket_set.rs` | `add` | 2 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/iface/socket_set.rs` | `remove` | 2 | OBLIGATION | call to managed[ba83]::slice::{impl#3}::deref_mut may panic: MightPani |
| `src/socket/dhcpv4.rs` | `process` | 2 | OBLIGATION | call to core[a8c6]::cmp::PartialEq::ne may panic: MightPanic(Transitiv |
| `src/storage/packet_buffer.rs` | `dequeue_with` | 2 | OBLIGATION | internal flux error: crates/flux-infer/src/infer.rs:888:22 |
| `src/storage/ring_buffer.rs` | `enqueue_many_with` | 2 | OBLIGATION | internal flux error: crates/flux-infer/src/infer.rs:888:22 |
| `src/storage/ring_buffer.rs` | `get_allocated` | 2 | OBLIGATION | call to managed[ba83]::slice::{impl#2}::deref may panic: MightPanic(No |
| `src/wire/dhcpv4.rs` | `set_sname_and_boot_file_to_zero` | 2 | OBLIGATION | call to core[a8c6]::slice::iter::{impl#174}::next may panic: MightPani |
| `src/wire/icmpv4.rs` | `emit` | 2 | OBLIGATION | call to core[a8c6]::slice::{impl#0}::copy_from_slice may panic: MightP |
| `src/wire/icmpv6.rs` | `set_msg_type` | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/icmpv6.rs` | `payload_mut` | 2 | OBLIGATION | refinement type error |
| `src/wire/icmpv6.rs` | `emit` | 2 | OBLIGATION | refinement type error |
| `src/wire/ieee802154.rs` | `frame_type` | 2 | OBLIGATION | call to byteorder[387c]::{impl#3}::read_u16 may panic: MightPanic(NoMI |
| `src/wire/ieee802154.rs` | `addressing_fields` | 2 | OBLIGATION | refinement type error |
| `src/wire/ipv4.rs` | `set_version` | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv4.rs` | `set_dscp` | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv4.rs` | `set_total_len` | 2 | OBLIGATION | refinement type error |
| `src/wire/ipv4.rs` | `set_ident` | 2 | OBLIGATION | refinement type error |
| `src/wire/ipv4.rs` | `clear_flags` | 2 | OBLIGATION | refinement type error |
| `src/wire/ipv4.rs` | `set_hop_limit` | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv4.rs` | `set_next_header` | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv4.rs` | `set_src_addr` | 2 | OBLIGATION | refinement type error |
| `src/wire/ipv4.rs` | `set_dst_addr` | 2 | OBLIGATION | refinement type error |
| `src/wire/ipv6.rs` | `mask` | 2 | OBLIGATION | call to core[a8c6]::slice::{impl#0}::copy_from_slice may panic: MightP |
| `src/wire/ipv6.rs` | `payload_len` | 2 | OBLIGATION | call to byteorder[387c]::{impl#2}::read_u16 may panic: MightPanic(NoMI |
| `src/wire/ipv6.rs` | `set_version` | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6hbh.rs` | `emit` | 2 | OBLIGATION | refinement type error |
| `src/wire/ipv6option.rs` | `set_data_len` | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/mld.rs` | `set_mcast_addr` | 2 | OBLIGATION | call to core[a8c6]::net::ip_addr::{impl#20}::is_multicast may panic: M |
| `src/wire/mod.rs` | `ethernet_or_panic` | 2 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/wire/ndisc.rs` | `set_target_addr` | 2 | OBLIGATION | call to core[a8c6]::slice::{impl#0}::copy_from_slice may panic: MightP |
| `src/wire/ndiscoption.rs` | `set_data_len` | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ndiscoption.rs` | `data_mut` | 2 | OBLIGATION | refinement type error |
| `src/wire/ndiscoption.rs` | `emit` | 2 | OBLIGATION | call to core[a8c6]::slice::{impl#0}::copy_from_slice may panic: MightP |
| `src/wire/sixlowpan/iphc.rs` | `flow_label_field` | 2 | OBLIGATION | call to byteorder[387c]::{impl#2}::read_u16 may panic: MightPanic(NoMI |
| `src/wire/sixlowpan/iphc.rs` | `set_field` | 2 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/nhc.rs` | `length` | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/sixlowpan/nhc.rs` | `dst_port` | 2 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/sixlowpan/nhc.rs` | `payload_mut` | 2 | OBLIGATION | refinement type error |
| `src/wire/udp.rs` | `set_checksum` | 2 | OBLIGATION | refinement type error |
| `src/wire/udp.rs` | `payload_mut` | 2 | OBLIGATION | refinement type error |
| `src/iface/interface/ipv6.rs` | `process_hopbyhop` | 1 | OBLIGATION | call to core[a8c6]::slice::iter::{impl#166}::next may panic: MightPani |
| `src/iface/interface/sixlowpan.rs` | `process_sixlowpan` | 1 | OBLIGATION | call to core[a8c6]::array::{impl#15}::index may panic: MightPanic(Tran |
| `src/phy/mod.rs` | `from_driver` | 1 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/socket/dhcpv4.rs` | `dispatch` | 1 | OBLIGATION | call to core[a8c6]::result::{impl#28}::from_residual may panic: MightP |
| `src/socket/tcp.rs` | `new` | 1 | OBLIGATION | call to core[a8c6]::num::{impl#11}::leading_zeros may panic: MightPani |
| `src/socket/tcp.rs` | `seq_to_transmit` | 1 | OBLIGATION | arithmetic operation may underflow |
| `src/socket/udp.rs` | `process` | 1 | OBLIGATION | call to core[a8c6]::slice::{impl#0}::copy_from_slice may panic: MightP |
| `src/storage/assembler.rs` | `add` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/storage/packet_buffer.rs` | `dequeue` | 1 | OBLIGATION | call to core[a8c6]::option::{impl#0}::unwrap may panic: MightPanic(Tra |
| `src/storage/packet_buffer.rs` | `peek` | 1 | OBLIGATION | call to core[a8c6]::option::{impl#0}::unwrap may panic: MightPanic(Tra |
| `src/storage/ring_buffer.rs` | `get_unallocated` | 1 | OBLIGATION | refinement type error |
| `src/storage/ring_buffer.rs` | `enqueue_unallocated` | 1 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/storage/ring_buffer.rs` | `dequeue_allocated` | 1 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/wire/arp.rs` | `set_hardware_type` | 1 | OBLIGATION | refinement type error |
| `src/wire/arp.rs` | `set_protocol_type` | 1 | OBLIGATION | refinement type error |
| `src/wire/arp.rs` | `set_hardware_len` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/arp.rs` | `set_protocol_len` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/arp.rs` | `set_operation` | 1 | OBLIGATION | call to byteorder[387c]::{impl#2}::write_u16 may panic: MightPanic(NoM |
| `src/wire/arp.rs` | `set_source_hardware_addr` | 1 | OBLIGATION | refinement type error |
| `src/wire/arp.rs` | `set_source_protocol_addr` | 1 | OBLIGATION | refinement type error |
| `src/wire/arp.rs` | `set_target_hardware_addr` | 1 | OBLIGATION | refinement type error |
| `src/wire/arp.rs` | `set_target_protocol_addr` | 1 | OBLIGATION | refinement type error |
| `src/wire/dhcpv4.rs` | `set_magic_number` | 1 | OBLIGATION | call to byteorder[387c]::{impl#2}::write_u32 may panic: MightPanic(NoM |
| `src/wire/dhcpv4.rs` | `emit` | 1 | OBLIGATION | call to core[a8c6]::array::{impl#16}::index_mut may panic: MightPanic( |
| `src/wire/ethernet.rs` | `from_bytes` | 1 | OBLIGATION | call to core[a8c6]::slice::{impl#0}::copy_from_slice may panic: MightP |
| `src/wire/icmpv4.rs` | `set_msg_code` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/icmpv4.rs` | `set_echo_ident` | 1 | OBLIGATION | refinement type error |
| `src/wire/icmpv4.rs` | `set_echo_seq_no` | 1 | OBLIGATION | call to byteorder[387c]::{impl#2}::write_u16 may panic: MightPanic(NoM |
| `src/wire/icmpv4.rs` | `data_mut` | 1 | OBLIGATION | refinement type error |
| `src/wire/icmpv6.rs` | `set_echo_ident` | 1 | OBLIGATION | refinement type error |
| `src/wire/icmpv6.rs` | `set_echo_seq_no` | 1 | OBLIGATION | refinement type error |
| `src/wire/icmpv6.rs` | `parse` | 1 | OBLIGATION | call to xarxa_driver[1613]::{impl#1}::rx may panic: MightPanic(NoMIRAv |
| `src/wire/ieee802154.rs` | `dst_addressing_mode` | 1 | OBLIGATION | refinement type error |
| `src/wire/ieee802154.rs` | `src_addressing_mode` | 1 | OBLIGATION | refinement type error |
| `src/wire/ieee802154.rs` | `src_pan_id` | 1 | OBLIGATION | refinement type error |
| `src/wire/ieee802154.rs` | `payload` | 1 | OBLIGATION | refinement type error |
| `src/wire/ipv4.rs` | `new` | 1 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/wire/ipv4.rs` | `verify_checksum` | 1 | OBLIGATION | refinement type error |
| `src/wire/ipv4.rs` | `payload` | 1 | OBLIGATION | refinement type error |
| `src/wire/ipv6.rs` | `solicited_node` | 1 | OBLIGATION | call to core[a8c6]::panicking::panic may panic: MightPanic(NoMIRAvaila |
| `src/wire/ipv6.rs` | `src_addr` | 1 | OBLIGATION | call to core[a8c6]::result::{impl#0}::unwrap may panic: MightPanic(Tra |
| `src/wire/ipv6.rs` | `dst_addr` | 1 | OBLIGATION | refinement type error |
| `src/wire/ipv6.rs` | `payload` | 1 | OBLIGATION | refinement type error |
| `src/wire/ipv6.rs` | `set_next_header` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6.rs` | `payload_mut` | 1 | OBLIGATION | refinement type error |
| `src/wire/ipv6ext_header.rs` | `set_next_header` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6ext_header.rs` | `set_header_len` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6option.rs` | `set_option_type` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ipv6option.rs` | `emit` | 1 | OBLIGATION | call to core[a8c6]::slice::{impl#0}::copy_from_slice may panic: MightP |
| `src/wire/mld.rs` | `mcast_addr` | 1 | OBLIGATION | refinement type error |
| `src/wire/mld.rs` | `s_flag` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/mld.rs` | `qqic` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/mld.rs` | `num_srcs` | 1 | OBLIGATION | call to byteorder[387c]::{impl#2}::read_u16 may panic: MightPanic(NoMI |
| `src/wire/mld.rs` | `set_qrv` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/mld.rs` | `set_qqic` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/mld.rs` | `set_num_srcs` | 1 | OBLIGATION | refinement type error |
| `src/wire/mld.rs` | `set_num_srcs` | 1 | OBLIGATION | call to byteorder[387c]::{impl#2}::write_u16 may panic: MightPanic(NoM |
| `src/wire/mod.rs` | `ieee802154_or_panic` | 1 | OBLIGATION | call to core[a8c6]::panicking::panic_fmt may panic: MightPanic(NoMIRAv |
| `src/wire/mod.rs` | `as_bytes` | 1 | OBLIGATION | call to core[a8c6]::array::{impl#15}::index may panic: MightPanic(Tran |
| `src/wire/ndisc.rs` | `reachable_time` | 1 | OBLIGATION | refinement type error |
| `src/wire/ndisc.rs` | `retrans_time` | 1 | OBLIGATION | refinement type error |
| `src/wire/ndisc.rs` | `target_addr` | 1 | OBLIGATION | refinement type error |
| `src/wire/ndisc.rs` | `dest_addr` | 1 | OBLIGATION | call to core[a8c6]::result::{impl#0}::unwrap may panic: MightPanic(Tra |
| `src/wire/ndisc.rs` | `set_current_hop_limit` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ndisc.rs` | `set_router_flags` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ndisc.rs` | `set_router_lifetime` | 1 | OBLIGATION | refinement type error |
| `src/wire/ndisc.rs` | `set_reachable_time` | 1 | OBLIGATION | refinement type error |
| `src/wire/ndisc.rs` | `set_retrans_time` | 1 | OBLIGATION | refinement type error |
| `src/wire/ndisc.rs` | `set_dest_addr` | 1 | OBLIGATION | refinement type error |
| `src/wire/ndisc.rs` | `parse` | 1 | OBLIGATION | refinement type error |
| `src/wire/ndisc.rs` | `emit` | 1 | OBLIGATION | refinement type error |
| `src/wire/ndiscoption.rs` | `set_option_type` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/ndiscoption.rs` | `set_link_layer_addr` | 1 | OBLIGATION | refinement type error |
| `src/wire/ndiscoption.rs` | `set_mtu` | 1 | OBLIGATION | refinement type error |
| `src/wire/ndiscoption.rs` | `clear_prefix_reserved` | 1 | OBLIGATION | refinement type error |
| `src/wire/ndiscoption.rs` | `set_prefix` | 1 | OBLIGATION | refinement type error |
| `src/wire/ndiscoption.rs` | `clear_redirected_reserved` | 1 | OBLIGATION | refinement type error |
| `src/wire/ndiscoption.rs` | `parse` | 1 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `next_header` | 1 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `hop_limit` | 1 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `payload` | 1 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `set_dispatch_field` | 1 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/iphc.rs` | `buffer_len` | 1 | OBLIGATION | call to core[a8c6]::array::{impl#15}::index may panic: MightPanic(Tran |
| `src/wire/sixlowpan/nhc.rs` | `src_port` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/sixlowpan/nhc.rs` | `checksum` | 1 | OBLIGATION | refinement type error |
| `src/wire/sixlowpan/nhc.rs` | `set_dispatch_field` | 1 | OBLIGATION | assertion might fail: possible out-of-bounds access |
| `src/wire/sixlowpan/nhc.rs` | `set_checksum` | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `options` | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `payload` | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `set_src_port` | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `set_dst_port` | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `set_seq_number` | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `set_ack_number` | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `set_window_len` | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `set_urgent_at` | 1 | OBLIGATION | call to byteorder[387c]::{impl#2}::write_u16 may panic: MightPanic(NoM |
| `src/wire/tcp.rs` | `options_mut` | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `payload_mut` | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `emit` | 1 | OBLIGATION | refinement type error |
| `src/wire/tcp.rs` | `emit` | 1 | OBLIGATION | call to core[a8c6]::slice::iter::{impl#166}::any may panic: MightPanic |
| `src/wire/udp.rs` | `len` | 1 | OBLIGATION | refinement type error |
| `src/wire/udp.rs` | `checksum` | 1 | OBLIGATION | refinement type error |
| `src/wire/udp.rs` | `verify_checksum` | 1 | OBLIGATION | refinement type error |
| `src/wire/udp.rs` | `payload` | 1 | OBLIGATION | refinement type error |
| `src/wire/udp.rs` | `fill_checksum` | 1 | OBLIGATION | refinement type error |
