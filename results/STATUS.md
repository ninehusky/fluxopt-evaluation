# Panic removal: status

Measured 2026-08-11 against the linked nRF52840 `usb_ethernet` firmware. Regenerate with `./status.py`.

## The budget

What removing panics is worth, measured by rebuilding the real firmware with the checks ablated to `get_unchecked`.

| | flash | `.text` | `.rodata` | panic sites | xarxa sites |
| --- | ---: | ---: | ---: | ---: | ---: |
| today | 155404 | 136620 | 18448 | 650 | 439 |
| **ceiling** (every xarxa panic gone) | **131188** | 121468 | 9384 | 244 | 53 |
| delta | **-24216** (-15.58%) | -15152 (-11.09%) | -9064 (-49.13%) | -406 | -386 |

**`.rodata` nearly halves** -- 9064 B, 37% of the whole win. That is panic message strings and `core::panic::Location` structs, and they are SHARED: they are freed when the last user dies, not gradually. Expect a partial effort to look sublinear and the final files to pay disproportionately.

53 xarxa sites survive even full ablation, so 386 of 439 is the real target.

## Progress

| | sites | flash |
| --- | ---: | ---: |
| removed so far | **0** | **0** |
| the 8-file CHURN batch, if completed | 94 | -3624 |
| ceiling | 406 | -24216 |

Nothing has been removed yet: every branch so far is proof-only. A site leaves the binary when a discharged obligation LICENSES replacing the checked operation with `get_unchecked` -- and only after `check_proof.py` passes for that file. A trusted shim is not a fix; it assumes the obligation.

## By file

`churn` is the tractable work: state a length or range precondition and discharge it. Sorted by it. `Δ alone` is that file's CHURN lines ablated on their own -- see the caveats, most of those are inside the noise floor individually.

| file | sites | churn | panic | core | bug/ICE | other | Δ alone | owner |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [`src/wire/ipv6.rs`](#srcwireipv6rs) | 33 | 22 | 3 | 6 | 0 | 2 | -416 | andrew |
| [`src/wire/ipv4.rs`](#srcwireipv4rs) | 21 | 20 | 1 | 0 | 0 | 0 | -212 | agent |
| [`src/wire/icmpv6.rs`](#srcwireicmpv6rs) | 26 | 18 | 0 | 3 | 0 | 5 | -180 | andrew |
| [`src/wire/udp.rs`](#srcwireudprs) | 18 | 18 | 0 | 0 | 0 | 0 | -628 | agent |
| [`src/wire/ndisc.rs`](#srcwirendiscrs) | 16 | 12 | 0 | 2 | 0 | 2 | -204 | andrew |
| [`src/wire/sixlowpan/nhc.rs`](#srcwiresixlowpannhcrs) | 25 | 12 | 3 | 0 | 0 | 10 | -220 | agent |
| [`src/wire/arp.rs`](#srcwirearprs) | 9 | 9 | 0 | 0 | 0 | 0 | 84 | blocked: const fn new_unchecked |
| [`src/wire/ndiscoption.rs`](#srcwirendiscoptionrs) | 13 | 9 | 0 | 4 | 0 | 0 | -128 | agent |
| [`src/wire/sixlowpan/iphc.rs`](#srcwiresixlowpaniphcrs) | 49 | 8 | 4 | 0 | 0 | 37 | -- |  |
| [`src/wire/tcp.rs`](#srcwiretcprs) | 34 | 8 | 20 | 6 | 0 | 0 | -- |  |
| [`src/wire/ethernet.rs`](#srcwireethernetrs) | 7 | 7 | 0 | 0 | 0 | 0 | -- |  |
| [`src/wire/ipv6option.rs`](#srcwireipv6optionrs) | 7 | 6 | 0 | 1 | 0 | 0 | -- |  |
| [`src/wire/mld.rs`](#srcwiremldrs) | 18 | 6 | 3 | 1 | 0 | 8 | -- |  |
| [`src/storage/ring_buffer.rs`](#srcstorageringbufferrs) | 20 | 4 | 2 | 3 | 10 | 1 | -- |  |
| [`src/wire/icmpv4.rs`](#srcwireicmpv4rs) | 8 | 4 | 0 | 2 | 0 | 2 | -- |  |
| [`src/iface/interface/sixlowpan.rs`](#srcifaceinterfacesixlowpanrs) | 16 | 3 | 7 | 4 | 0 | 2 | -- |  |
| [`src/wire/ieee802154.rs`](#srcwireieee802154rs) | 18 | 3 | 0 | 5 | 0 | 10 | -- |  |
| [`src/wire/ipv6ext_header.rs`](#srcwireipv6extheaderrs) | 2 | 2 | 0 | 0 | 0 | 0 | -- |  |
| [`src/wire/dhcpv4.rs`](#srcwiredhcpv4rs) | 4 | 1 | 0 | 3 | 0 | 0 | -- |  |
| [`src/iface/interface/ipv6.rs`](#srcifaceinterfaceipv6rs) | 3 | 0 | 2 | 1 | 0 | 0 | -- |  |
| [`src/iface/interface/mod.rs`](#srcifaceinterfacemodrs) | 7 | 0 | 0 | 0 | 7 | 0 | -- |  |
| [`src/iface/neighbor.rs`](#srcifaceneighborrs) | 4 | 0 | 4 | 0 | 0 | 0 | -- |  |
| [`src/iface/packet.rs`](#srcifacepacketrs) | 12 | 0 | 12 | 0 | 0 | 0 | -- |  |
| [`src/iface/route.rs`](#srcifacerouters) | 2 | 0 | 2 | 0 | 0 | 0 | -- |  |
| [`src/iface/socket_set.rs`](#srcifacesocketsetrs) | 28 | 0 | 28 | 0 | 0 | 0 | -- |  |
| [`src/phy/mod.rs`](#srcphymodrs) | 1 | 0 | 1 | 0 | 0 | 0 | -- |  |
| [`src/socket/dhcpv4.rs`](#srcsocketdhcpv4rs) | 3 | 0 | 3 | 0 | 0 | 0 | -- |  |
| [`src/socket/tcp.rs`](#srcsockettcprs) | 8 | 0 | 1 | 1 | 0 | 6 | -- |  |
| [`src/socket/udp.rs`](#srcsocketudprs) | 1 | 0 | 1 | 0 | 0 | 0 | -- |  |
| [`src/storage/assembler.rs`](#srcstorageassemblerrs) | 1 | 0 | 0 | 1 | 0 | 0 | -- |  |
| [`src/storage/packet_buffer.rs`](#srcstoragepacketbufferrs) | 5 | 0 | 1 | 1 | 2 | 1 | -- |  |
| [`src/wire/ip.rs`](#srcwireiprs) | 4 | 0 | 4 | 0 | 0 | 0 | -- |  |
| [`src/wire/ipv6hbh.rs`](#srcwireipv6hbhrs) | 2 | 0 | 0 | 2 | 0 | 0 | -- |  |
| [`src/wire/mod.rs`](#srcwiremodrs) | 4 | 0 | 3 | 1 | 0 | 0 | -- |  |
| [`src/wire/sixlowpan/mod.rs`](#srcwiresixlowpanmodrs) | 10 | 0 | 0 | 5 | 0 | 5 | -- |  |
| **total** | **439** | **172** | **105** | **52** | **19** | **91** | | |

`other` is mostly UNATTRIBUTED: a site the blame data puts in this file but that falls outside any function the triage parser recognised -- macro bodies, derives, closures. Those sites are real and counted in the metric; they just have no Flux obligation attached yet.

## Every panic site, by file

One row per source line. `sites` exceeds lines because generics and inlining duplicate a line into several machine call sites -- lines track effort, sites track the metric. A `?` line means DWARF blamed the file but no statement.

<a id="srcwireipv6rs"></a>
### `src/wire/ipv6.rs`

33 sites across 17 lines. churn 22, panic 3, core 6. Owner: andrew.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| ? | 2 | bounds-check | UNATTRIBUTED | `` | `` |
| 163 | 2 | panic!/unreachable! | PANIC | `mask` | `assert!(mask <= 128);` |
| 178 | 1 | panic!/unreachable! | PANIC | `solicited_node` | `assert!(self.x_is_unicast());` |
| 448 | 2 | slice-index | CHURN | `payload_len` | `NetworkEndian::read_u16(&data[field::LENGTH])` |
| 475 | 1 | slice-index | CORE | `src_addr` | `Address::from_octets(data[field::SRC_ADDR].try_into().unwrap())` |
| 482 | 1 | slice-index | CORE | `dst_addr` | `Address::from_octets(data[field::DST_ADDR].try_into().unwrap())` |
| 492 | 1 | slice-index | CHURN | `payload` | `&data[range]` |
| 503 | 2 | bounds-check | CHURN | `set_version` | `data[0] = (data[0] & 0x0f) \| ((value & 0x0f) << 4);` |
| 515 | 3 | bounds-check | CHURN | `set_traffic_class` | `data[1] = (data[1] & 0x0f) \| ((value & 0x0f) << 4);` |
| 523 | 1 | bounds-check | CORE | `set_flow_label` | `let raw = (((data[1] & 0xf0) as u32) << 16) \| (value & 0x0fffff);` |
| 524 | 3 | slice-index | CORE | `set_flow_label` | `NetworkEndian::write_u24(&mut data[1..4], raw);` |
| 531 | 3 | slice-index | CHURN | `set_payload_len` | `NetworkEndian::write_u16(&mut data[field::LENGTH], value);` |
| 538 | 1 | bounds-check | CHURN | `set_next_header` | `data[field::NXT_HDR] = value.into();` |
| 545 | 3 | bounds-check | CHURN | `set_hop_limit` | `data[field::HOP_LIMIT] = value;` |
| 552 | 3 | slice-index | CHURN | `set_src_addr` | `data[field::SRC_ADDR].copy_from_slice(&value.octets());` |
| 559 | 3 | slice-index | CHURN | `set_dst_addr` | `data[field::DST_ADDR].copy_from_slice(&value.octets());` |
| 567 | 1 | slice-index | CHURN | `payload_mut` | `&mut data[range]` |

<a id="srcwireipv4rs"></a>
### `src/wire/ipv4.rs`

21 sites across 12 lines. churn 20, panic 1, core 0. Owner: agent.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 101 | 1 | panic!/unreachable! | PANIC | `new` | `assert!(prefix_len <= 32);` |
| 369 | 1 | slice-index | CHURN | `verify_checksum` | `checksum::data(&data[..self.header_len() as usize]) == !0` |
| 389 | 1 | slice-index | CHURN | `payload` | `&data[range]` |
| 398 | 2 | bounds-check | CHURN | `set_version` | `data[field::VER_IHL] = (data[field::VER_IHL] & !0xf0) \| (value << 4);` |
| 411 | 2 | bounds-check | CHURN | `set_dscp` | `data[field::DSCP_ECN] = (data[field::DSCP_ECN] & !0xfc) \| (value << 2)` |
| 424 | 2 | slice-index | CHURN | `set_total_len` | `NetworkEndian::write_u16(&mut data[field::LENGTH], value)` |
| 431 | 2 | slice-index | CHURN | `set_ident` | `NetworkEndian::write_u16(&mut data[field::IDENT], value)` |
| 438 | 2 | slice-index | CHURN | `clear_flags` | `let raw = NetworkEndian::read_u16(&data[field::FLG_OFF]);` |
| 474 | 2 | bounds-check | CHURN | `set_hop_limit` | `data[field::TTL] = value` |
| 481 | 2 | bounds-check | CHURN | `set_next_header` | `data[field::PROTOCOL] = value.into()` |
| 495 | 2 | slice-index | CHURN | `set_src_addr` | `data[field::SRC_ADDR].copy_from_slice(&value.octets())` |
| 502 | 2 | slice-index | CHURN | `set_dst_addr` | `data[field::DST_ADDR].copy_from_slice(&value.octets())` |

<a id="srcwireicmpv6rs"></a>
### `src/wire/icmpv6.rs`

26 sites across 13 lines. churn 18, panic 0, core 3. Owner: andrew.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| ? | 5 | slice-index | UNATTRIBUTED | `` | `` |
| 458 | 5 | slice-index | CHURN | `payload` | `&data[self.header_len()..]` |
| 470 | 2 | bounds-check | CHURN | `set_msg_type` | `data[field::TYPE] = value.into()` |
| 479 | 3 | bounds-check | CHURN | `set_msg_code` | `data[field::CODE] = value` |
| 502 | 2 | slice-index | CHURN | `clear_reserved` | `NetworkEndian::write_u32(&mut data[field::UNUSED], 0);` |
| 507 | 1 | bounds-check | CHURN | `clear_reserved` | `data[field::SQRV] &= 0xf;` |
| 511 | 1 | slice-index | CHURN | `clear_reserved` | `NetworkEndian::write_u16(&mut data[field::RECORD_RESV], 0);` |
| 544 | 1 | slice-index | CHURN | `set_echo_ident` | `NetworkEndian::write_u16(&mut data[field::ECHO_IDENT], value)` |
| 554 | 1 | slice-index | CHURN | `set_echo_seq_no` | `NetworkEndian::write_u16(&mut data[field::ECHO_SEQNO], value)` |
| 600 | 2 | slice-index | CHURN | `payload_mut` | `&mut data[range]` |
| 680 | 1 | slice-index | CORE | `parse` | `let payload = &packet.payload()[ip_packet.header_len()..];` |
| 787 | 1 | slice-index | CORE | `emit` | `let payload = &mut ip_packet.into_inner()[header.buffer_len()..];` |
| 794 | 1 | slice-index | CORE | `emit` | `payload[..payload_len].copy_from_slice(&data[..payload_len]);` |

<a id="srcwireudprs"></a>
### `src/wire/udp.rs`

18 sites across 10 lines. churn 18, panic 0, core 0. Owner: agent.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 94 | 1 | slice-index | CHURN | `len` | `NetworkEndian::read_u16(&data[field::LENGTH])` |
| 101 | 1 | slice-index | CHURN | `checksum` | `NetworkEndian::read_u16(&data[field::CHECKSUM])` |
| 145 | 1 | slice-index | CHURN | `verify_checksum` | `checksum::data(&data[..self.len() as usize]),` |
| 156 | 1 | slice-index | CHURN | `payload` | `&data[field::PAYLOAD(length)]` |
| 165 | 3 | slice-index | CHURN | `set_src_port` | `NetworkEndian::write_u16(&mut data[field::SRC_PORT], value)` |
| 172 | 3 | slice-index | CHURN | `set_dst_port` | `NetworkEndian::write_u16(&mut data[field::DST_PORT], value)` |
| 179 | 3 | slice-index | CHURN | `set_len` | `NetworkEndian::write_u16(&mut data[field::LENGTH], value)` |
| 186 | 2 | slice-index | CHURN | `set_checksum` | `NetworkEndian::write_u16(&mut data[field::CHECKSUM], value)` |
| 200 | 1 | slice-index | CHURN | `fill_checksum` | `checksum::data(&data[..self.len() as usize]),` |
| 215 | 2 | slice-index | CHURN | `payload_mut` | `&mut data[field::PAYLOAD(length)]` |

<a id="srcwirendiscrs"></a>
### `src/wire/ndisc.rs`

16 sites across 14 lines. churn 12, panic 0, core 2. Owner: andrew.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| ? | 2 | slice-index | UNATTRIBUTED | `` | `` |
| 59 | 1 | slice-index | CHURN | `reachable_time` | `Duration::from_millis(NetworkEndian::read_u32(&data[field::REACHABLE_TM]) as u64)` |
| 66 | 1 | slice-index | CHURN | `retrans_time` | `Duration::from_millis(NetworkEndian::read_u32(&data[field::RETRANS_TM]) as u64)` |
| 81 | 1 | slice-index | CORE | `target_addr` | `Ipv6Address::from_octets(data[field::TARGET_ADDR].try_into().unwrap())` |
| 107 | 1 | slice-index | CORE | `dest_addr` | `Ipv6Address::from_octets(data[field::DEST_ADDR].try_into().unwrap())` |
| 120 | 1 | bounds-check | CHURN | `set_current_hop_limit` | `data[field::CUR_HOP_LIMIT] = value;` |
| 126 | 1 | bounds-check | CHURN | `set_router_flags` | `self.buffer.as_mut()[field::ROUTER_FLAGS] = flags.bits();` |
| 133 | 1 | slice-index | CHURN | `set_router_lifetime` | `NetworkEndian::write_u16(&mut data[field::ROUTER_LT], value.secs() as u16);` |
| 140 | 1 | slice-index | CHURN | `set_reachable_time` | `NetworkEndian::write_u32(&mut data[field::REACHABLE_TM], value.total_millis() as u32);` |
| 147 | 1 | slice-index | CHURN | `set_retrans_time` | `NetworkEndian::write_u32(&mut data[field::RETRANS_TM], value.total_millis() as u32);` |
| 162 | 2 | slice-index | CHURN | `set_target_addr` | `data[field::TARGET_ADDR].copy_from_slice(&value.octets());` |
| 187 | 1 | slice-index | CHURN | `set_dest_addr` | `data[field::DEST_ADDR].copy_from_slice(&value.octets());` |
| 240 | 1 | slice-index | CHURN | `parse` | `let pkt = NdiscOption::new_checked(&packet.payload()[offset..])?;` |
| 451 | 1 | slice-index | CHURN | `emit` | `NdiscOption::new_unchecked(&mut packet.payload_mut()[offset..]);` |

<a id="srcwiresixlowpannhcrs"></a>
### `src/wire/sixlowpan/nhc.rs`

25 sites across 15 lines. churn 12, panic 3, core 0. Owner: agent.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| ? | 4 | bounds-check, slice-index | UNATTRIBUTED | `` | `` |
| 16 | 3 | bounds-check | UNATTRIBUTED | `` | `let raw = &data[0];` |
| 179 | 2 | bounds-check | CHURN | `length` | `self.buffer.as_ref()[1 + self.next_header_size()]` |
| 208 | 2 | slice-index | CHURN | `payload` | `&self.buffer.as_ref()[start..][..len]` |
| 525 | 1 | slice-index | PANIC | `src_port` | `NetworkEndian::read_u16(&data[start..start + 2])` |
| 553 | 1 | slice-index | PANIC | `dst_port` | `NetworkEndian::read_u16(&data[idx + 2..idx + 4])` |
| 567 | 1 | slice-index | PANIC | `dst_port` | `NetworkEndian::read_u16(&data[idx + 1..idx + 1 + 2])` |
| 586 | 1 | slice-index | CHURN | `checksum` | `Some(NetworkEndian::read_u16(&data[start..start + 2]))` |
| 618 | 3 | slice-index | CHURN | `payload` | `&self.buffer.as_ref()[start..]` |
| 626 | 2 | slice-index | CHURN | `payload_mut` | `&mut self.buffer.as_mut()[start..]` |
| 632 | 1 | bounds-check | CHURN | `set_dispatch_field` | `data[0] = (data[0] & !(0b11111 << 3)) \| (DISPATCH_UDP_HEADER << 3);` |
| 657 | 1 | slice-index | CLEAN | `set_ports` | `NetworkEndian::write_u16(&mut data[idx..idx + 2], dst_port);` |
| 665 | 1 | bounds-check | CLEAN | `set_ports` | `data[idx] = (dst_port - 0xf000) as u8;` |
| 673 | 1 | slice-index | CLEAN | `set_ports` | `NetworkEndian::write_u16(&mut data[idx..idx + 2], dst_port);` |
| 682 | 1 | slice-index | CHURN | `set_checksum` | `NetworkEndian::write_u16(&mut data[idx..idx + 2], checksum);` |

<a id="srcwirearprs"></a>
### `src/wire/arp.rs`

9 sites across 9 lines. churn 9, panic 0, core 0. Owner: blocked: const fn new_unchecked.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 176 | 1 | slice-index | CHURN | `set_hardware_type` | `NetworkEndian::write_u16(&mut data[field::HTYPE], value.into())` |
| 183 | 1 | slice-index | CHURN | `set_protocol_type` | `NetworkEndian::write_u16(&mut data[field::PTYPE], value.into())` |
| 190 | 1 | bounds-check | CHURN | `set_hardware_len` | `data[field::HLEN] = value` |
| 197 | 1 | bounds-check | CHURN | `set_protocol_len` | `data[field::PLEN] = value` |
| 204 | 1 | slice-index | CHURN | `set_operation` | `NetworkEndian::write_u16(&mut data[field::OPER], value.into())` |
| 214 | 1 | slice-index | CHURN | `set_source_hardware_addr` | `data[field::SHA(hardware_len, protocol_len)].copy_from_slice(value)` |
| 224 | 1 | slice-index | CHURN | `set_source_protocol_addr` | `data[field::SPA(hardware_len, protocol_len)].copy_from_slice(value)` |
| 234 | 1 | slice-index | CHURN | `set_target_hardware_addr` | `data[field::THA(hardware_len, protocol_len)].copy_from_slice(value)` |
| 244 | 1 | slice-index | CHURN | `set_target_protocol_addr` | `data[field::TPA(hardware_len, protocol_len)].copy_from_slice(value)` |

<a id="srcwirendiscoptionrs"></a>
### `src/wire/ndiscoption.rs`

13 sites across 11 lines. churn 9, panic 0, core 4. Owner: agent.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 289 | 1 | bounds-check | CHURN | `set_option_type` | `data[field::TYPE] = value.into();` |
| 296 | 2 | bounds-check | CHURN | `set_data_len` | `data[field::LENGTH] = value;` |
| 306 | 1 | slice-index | CHURN | `set_link_layer_addr` | `data[2..2 + addr.len()].copy_from_slice(addr.as_bytes())` |
| 316 | 1 | slice-index | CHURN | `set_mtu` | `NetworkEndian::write_u32(&mut data[field::MTU], value);` |
| 352 | 1 | slice-index | CHURN | `clear_prefix_reserved` | `NetworkEndian::write_u32(&mut data[field::PREF_RESERVED], 0);` |
| 359 | 1 | slice-index | CHURN | `set_prefix` | `data[field::PREFIX].copy_from_slice(&addr.octets());` |
| 369 | 1 | slice-index | CORE | `clear_redirected_reserved` | `data[field::REDIRECTED_RESERVED].fill_with(\|\| 0);` |
| 379 | 2 | slice-index | CHURN | `data_mut` | `&mut data[field::DATA(len)]` |
| 488 | 1 | slice-index | CORE | `parse` | `data: &redirected_packet[ip_repr.buffer_len()..][..ip_repr.payload_len],` |
| 574 | 1 | copy_from_slice | CORE | `emit` | `ip_packet.payload_mut().copy_from_slice(data);` |
| 588 | 1 | copy_from_slice | CORE | `emit` | `opt.data_mut().copy_from_slice(data);` |

<a id="srcwiresixlowpaniphcrs"></a>
### `src/wire/sixlowpan/iphc.rs`

49 sites across 13 lines. churn 8, panic 4, core 0. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| ? | 35 | bounds-check, slice-index | UNATTRIBUTED | `` | `` |
| 22 | 2 | slice-index | UNATTRIBUTED | `` | `let raw = NetworkEndian::read_u16(&data[field::IPHC_FIELD]);` |
| 133 | 1 | slice-index | CHURN | `next_header` | `let nh = data[start..start + 1][0];` |
| 147 | 1 | slice-index | PANIC | `hop_limit` | `data[start..start + 1][0]` |
| 206 | 1 | slice-index | PANIC | `flow_label_field` | `&self.buffer.as_ref()[start..][2..4],` |
| 212 | 1 | slice-index | PANIC | `flow_label_field` | `&self.buffer.as_ref()[start..][1..3],` |
| 332 | 1 | slice-index | CHURN | `dst_addr` | `AddressMode::Multicast48bits(&data[start..][..6]),` |
| 335 | 1 | slice-index | CHURN | `dst_addr` | `AddressMode::Multicast32bits(&data[start..][..4]),` |
| 338 | 1 | slice-index | CHURN | `dst_addr` | `AddressMode::Multicast8bits(&data[start..][..1]),` |
| 455 | 1 | slice-index | CHURN | `payload` | `&data[len..]` |
| 462 | 1 | slice-index | CHURN | `set_dispatch_field` | `let data = &mut self.buffer.as_mut()[field::IPHC_FIELD];` |
| 481 | 2 | slice-index | CHURN | `set_field` | `raw[idx..idx + value.len()].copy_from_slice(value);` |
| 845 | 1 | panic!/unreachable! | PANIC | `buffer_len` | `_ => unreachable!(),` |

<a id="srcwiretcprs"></a>
### `src/wire/tcp.rs`

34 sites across 23 lines. churn 8, panic 20, core 6. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 44 | 7 | panic!(fmt) | PANIC | `add` | `panic!("attempt to add to sequence number with unsigned overflow")` |
| 55 | 1 | panic!(fmt) | PANIC | `sub` | `panic!("attempt to subtract to sequence number with unsigned overflow")` |
| 73 | 6 | panic!(fmt) | PANIC | `sub` | `panic!("attempt to subtract sequence numbers with underflow")` |
| 392 | 1 | slice-index | CHURN | `options` | `&data[field::OPTIONS(header_len)]` |
| 400 | 1 | slice-index | CHURN | `payload` | `&data[header_len..]` |
| 409 | 1 | slice-index | CHURN | `set_src_port` | `NetworkEndian::write_u16(&mut data[field::SRC_PORT], value)` |
| 416 | 1 | slice-index | CHURN | `set_dst_port` | `NetworkEndian::write_u16(&mut data[field::DST_PORT], value)` |
| 423 | 1 | slice-index | CORE | `set_seq_number` | `NetworkEndian::write_i32(&mut data[field::SEQ_NUM], value.0)` |
| 430 | 1 | slice-index | CORE | `set_ack_number` | `NetworkEndian::write_i32(&mut data[field::ACK_NUM], value.0)` |
| 572 | 1 | slice-index | CHURN | `set_window_len` | `NetworkEndian::write_u16(&mut data[field::WIN_SIZE], value)` |
| 586 | 1 | slice-index | CHURN | `set_urgent_at` | `NetworkEndian::write_u16(&mut data[field::URGENT], value)` |
| 611 | 1 | slice-index | CHURN | `options_mut` | `&mut data[field::OPTIONS(header_len)]` |
| 619 | 1 | slice-index | CHURN | `payload_mut` | `&mut data[header_len..]` |
| 694 | 1 | slice-index | CORE | `parse` | `let range_left = NetworkEndian::read_u32(&data[left..mid]);` |
| 695 | 1 | slice-index | CORE | `parse` | `let range_right = NetworkEndian::read_u32(&data[mid..right]);` |
| 712 | 1 | slice-index | CORE | `parse` | `Ok((&buffer[length..], option))` |
| 740 | 1 | bounds-check | PANIC | `emit` | `buffer[0] = field::OPT_NOP;` |
| 744 | 1 | bounds-check | PANIC | `emit` | `buffer[1] = length as u8;` |
| 753 | 1 | bounds-check | PANIC | `emit` | `buffer[2] = value;` |
| 767 | 1 | slice-index | PANIC | `emit` | `NetworkEndian::write_u32(&mut buffer[pos..], first);` |
| 781 | 1 | copy_from_slice | PANIC | `emit` | `buffer[2..].copy_from_slice(provided)` |
| 786 | 1 | slice-index | PANIC | `emit` | `&mut buffer[length..]` |
| 1053 | 1 | slice-index | CORE | `emit` | `packet.payload_mut()[..self.payload.len()].copy_from_slice(self.payload);` |

<a id="srcwireethernetrs"></a>
### `src/wire/ethernet.rs`

7 sites across 3 lines. churn 7, panic 0, core 0. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 76 | 1 | copy_from_slice | CHURN | `from_bytes` | `bytes.copy_from_slice(data);` |
| 287 | 3 | slice-index | CHURN | `set_src_addr` | `data[field::SOURCE].copy_from_slice(value.as_bytes())` |
| 294 | 3 | slice-index | CHURN | `set_ethertype` | `NetworkEndian::write_u16(&mut data[field::ETHERTYPE], value.into())` |

<a id="srcwireipv6optionrs"></a>
### `src/wire/ipv6option.rs`

7 sites across 4 lines. churn 6, panic 0, core 1. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 229 | 1 | bounds-check | CHURN | `set_option_type` | `data[field::TYPE] = value.into();` |
| 239 | 2 | bounds-check | CHURN | `set_data_len` | `data[field::LENGTH] = value;` |
| 252 | 3 | slice-index | CHURN | `data_mut` | `&mut data[field::DATA(len)]` |
| 366 | 1 | slice-index | CORE | `emit` | `opt.data_mut().copy_from_slice(&data[..length as usize]);` |

<a id="srcwiremldrs"></a>
### `src/wire/mld.rs`

18 sites across 11 lines. churn 6, panic 3, core 1. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| ? | 8 | bounds-check, copy_from_slice, slice-index | UNATTRIBUTED | `` | `` |
| 52 | 1 | slice-index | CORE | `mcast_addr` | `Ipv6Address::from_octets(data[field::QUERY_MCAST_ADDR].try_into().unwrap())` |
| 59 | 1 | bounds-check | CHURN | `s_flag` | `(data[field::SQRV] & 0x08) != 0` |
| 73 | 1 | bounds-check | CHURN | `qqic` | `data[field::QQIC]` |
| 80 | 1 | slice-index | CHURN | `num_srcs` | `NetworkEndian::read_u16(&data[field::QUERY_NUM_SRCS])` |
| 134 | 1 | panic!/unreachable! | PANIC | `set_qrv` | `assert!(value < 8);` |
| 143 | 1 | bounds-check | CHURN | `set_qqic` | `data[field::QQIC] = value;` |
| 150 | 1 | slice-index | CHURN | `set_num_srcs` | `NetworkEndian::write_u16(&mut data[field::QUERY_NUM_SRCS], value);` |
| 273 | 1 | slice-index | CHURN | `set_num_srcs` | `NetworkEndian::write_u16(&mut data[field::RECORD_NUM_SRCS], num_srcs);` |
| 282 | 1 | panic!/unreachable! | PANIC | `set_mcast_addr` | `assert!(addr.is_multicast());` |
| 284 | 1 | slice-index | PANIC | `set_mcast_addr` | `data[field::RECORD_MCAST_ADDR].copy_from_slice(&addr.octets());` |

<a id="srcstorageringbufferrs"></a>
### `src/storage/ring_buffer.rs`

20 sites across 9 lines. churn 4, panic 2, core 3. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| ? | 1 | slice-index | UNATTRIBUTED | `` | `` |
| 110 | 4 | rem-by-zero | CHURN | `get_idx_unchecked` | `(self.read_at + idx) % self.capacity()` |
| 154 | 3 | bounds-check | FLUXBUG | `dequeue_one_with` | `let res = f(&mut self.storage[self.read_at]);` |
| 193 | 2 | slice-index | FLUXBUG | `enqueue_many_with` | `let (size, result) = f(&mut self.storage[write_at..write_at + max_size]);` |
| 245 | 5 | slice-index | FLUXBUG | `dequeue_many_with` | `let (size, result) = f(&mut self.storage[self.read_at..self.read_at + max_size]);` |
| 314 | 1 | slice-index | CORE | `get_unallocated` | `&mut self.storage[start_at..start_at + size]` |
| 345 | 1 | panic!/unreachable! | PANIC | `enqueue_unallocated` | `assert!(count <= self.window());` |
| 369 | 2 | slice-index | CORE | `get_allocated` | `&self.storage[start_at..start_at + size]` |
| 398 | 1 | panic!/unreachable! | PANIC | `dequeue_allocated` | `assert!(count <= self.len());` |

<a id="srcwireicmpv4rs"></a>
### `src/wire/icmpv4.rs`

8 sites across 7 lines. churn 4, panic 0, core 2. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| ? | 2 | slice-index | UNATTRIBUTED | `` | `` |
| 308 | 1 | bounds-check | CHURN | `set_msg_code` | `data[field::CODE] = value` |
| 325 | 1 | slice-index | CHURN | `set_echo_ident` | `NetworkEndian::write_u16(&mut data[field::ECHO_IDENT], value)` |
| 335 | 1 | slice-index | CHURN | `set_echo_seq_no` | `NetworkEndian::write_u16(&mut data[field::ECHO_SEQNO], value)` |
| 355 | 1 | slice-index | CHURN | `data_mut` | `&mut data[range]` |
| 530 | 1 | copy_from_slice | CORE | `emit` | `payload.copy_from_slice(data)` |
| 544 | 1 | copy_from_slice | CORE | `emit` | `payload.copy_from_slice(data)` |

<a id="srcifaceinterfacesixlowpanrs"></a>
### `src/iface/interface/sixlowpan.rs`

16 sites across 14 lines. churn 3, panic 7, core 4. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| ? | 2 | slice-index | UNATTRIBUTED | `` | `` |
| 81 | 1 | slice-index | CORE | `process_sixlowpan` | `Ok(len) => &f.decompress_buf[..len],` |
| 303 | 1 | panic!/unreachable! | PANIC | `dispatch_sixlowpan` | `Packet::Ipv4(_) => unreachable!(),` |
| 413 | 1 | slice-index | PANIC | `dispatch_sixlowpan` | `let mut ieee_packet = Ieee802154Frame::new_unchecked(&mut tx_buf[..ieee_len]);` |
| 458 | 1 | slice-index | PANIC | `ipv6_to_sixlowpan` | `&mut buffer[..iphc_repr.buffer_len()],` |
| 460 | 1 | slice-index | PANIC | `ipv6_to_sixlowpan` | `buffer = &mut buffer[iphc_repr.buffer_len()..];` |
| 527 | 1 | slice-index | PANIC | `ipv6_to_sixlowpan` | `&mut buffer[..udp_repr.header_len() + payload.len()],` |
| 532 | 1 | copy_from_slice | PANIC | `ipv6_to_sixlowpan` | `\|buf\| buf.copy_from_slice(payload),` |
| 549 | 1 | panic!/unreachable! | PANIC | `ipv6_to_sixlowpan` | `_ => unreachable!(),` |
| 720 | 1 | slice-index | CHURN | `decompress_ext_hdr` | `&data[ext_repr.length as usize + ext_repr.buffer_len()..],` |
| 732 | 1 | slice-index | CHURN | `decompress_ext_hdr` | `&mut buffer[..ipv6_ext_hdr.header_len()],` |
| 734 | 1 | slice-index | CHURN | `decompress_ext_hdr` | `buffer[ipv6_ext_hdr.header_len()..][..ipv6_ext_hdr.data.len()]` |
| 771 | 1 | slice-index | CORE | `decompress_udp` | `let mut udp = UdpPacket::new_unchecked(&mut buffer[..payload.len() + 8]);` |
| 773 | 2 | slice-index | CORE | `decompress_udp` | `buffer[8..][..payload.len()].copy_from_slice(payload);` |

<a id="srcwireieee802154rs"></a>
### `src/wire/ieee802154.rs`

18 sites across 7 lines. churn 3, panic 0, core 5. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| ? | 10 | bounds-check, slice-index | UNATTRIBUTED | `` | `` |
| 371 | 2 | slice-index | CORE | `frame_type` | `let raw = LittleEndian::read_u16(&data[field::FRAMECONTROL]);` |
| 388 | 1 | slice-index | CORE | `dst_addressing_mode` | `let raw = LittleEndian::read_u16(&data[field::FRAMECONTROL]);` |
| 406 | 1 | slice-index | CORE | `src_addressing_mode` | `let raw = LittleEndian::read_u16(&data[field::FRAMECONTROL]);` |
| 450 | 2 | slice-index | CHURN | `addressing_fields` | `Some(&data[field::ADDRESSING][..offset])` |
| 543 | 1 | slice-index | CORE | `src_pan_id` | `&addressing_fields[offset..][..2],` |
| 721 | 1 | slice-index | CHURN | `payload` | `Some(&data[index..])` |

<a id="srcwireipv6extheaderrs"></a>
### `src/wire/ipv6ext_header.rs`

2 sites across 2 lines. churn 2, panic 0, core 0. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 102 | 1 | bounds-check | CHURN | `set_next_header` | `data[field::NXT_HDR] = value.into();` |
| 110 | 1 | bounds-check | CHURN | `set_header_len` | `data[field::LENGTH] = value;` |

<a id="srcwiredhcpv4rs"></a>
### `src/wire/dhcpv4.rs`

4 sites across 4 lines. churn 1, panic 0, core 3. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 428 | 1 | slice-index | CORE | `set_sname_and_boot_file_to_zero` | `for byte in &mut data[field::SNAME] {` |
| 431 | 1 | slice-index | CORE | `set_sname_and_boot_file_to_zero` | `for byte in &mut data[field::FILE] {` |
| 495 | 1 | slice-index | CHURN | `set_magic_number` | `let field = &mut self.buffer.as_mut()[field::MAGIC_NUMBER];` |
| 935 | 1 | slice-index | CORE | `emit` | `servers[(i * IP_SIZE)..((i + 1) * IP_SIZE)].copy_from_slice(&ip.octets());` |

<a id="srcifaceinterfaceipv6rs"></a>
### `src/iface/interface/ipv6.rs`

3 sites across 3 lines. churn 0, panic 2, core 1. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 31 | 1 | panic!/unreachable! | PANIC | `get_source_address_ipv6` | `assert!(!dst_addr.is_unspecified());` |
| 98 | 1 | unwrap | PANIC | `get_source_address_ipv6` | `.unwrap(); // NOTE: we check above that there is at least one IPv6 address.` |
| 317 | 1 | slice-index | CORE | `process_hopbyhop` | `&ip_payload[ext_repr.header_len() + ext_repr.data.len()..],` |

<a id="srcifaceinterfacemodrs"></a>
### `src/iface/interface/mod.rs`

7 sites across 7 lines. churn 0, panic 0, core 0. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 212 | 1 | Medium> | ICE | `new` | `assert_eq!(` |
| 814 | 1 | expect | ICE | `socket_egress` | `neighbor_addr.expect("non-IP response packet"),` |
| 920 | 1 | panic!(fmt) | ICE | `check_ip_addrs` | `panic!("IP address {} is not unicast", cidr.address())` |
| 1122 | 1 | panic!/unreachable! | ICE | `lookup_hardware_addr` | `Medium::Ieee802154 => unreachable!(),` |
| 1245 | 1 | panic!/unreachable! | ICE | `dispatch_ip` | `assert!(!ip_repr.dst_addr().is_unspecified());` |
| 1281 | 1 | panic!/unreachable! | ICE | `dispatch_ip` | `(_, _) => unreachable!(),` |
| 1308 | 1 | slice-index | ICE | `dispatch_ip` | `let payload = &mut tx_buffer[repr.header_len()..];` |

<a id="srcifaceneighborrs"></a>
### `src/iface/neighbor.rs`

4 sites across 3 lines. churn 0, panic 4, core 0. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 131 | 1 | unwrap | PANIC | `fill_with_expiration` | `let _old_neighbor = self.storage.remove(&old_protocol_addr).unwrap();` |
| 143 | 1 | panic!/unreachable! | PANIC | `fill_with_expiration` | `_ => unreachable!(),` |
| 150 | 2 | panic!/unreachable! | PANIC | `lookup` | `assert!(protocol_addr.is_unicast());` |

<a id="srcifacepacketrs"></a>
### `src/iface/packet.rs`

12 sites across 9 lines. churn 0, panic 12, core 0. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 90 | 1 | panic!/unreachable! | PANIC | `emit_payload` | `IpRepr::Ipv4(_) => unreachable!(),` |
| 105 | 1 | panic!/unreachable! | PANIC | `emit_payload` | `IpRepr::Ipv4(_) => unreachable!(),` |
| 115 | 1 | slice-index | PANIC | `emit_payload` | `&mut payload[..ipv6_ext_hdr.header_len()],` |
| 121 | 1 | slice-index | PANIC | `emit_payload` | `&mut payload[hbh_start..hbh_end],` |
| 143 | 1 | copy_from_slice | PANIC | `emit_payload` | `\|buf\| buf.copy_from_slice(inner_payload),` |
| 179 | 1 | unwrap | PANIC | `emit_payload` | `\|buf\| dhcp_repr.emit(&mut DhcpPacket::new_unchecked(buf)).unwrap(),` |
| 234 | 2 | panic!/unreachable! | PANIC | `as_sixlowpan_next_header` | `Self::Icmpv4(_) => unreachable!(),` |
| 236 | 2 | panic!/unreachable! | PANIC | `as_sixlowpan_next_header` | `Self::Dhcpv4(..) => unreachable!(),` |
| 240 | 2 | panic!/unreachable! | PANIC | `as_sixlowpan_next_header` | `Self::HopByHopIcmpv6(_, _) => unreachable!(),` |

<a id="srcifacerouters"></a>
### `src/iface/route.rs`

2 sites across 2 lines. churn 0, panic 2, core 0. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 173 | 1 | panic!/unreachable! | PANIC | `lookup` | `assert!(addr.is_unicast());` |
| 187 | 1 | panic!/unreachable! | PANIC | `lookup` | `.max_by_key(\|route\| route.cidr.prefix_len())` |

<a id="srcifacesocketsetrs"></a>
### `src/iface/socket_set.rs`

28 sites across 9 lines. churn 0, panic 28, core 0. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 83 | 2 | panic!(fmt) | PANIC | `add` | `ManagedSlice::Borrowed(_) => panic!("adding a socket to a full SocketSet"),` |
| 99 | 1 | bounds-check | PANIC | `get` | `match self.sockets[handle.0].inner.as_ref() {` |
| 101 | 1 | expect | PANIC | `get` | `T::downcast(&item.socket).expect("handle refers to a socket of a wrong type")` |
| 103 | 1 | panic!(fmt) | PANIC | `get` | `None => panic!("handle does not refer to a valid socket"),` |
| 113 | 7 | bounds-check | PANIC | `get_mut` | `match self.sockets[handle.0].inner.as_mut() {` |
| 115 | 7 | expect | PANIC | `get_mut` | `.expect("handle refers to a socket of a wrong type"),` |
| 116 | 7 | panic!(fmt) | PANIC | `get_mut` | `None => panic!("handle does not refer to a valid socket"),` |
| 126 | 1 | bounds-check | PANIC | `remove` | `match self.sockets[handle.0].inner.take() {` |
| 128 | 1 | panic!(fmt) | PANIC | `remove` | `None => panic!("handle does not refer to a valid socket"),` |

<a id="srcphymodrs"></a>
### `src/phy/mod.rs`

1 sites across 1 lines. churn 0, panic 1, core 0. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 67 | 1 | panic!(fmt) | PANIC | `from_driver` | `medium => panic!(` |

<a id="srcsocketdhcpv4rs"></a>
### `src/socket/dhcpv4.rs`

3 sites across 3 lines. churn 0, panic 3, core 0. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 315 | 1 | panic!/unreachable! | PANIC | `process` | `assert!(repr.src_port == self.server_port && repr.dst_port == self.client_port);` |
| 333 | 1 | panic!(fmt) | PANIC | `process` | `panic!("using DHCPv4 socket with a non-ethernet hardware address.");` |
| 570 | 1 | panic!(fmt) | PANIC | `dispatch` | `panic!("using DHCPv4 socket with a non-ethernet hardware address.");` |

<a id="srcsockettcprs"></a>
### `src/socket/tcp.rs`

8 sites across 5 lines. churn 0, panic 1, core 1. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| ? | 4 | panic!(fmt) | UNATTRIBUTED | `` | `` |
| 592 | 1 | panic!(fmt) | PANIC | `new` | `panic!("receiving buffer too large, cannot exceed 1 GiB")` |
| 1641 | 1 | panic!/unreachable! | CLEAN | `process` | `(State::Listen, _, Some(_)) => unreachable!(),` |
| 1799 | 1 | slice-index | CLEAN | `process` | `&repr.payload[overlap_start - segment_start..overlap_end - segment_start],` |
| 2323 | 1 | unwrap | CORE | `seq_to_transmit` | `let ip_header_len = match self.tuple.unwrap().local.addr {` |

<a id="srcsocketudprs"></a>
### `src/socket/udp.rs`

1 sites across 1 lines. churn 0, panic 1, core 0. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 643 | 1 | copy_from_slice | PANIC | `process` | `Ok(buf) => buf.copy_from_slice(payload),` |

<a id="srcstorageassemblerrs"></a>
### `src/storage/assembler.rs`

1 sites across 1 lines. churn 0, panic 0, core 1. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 233 | 1 | bounds-check | CORE | `add` | `self.contigs[i + 1].shrink_hole_by(offset + size);` |

<a id="srcstoragepacketbufferrs"></a>
### `src/storage/packet_buffer.rs`

5 sites across 5 lines. churn 0, panic 1, core 1. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| ? | 1 | slice-index | UNATTRIBUTED | `` | `` |
| 195 | 1 | unwrap | FLUXBUG | `dequeue_with` | `metadata.header.as_mut().unwrap(),` |
| 196 | 1 | slice-index | FLUXBUG | `dequeue_with` | `&mut payload_buf[..metadata.size],` |
| 215 | 1 | unwrap | PANIC | `dequeue` | `Ok((meta.header.take().unwrap(), payload_buf))` |
| 227 | 1 | unwrap | CORE | `peek` | `metadata.header.as_ref().unwrap(),` |

<a id="srcwireiprs"></a>
### `src/wire/ip.rs`

4 sites across 1 lines. churn 0, panic 4, core 0. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 992 | 4 | panic!/unreachable! | PANIC | `pseudo_header` | `_ => unreachable!(),` |

<a id="srcwireipv6hbhrs"></a>
### `src/wire/ipv6hbh.rs`

2 sites across 2 lines. churn 0, panic 0, core 2. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 104 | 1 | slice-index | CORE | `emit` | `&mut buffer[..opt.buffer_len()],` |
| 106 | 1 | slice-index | CORE | `emit` | `buffer = &mut buffer[opt.buffer_len()..];` |

<a id="srcwiremodrs"></a>
### `src/wire/mod.rs`

4 sites across 3 lines. churn 0, panic 3, core 1. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 441 | 2 | panic!(fmt) | PANIC | `ethernet_or_panic` | `_ => panic!("HardwareAddress is not Ethernet."),` |
| 450 | 1 | panic!(fmt) | PANIC | `ieee802154_or_panic` | `_ => panic!("HardwareAddress is not Ethernet."),` |
| 549 | 1 | slice-index | CORE | `as_bytes` | `&self.data[..self.len as usize]` |

<a id="srcwiresixlowpanmodrs"></a>
### `src/wire/sixlowpan/mod.rs`

10 sites across 6 lines. churn 0, panic 0, core 5. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| ? | 5 | bounds-check, slice-index | UNATTRIBUTED | `` | `` |
| 86 | 1 | unwrap | CORE | `resolve` | `Ok(ipv6::Address::from_octets(addr.try_into().unwrap()))` |
| 90 | 1 | copy_from_slice | CORE | `resolve` | `bytes[8..].copy_from_slice(inline);` |
| 96 | 1 | copy_from_slice | CORE | `resolve` | `bytes[14..].copy_from_slice(inline);` |
| 118 | 1 | slice-index | CORE | `resolve` | `bytes[11..].copy_from_slice(&inline[1..][..5]);` |
| 124 | 1 | slice-index | CORE | `resolve` | `bytes[13..].copy_from_slice(&inline[1..][..3]);` |

## Caveats

- **Ablation is a ceiling, not a forecast.** `get_unchecked` removes a check whether or not anything proved it safe. These binaries are measured, never flashed.
- **Per-file deltas do not sum.** The eight files' CHURN lines total -1904 B alone but -3624 B of flash together -- superadditive, because shared panic machinery only dies with its last user. Rank with the per-file column; never total it.
- **Noise floor.** An identical rebuild reproduced `.text` exactly (0 B), so there is no link noise -- but a real source change shifts inlining, and the largest INCREASE seen was +332 B. Treat a single-file delta under ~300 B as unresolved.
- **Categories come from the HARDEST Flux error on a function**, not the first. Flux's diagnostic order is not reproducible: two runs of identical code disagreed on 29 rows. A line counts as churn only if every error on its function is churn.
- **`src/wire/mod.rs` and `src/storage/assembler.rs` are excluded from the ceiling** -- the ablator cannot rewrite them (`[u8; N]` has no `__ai` impl; `assembler.rs` hits borrowck). 5 sites.
- **Two files under-ablated** against their targets: `ndiscoption` removed 4 of 7 targeted, `nhc` 5 of 7, mostly `const fn` bodies the rewriter skips. Their small deltas are understated.
