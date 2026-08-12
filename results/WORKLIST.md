# Worklist: every panic site, by phase

All 650 panic sites in the linked nRF52840 `usb_ethernet` binary, grouped into the phases in [ROADMAP.md](ROADMAP.md). Regenerate with `./worklist.py`.

One row per source **line**; `sites` is how many machine call sites that line compiles to, because generics and inlining duplicate it. Lines track effort, sites track the metric.

Spans come from each panic's `core::panic::Location` argument, read out of `.rodata` — the location the panic would print at runtime — not from DWARF, which reports no line for the branches the optimiser tail-merged and misattributes others to the core code they inlined. `(no line)` means the site carries no Location either; on this firmware that is defmt's panic macro, and never xarxa.

| phase | sites | what |
| --- | ---: | --- |
| [0](#phase-0) | 205 | xarxa CHURN |
| [1](#phase-1) | 54 | the attribution gap |
| [2](#phase-2) | 112 | xarxa PANIC |
| [3](#phase-3) | 62 | xarxa CORE |
| [4](#phase-4) | 20 | compiler work |
| [5](#phase-5) | 33 | logging and formatting |
| [6](#phase-6) | 164 | the embassy crates and other dependencies |
| | **650** | |

---

<a id="phase-0"></a>
## Phase 0 — xarxa CHURN

205 sites. State a length or range precondition and discharge it, then follow the obligation to the callers. Fully delegable; four agents are on udp, ipv4, ndiscoption and nhc as of 2026-08-11.

### `src/wire/sixlowpan/iphc.rs` — 25 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/sixlowpan/iphc.rs:133` | 1 | slice-index | `next_header` | `let nh = data[start..start + 1][0];` |
| `src/wire/sixlowpan/iphc.rs:288` | 2 | slice-index | `dst_addr` | `&data[start..][..16],` |
| `src/wire/sixlowpan/iphc.rs:291` | 2 | slice-index | `dst_addr` | `AddressMode::InLine64bits(&data[start..][..8]),` |
| `src/wire/sixlowpan/iphc.rs:294` | 2 | slice-index | `dst_addr` | `AddressMode::InLine16bits(&data[start..][..2]),` |
| `src/wire/sixlowpan/iphc.rs:302` | 2 | slice-index | `dst_addr` | `AddressMode::InLine64bits(&data[start..][..8]),` |
| `src/wire/sixlowpan/iphc.rs:312` | 2 | slice-index | `dst_addr` | `AddressMode::InLine16bits(&data[start..][..2]),` |
| `src/wire/sixlowpan/iphc.rs:329` | 2 | slice-index | `dst_addr` | `&data[start..][..16],` |
| `src/wire/sixlowpan/iphc.rs:332` | 2 | slice-index | `dst_addr` | `AddressMode::Multicast48bits(&data[start..][..6]),` |
| `src/wire/sixlowpan/iphc.rs:335` | 2 | slice-index | `dst_addr` | `AddressMode::Multicast32bits(&data[start..][..4]),` |
| `src/wire/sixlowpan/iphc.rs:338` | 2 | slice-index | `dst_addr` | `AddressMode::Multicast8bits(&data[start..][..1]),` |
| `src/wire/sixlowpan/iphc.rs:455` | 1 | slice-index | `payload` | `&data[len..]` |
| `src/wire/sixlowpan/iphc.rs:462` | 1 | slice-index | `set_dispatch_field` | `let data = &mut self.buffer.as_mut()[field::IPHC_FIELD];` |
| `src/wire/sixlowpan/iphc.rs:481` | 4 | slice-index | `set_field` | `raw[idx..idx + value.len()].copy_from_slice(value);` |

### `src/wire/ipv6.rs` — 24 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ipv6.rs:448` | 2 | slice-index | `payload_len` | `NetworkEndian::read_u16(&data[field::LENGTH])` |
| `src/wire/ipv6.rs:492` | 1 | slice-index | `payload` | `&data[range]` |
| `src/wire/ipv6.rs:503` | 3 | bounds-check | `set_version` | `data[0] = (data[0] & 0x0f) \| ((value & 0x0f) << 4);` |
| `src/wire/ipv6.rs:512` | 1 | bounds-check | `set_traffic_class` | `data[0] = (data[0] & 0xf0) \| ((value & 0xf0) >> 4);` |
| `src/wire/ipv6.rs:515` | 3 | bounds-check | `set_traffic_class` | `data[1] = (data[1] & 0x0f) \| ((value & 0x0f) << 4);` |
| `src/wire/ipv6.rs:531` | 3 | slice-index | `set_payload_len` | `NetworkEndian::write_u16(&mut data[field::LENGTH], value);` |
| `src/wire/ipv6.rs:538` | 1 | bounds-check | `set_next_header` | `data[field::NXT_HDR] = value.into();` |
| `src/wire/ipv6.rs:545` | 3 | bounds-check | `set_hop_limit` | `data[field::HOP_LIMIT] = value;` |
| `src/wire/ipv6.rs:552` | 3 | slice-index | `set_src_addr` | `data[field::SRC_ADDR].copy_from_slice(&value.octets());` |
| `src/wire/ipv6.rs:559` | 3 | slice-index | `set_dst_addr` | `data[field::DST_ADDR].copy_from_slice(&value.octets());` |
| `src/wire/ipv6.rs:567` | 1 | slice-index | `payload_mut` | `&mut data[range]` |

### `src/wire/icmpv6.rs` — 21 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/icmpv6.rs:458` | 5 | slice-index | `payload` | `&data[self.header_len()..]` |
| `src/wire/icmpv6.rs:470` | 3 | bounds-check | `set_msg_type` | `data[field::TYPE] = value.into()` |
| `src/wire/icmpv6.rs:479` | 4 | bounds-check | `set_msg_code` | `data[field::CODE] = value` |
| `src/wire/icmpv6.rs:502` | 2 | slice-index | `clear_reserved` | `NetworkEndian::write_u32(&mut data[field::UNUSED], 0);` |
| `src/wire/icmpv6.rs:506` | 1 | slice-index | `clear_reserved` | `NetworkEndian::write_u16(&mut data[field::QUERY_RESV], 0);` |
| `src/wire/icmpv6.rs:507` | 1 | bounds-check | `clear_reserved` | `data[field::SQRV] &= 0xf;` |
| `src/wire/icmpv6.rs:511` | 1 | slice-index | `clear_reserved` | `NetworkEndian::write_u16(&mut data[field::RECORD_RESV], 0);` |
| `src/wire/icmpv6.rs:544` | 1 | slice-index | `set_echo_ident` | `NetworkEndian::write_u16(&mut data[field::ECHO_IDENT], value)` |
| `src/wire/icmpv6.rs:554` | 1 | slice-index | `set_echo_seq_no` | `NetworkEndian::write_u16(&mut data[field::ECHO_SEQNO], value)` |
| `src/wire/icmpv6.rs:600` | 2 | slice-index | `payload_mut` | `&mut data[range]` |

### `src/wire/ipv4.rs` — 20 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ipv4.rs:369` | 1 | slice-index | `verify_checksum` | `checksum::data(&data[..self.header_len() as usize]) == !0` |
| `src/wire/ipv4.rs:389` | 1 | slice-index | `payload` | `&data[range]` |
| `src/wire/ipv4.rs:398` | 2 | bounds-check | `set_version` | `data[field::VER_IHL] = (data[field::VER_IHL] & !0xf0) \| (value << 4);` |
| `src/wire/ipv4.rs:411` | 2 | bounds-check | `set_dscp` | `data[field::DSCP_ECN] = (data[field::DSCP_ECN] & !0xfc) \| (value << 2)` |
| `src/wire/ipv4.rs:424` | 2 | slice-index | `set_total_len` | `NetworkEndian::write_u16(&mut data[field::LENGTH], value)` |
| `src/wire/ipv4.rs:431` | 2 | slice-index | `set_ident` | `NetworkEndian::write_u16(&mut data[field::IDENT], value)` |
| `src/wire/ipv4.rs:438` | 2 | slice-index | `clear_flags` | `let raw = NetworkEndian::read_u16(&data[field::FLG_OFF]);` |
| `src/wire/ipv4.rs:474` | 2 | bounds-check | `set_hop_limit` | `data[field::TTL] = value` |
| `src/wire/ipv4.rs:481` | 2 | bounds-check | `set_next_header` | `data[field::PROTOCOL] = value.into()` |
| `src/wire/ipv4.rs:495` | 2 | slice-index | `set_src_addr` | `data[field::SRC_ADDR].copy_from_slice(&value.octets())` |
| `src/wire/ipv4.rs:502` | 2 | slice-index | `set_dst_addr` | `data[field::DST_ADDR].copy_from_slice(&value.octets())` |

### `src/wire/sixlowpan/nhc.rs` — 19 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/sixlowpan/nhc.rs:179` | 2 | bounds-check | `length` | `self.buffer.as_ref()[1 + self.next_header_size()]` |
| `src/wire/sixlowpan/nhc.rs:208` | 2 | slice-index | `payload` | `&self.buffer.as_ref()[start..][..len]` |
| `src/wire/sixlowpan/nhc.rs:586` | 1 | slice-index | `checksum` | `Some(NetworkEndian::read_u16(&data[start..start + 2]))` |
| `src/wire/sixlowpan/nhc.rs:618` | 3 | slice-index | `payload` | `&self.buffer.as_ref()[start..]` |
| `src/wire/sixlowpan/nhc.rs:626` | 2 | slice-index | `payload_mut` | `&mut self.buffer.as_mut()[start..]` |
| `src/wire/sixlowpan/nhc.rs:632` | 1 | bounds-check | `set_dispatch_field` | `data[0] = (data[0] & !(0b11111 << 3)) \| (DISPATCH_UDP_HEADER << 3);` |
| `src/wire/sixlowpan/nhc.rs:648` | 1 | bounds-check | `set_ports` | `data[idx] = (((src_port - 0xf0b0) as u8) << 4) & ((dst_port - 0xf0b0) as u8);` |
| `src/wire/sixlowpan/nhc.rs:654` | 1 | bounds-check | `set_ports` | `data[idx] = (src_port - 0xf000) as u8;` |
| `src/wire/sixlowpan/nhc.rs:657` | 1 | slice-index | `set_ports` | `NetworkEndian::write_u16(&mut data[idx..idx + 2], dst_port);` |
| `src/wire/sixlowpan/nhc.rs:663` | 1 | slice-index | `set_ports` | `NetworkEndian::write_u16(&mut data[idx..idx + 2], src_port);` |
| `src/wire/sixlowpan/nhc.rs:665` | 1 | bounds-check | `set_ports` | `data[idx] = (dst_port - 0xf000) as u8;` |
| `src/wire/sixlowpan/nhc.rs:671` | 1 | slice-index | `set_ports` | `NetworkEndian::write_u16(&mut data[idx..idx + 2], src_port);` |
| `src/wire/sixlowpan/nhc.rs:673` | 1 | slice-index | `set_ports` | `NetworkEndian::write_u16(&mut data[idx..idx + 2], dst_port);` |
| `src/wire/sixlowpan/nhc.rs:682` | 1 | slice-index | `set_checksum` | `NetworkEndian::write_u16(&mut data[idx..idx + 2], checksum);` |

### `src/wire/udp.rs` — 18 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/udp.rs:94` | 1 | slice-index | `len` | `NetworkEndian::read_u16(&data[field::LENGTH])` |
| `src/wire/udp.rs:101` | 1 | slice-index | `checksum` | `NetworkEndian::read_u16(&data[field::CHECKSUM])` |
| `src/wire/udp.rs:145` | 1 | slice-index | `verify_checksum` | `checksum::data(&data[..self.len() as usize]),` |
| `src/wire/udp.rs:156` | 1 | slice-index | `payload` | `&data[field::PAYLOAD(length)]` |
| `src/wire/udp.rs:165` | 3 | slice-index | `set_src_port` | `NetworkEndian::write_u16(&mut data[field::SRC_PORT], value)` |
| `src/wire/udp.rs:172` | 3 | slice-index | `set_dst_port` | `NetworkEndian::write_u16(&mut data[field::DST_PORT], value)` |
| `src/wire/udp.rs:179` | 3 | slice-index | `set_len` | `NetworkEndian::write_u16(&mut data[field::LENGTH], value)` |
| `src/wire/udp.rs:186` | 2 | slice-index | `set_checksum` | `NetworkEndian::write_u16(&mut data[field::CHECKSUM], value)` |
| `src/wire/udp.rs:200` | 1 | slice-index | `fill_checksum` | `checksum::data(&data[..self.len() as usize]),` |
| `src/wire/udp.rs:215` | 2 | slice-index | `payload_mut` | `&mut data[field::PAYLOAD(length)]` |

### `src/wire/ndisc.rs` — 14 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ndisc.rs:59` | 1 | slice-index | `reachable_time` | `Duration::from_millis(NetworkEndian::read_u32(&data[field::REACHABLE_TM]) as u64)` |
| `src/wire/ndisc.rs:66` | 1 | slice-index | `retrans_time` | `Duration::from_millis(NetworkEndian::read_u32(&data[field::RETRANS_TM]) as u64)` |
| `src/wire/ndisc.rs:120` | 1 | bounds-check | `set_current_hop_limit` | `data[field::CUR_HOP_LIMIT] = value;` |
| `src/wire/ndisc.rs:126` | 1 | bounds-check | `set_router_flags` | `self.buffer.as_mut()[field::ROUTER_FLAGS] = flags.bits();` |
| `src/wire/ndisc.rs:133` | 1 | slice-index | `set_router_lifetime` | `NetworkEndian::write_u16(&mut data[field::ROUTER_LT], value.secs() as u16);` |
| `src/wire/ndisc.rs:140` | 1 | slice-index | `set_reachable_time` | `NetworkEndian::write_u32(&mut data[field::REACHABLE_TM], value.total_millis() as u32);` |
| `src/wire/ndisc.rs:147` | 1 | slice-index | `set_retrans_time` | `NetworkEndian::write_u32(&mut data[field::RETRANS_TM], value.total_millis() as u32);` |
| `src/wire/ndisc.rs:162` | 2 | slice-index | `set_target_addr` | `data[field::TARGET_ADDR].copy_from_slice(&value.octets());` |
| `src/wire/ndisc.rs:187` | 1 | slice-index | `set_dest_addr` | `data[field::DEST_ADDR].copy_from_slice(&value.octets());` |
| `src/wire/ndisc.rs:240` | 1 | slice-index | `parse` | `let pkt = NdiscOption::new_checked(&packet.payload()[offset..])?;` |
| `src/wire/ndisc.rs:389` | 1 | slice-index | `emit` | `NdiscOption::new_unchecked(&mut packet.payload_mut()[offset..]);` |
| `src/wire/ndisc.rs:395` | 1 | slice-index | `emit` | `NdiscOption::new_unchecked(&mut packet.payload_mut()[offset..]);` |
| `src/wire/ndisc.rs:451` | 1 | slice-index | `emit` | `NdiscOption::new_unchecked(&mut packet.payload_mut()[offset..]);` |

### `src/wire/arp.rs` — 9 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/arp.rs:176` | 1 | slice-index | `set_hardware_type` | `NetworkEndian::write_u16(&mut data[field::HTYPE], value.into())` |
| `src/wire/arp.rs:183` | 1 | slice-index | `set_protocol_type` | `NetworkEndian::write_u16(&mut data[field::PTYPE], value.into())` |
| `src/wire/arp.rs:190` | 1 | bounds-check | `set_hardware_len` | `data[field::HLEN] = value` |
| `src/wire/arp.rs:197` | 1 | bounds-check | `set_protocol_len` | `data[field::PLEN] = value` |
| `src/wire/arp.rs:204` | 1 | slice-index | `set_operation` | `NetworkEndian::write_u16(&mut data[field::OPER], value.into())` |
| `src/wire/arp.rs:214` | 1 | slice-index | `set_source_hardware_addr` | `data[field::SHA(hardware_len, protocol_len)].copy_from_slice(value)` |
| `src/wire/arp.rs:224` | 1 | slice-index | `set_source_protocol_addr` | `data[field::SPA(hardware_len, protocol_len)].copy_from_slice(value)` |
| `src/wire/arp.rs:234` | 1 | slice-index | `set_target_hardware_addr` | `data[field::THA(hardware_len, protocol_len)].copy_from_slice(value)` |
| `src/wire/arp.rs:244` | 1 | slice-index | `set_target_protocol_addr` | `data[field::TPA(hardware_len, protocol_len)].copy_from_slice(value)` |

### `src/wire/ndiscoption.rs` — 9 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ndiscoption.rs:289` | 1 | bounds-check | `set_option_type` | `data[field::TYPE] = value.into();` |
| `src/wire/ndiscoption.rs:296` | 2 | bounds-check | `set_data_len` | `data[field::LENGTH] = value;` |
| `src/wire/ndiscoption.rs:306` | 1 | slice-index | `set_link_layer_addr` | `data[2..2 + addr.len()].copy_from_slice(addr.as_bytes())` |
| `src/wire/ndiscoption.rs:316` | 1 | slice-index | `set_mtu` | `NetworkEndian::write_u32(&mut data[field::MTU], value);` |
| `src/wire/ndiscoption.rs:352` | 1 | slice-index | `clear_prefix_reserved` | `NetworkEndian::write_u32(&mut data[field::PREF_RESERVED], 0);` |
| `src/wire/ndiscoption.rs:359` | 1 | slice-index | `set_prefix` | `data[field::PREFIX].copy_from_slice(&addr.octets());` |
| `src/wire/ndiscoption.rs:379` | 2 | slice-index | `data_mut` | `&mut data[field::DATA(len)]` |

### `src/wire/tcp.rs` — 8 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/tcp.rs:392` | 1 | slice-index | `options` | `&data[field::OPTIONS(header_len)]` |
| `src/wire/tcp.rs:400` | 1 | slice-index | `payload` | `&data[header_len..]` |
| `src/wire/tcp.rs:409` | 1 | slice-index | `set_src_port` | `NetworkEndian::write_u16(&mut data[field::SRC_PORT], value)` |
| `src/wire/tcp.rs:416` | 1 | slice-index | `set_dst_port` | `NetworkEndian::write_u16(&mut data[field::DST_PORT], value)` |
| `src/wire/tcp.rs:572` | 1 | slice-index | `set_window_len` | `NetworkEndian::write_u16(&mut data[field::WIN_SIZE], value)` |
| `src/wire/tcp.rs:586` | 1 | slice-index | `set_urgent_at` | `NetworkEndian::write_u16(&mut data[field::URGENT], value)` |
| `src/wire/tcp.rs:611` | 1 | slice-index | `options_mut` | `&mut data[field::OPTIONS(header_len)]` |
| `src/wire/tcp.rs:619` | 1 | slice-index | `payload_mut` | `&mut data[header_len..]` |

### `src/wire/ethernet.rs` — 7 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ethernet.rs:76` | 1 | copy_from_slice | `from_bytes` | `bytes.copy_from_slice(data);` |
| `src/wire/ethernet.rs:287` | 3 | slice-index | `set_src_addr` | `data[field::SOURCE].copy_from_slice(value.as_bytes())` |
| `src/wire/ethernet.rs:294` | 3 | slice-index | `set_ethertype` | `NetworkEndian::write_u16(&mut data[field::ETHERTYPE], value.into())` |

### `src/wire/ipv6option.rs` — 6 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ipv6option.rs:229` | 1 | bounds-check | `set_option_type` | `data[field::TYPE] = value.into();` |
| `src/wire/ipv6option.rs:239` | 2 | bounds-check | `set_data_len` | `data[field::LENGTH] = value;` |
| `src/wire/ipv6option.rs:252` | 3 | slice-index | `data_mut` | `&mut data[field::DATA(len)]` |

### `src/wire/mld.rs` — 6 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/mld.rs:59` | 1 | bounds-check | `s_flag` | `(data[field::SQRV] & 0x08) != 0` |
| `src/wire/mld.rs:73` | 1 | bounds-check | `qqic` | `data[field::QQIC]` |
| `src/wire/mld.rs:80` | 1 | slice-index | `num_srcs` | `NetworkEndian::read_u16(&data[field::QUERY_NUM_SRCS])` |
| `src/wire/mld.rs:143` | 1 | bounds-check | `set_qqic` | `data[field::QQIC] = value;` |
| `src/wire/mld.rs:150` | 1 | slice-index | `set_num_srcs` | `NetworkEndian::write_u16(&mut data[field::QUERY_NUM_SRCS], value);` |
| `src/wire/mld.rs:273` | 1 | slice-index | `set_num_srcs` | `NetworkEndian::write_u16(&mut data[field::RECORD_NUM_SRCS], num_srcs);` |

### `src/storage/ring_buffer.rs` — 4 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/storage/ring_buffer.rs:110` | 4 | rem-by-zero | `get_idx_unchecked` | `(self.read_at + idx) % self.capacity()` |

### `src/wire/icmpv4.rs` — 4 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/icmpv4.rs:308` | 1 | bounds-check | `set_msg_code` | `data[field::CODE] = value` |
| `src/wire/icmpv4.rs:325` | 1 | slice-index | `set_echo_ident` | `NetworkEndian::write_u16(&mut data[field::ECHO_IDENT], value)` |
| `src/wire/icmpv4.rs:335` | 1 | slice-index | `set_echo_seq_no` | `NetworkEndian::write_u16(&mut data[field::ECHO_SEQNO], value)` |
| `src/wire/icmpv4.rs:355` | 1 | slice-index | `data_mut` | `&mut data[range]` |

### `src/iface/interface/sixlowpan.rs` — 3 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/iface/interface/sixlowpan.rs:720` | 1 | slice-index | `decompress_ext_hdr` | `&data[ext_repr.length as usize + ext_repr.buffer_len()..],` |
| `src/iface/interface/sixlowpan.rs:732` | 1 | slice-index | `decompress_ext_hdr` | `&mut buffer[..ipv6_ext_hdr.header_len()],` |
| `src/iface/interface/sixlowpan.rs:734` | 1 | slice-index | `decompress_ext_hdr` | `buffer[ipv6_ext_hdr.header_len()..][..ipv6_ext_hdr.data.len()]` |

### `src/wire/ieee802154.rs` — 3 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ieee802154.rs:450` | 2 | slice-index | `addressing_fields` | `Some(&data[field::ADDRESSING][..offset])` |
| `src/wire/ieee802154.rs:721` | 1 | slice-index | `payload` | `Some(&data[index..])` |

### `src/socket/tcp.rs` — 2 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/socket/tcp.rs:1641` | 1 | panic!/unreachable! | `process` | `(State::Listen, _, Some(_)) => unreachable!(),` |
| `src/socket/tcp.rs:1799` | 1 | slice-index | `process` | `&repr.payload[overlap_start - segment_start..overlap_end - segment_start],` |

### `src/wire/ipv6ext_header.rs` — 2 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ipv6ext_header.rs:102` | 1 | bounds-check | `set_next_header` | `data[field::NXT_HDR] = value.into();` |
| `src/wire/ipv6ext_header.rs:110` | 1 | bounds-check | `set_header_len` | `data[field::LENGTH] = value;` |

### `src/wire/dhcpv4.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/dhcpv4.rs:495` | 1 | slice-index | `set_magic_number` | `let field = &mut self.buffer.as_mut()[field::MAGIC_NUMBER];` |

---

<a id="phase-1"></a>
## Phase 1 — the attribution gap

54 sites. Sites with no Flux obligation attached. Every one now has an exact span -- blame.py reads it from the panic's own core::panic::Location -- so what is left is not a missing line but a missing obligation: the site sits outside any fn the triage parser recognises (a macro_rules body, a const, a derive), or its function was never in a triage run. Re-running triage.py against the current blame data is what shrinks this.

**Also in this phase, and not in the table below:** 53 xarxa sites survive even a full unsound `get_unchecked` ablation, so they cannot be removed by any means currently known. 20 are in `src/wire/sixlowpan/iphc.rs`, 4 each in `wire/mod.rs`, `ipv6.rs` and `ieee802154.rs`. Named causes so far: `const fn` bodies (the ablator skips them, `get_unchecked` is not const-stable), `[u8; N]` arrays (the ablator's index trait covers `[T]` only), and borrowck conflicts in `assembler.rs`. Rows below marked `const-fn` are inside a const body and are the prime suspects.

### `src/wire/ieee802154.rs` — 25 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ieee802154.rs:501` | 1 | slice-index | `` | `Some(Pan(LittleEndian::read_u16(&addressing_fields[..2])))` |
| `src/wire/ieee802154.rs:518` | 1 | slice-index | `` | `raw.clone_from_slice(&addressing_fields[offset..offset + 2]);` |
| `src/wire/ieee802154.rs:524` | 1 | slice-index | `` | `raw.clone_from_slice(&addressing_fields[offset..offset + 8]);` |
| `src/wire/ieee802154.rs:563` | 1 | slice-index | `` | `raw.clone_from_slice(&addressing_fields[offset..offset + 2]);` |
| `src/wire/ieee802154.rs:569` | 1 | slice-index | `` | `raw.clone_from_slice(&addressing_fields[offset..offset + 8]);` |
| `src/wire/ieee802154.rs:640` | 2 | bounds-check, slice-index | `` | `let b = self.buffer.as_ref()[index..][0];` |
| `src/wire/ieee802154.rs:647` | 2 | bounds-check, slice-index | `` | `let b = self.buffer.as_ref()[index..][0];` |
| `src/wire/ieee802154.rs:732` | 1 | slice-index | `` | `let data = &mut self.buffer.as_mut()[field::FRAMECONTROL];` |
| `src/wire/ieee802154.rs:758` | 1 | bounds-check | `` | `data[field::SEQUENCE_NUMBER] = value;` |
| `src/wire/ieee802154.rs:769` | 2 | slice-index | `` | `data[field::ADDRESSING][..2].copy_from_slice(&value.as_bytes());` |
| `src/wire/ieee802154.rs:781` | 2 | slice-index | `` | `data[field::ADDRESSING][2..2 + 2].copy_from_slice(&value);` |
| `src/wire/ieee802154.rs:787` | 1 | slice-index | `` | `let data = &mut self.buffer.as_mut()[field::ADDRESSING];` |
| `src/wire/ieee802154.rs:788` | 1 | slice-index | `` | `data[2..2 + 8].copy_from_slice(&value);` |
| `src/wire/ieee802154.rs:811` | 1 | panic!/unreachable! | `` | `_ => unreachable!(),` |
| `src/wire/ieee802154.rs:814` | 1 | slice-index | `` | `let data = &mut self.buffer.as_mut()[field::ADDRESSING];` |
| `src/wire/ieee802154.rs:815` | 1 | slice-index | `` | `data[offset..offset + 2].copy_from_slice(&value.as_bytes());` |
| `src/wire/ieee802154.rs:825` | 1 | panic!/unreachable! | `` | `_ => unreachable!(),` |
| `src/wire/ieee802154.rs:835` | 1 | slice-index | `` | `let data = &mut self.buffer.as_mut()[field::ADDRESSING];` |
| `src/wire/ieee802154.rs:836` | 1 | slice-index | `` | `data[offset..offset + 2].copy_from_slice(&value);` |
| `src/wire/ieee802154.rs:842` | 1 | slice-index | `` | `let data = &mut self.buffer.as_mut()[field::ADDRESSING];` |
| `src/wire/ieee802154.rs:843` | 1 | slice-index | `` | `data[offset..offset + 8].copy_from_slice(&value);` |

### `src/wire/sixlowpan/iphc.rs` — 18 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/sixlowpan/iphc.rs:160` | 1 | bounds-check | `` | `Some(data[2] >> 4)` |
| `src/wire/sixlowpan/iphc.rs:170` | 1 | bounds-check | `` | `Some(data[2] & 0x0f)` |
| `src/wire/sixlowpan/iphc.rs:181` | 2 | bounds-check, slice-index | `` | `Some(self.buffer.as_ref()[start..][0] & 0b1100_0000)` |
| `src/wire/sixlowpan/iphc.rs:193` | 2 | bounds-check, slice-index | `` | `Some(self.buffer.as_ref()[start..][0] & 0b111111)` |
| `src/wire/sixlowpan/iphc.rs:230` | 2 | slice-index | `` | `&data[start..][..16],` |
| `src/wire/sixlowpan/iphc.rs:233` | 2 | slice-index | `` | `AddressMode::InLine64bits(&data[start..][..8]),` |
| `src/wire/sixlowpan/iphc.rs:236` | 2 | slice-index | `` | `AddressMode::InLine16bits(&data[start..][..2]),` |
| `src/wire/sixlowpan/iphc.rs:247` | 2 | slice-index | `` | `AddressMode::InLine64bits(&data[start..][..8]),` |
| `src/wire/sixlowpan/iphc.rs:257` | 2 | slice-index | `` | `AddressMode::InLine16bits(&data[start..][..2]),` |
| `src/wire/sixlowpan/iphc.rs:349` | 1 | slice-index | `` | `get_field!(dispatch_field, 0b111, 13);` |
| `src/wire/sixlowpan/iphc.rs:353` | 1 | slice-index | `` | `get_field!(cid_field, 0b1, 7);` |

### `src/wire/mld.rs` — 5 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/mld.rs:163` | 1 | slice-index | `` | `NetworkEndian::write_u16(&mut data[field::NR_MCAST_RCRDS], value)` |
| `src/wire/mld.rs:259` | 1 | bounds-check | `` | `data[field::RECORD_TYPE] = rty.into();` |
| `src/wire/mld.rs:266` | 1 | bounds-check | `` | `data[field::AUX_DATA_LEN] = len;` |
| `src/wire/mld.rs:432` | 1 | copy_from_slice | `` | `packet.payload_mut().copy_from_slice(&data[..]);` |
| `src/wire/mld.rs:442` | 1 | copy_from_slice | `` | `packet.payload_mut().copy_from_slice(&data[..]);` |

### `src/wire/icmpv6.rs` — 3 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/icmpv6.rs:534` | 1 | slice-index | `` | `NetworkEndian::write_u16(&mut data[field::CHECKSUM], value)` |
| `src/wire/icmpv6.rs:564` | 1 | slice-index | `` | `NetworkEndian::write_u32(&mut data[field::MTU], value)` |
| `src/wire/icmpv6.rs:574` | 1 | slice-index | `` | `NetworkEndian::write_u32(&mut data[field::POINTER], value)` |

### `src/wire/sixlowpan/nhc.rs` — 3 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/sixlowpan/nhc.rs:160` | 1 | bounds-check | `` | `get_field!(eid_field, 0b111, 1);` |
| `src/wire/sixlowpan/nhc.rs:161` | 1 | bounds-check | `` | `get_field!(nh_field, 0b1, 0);` |
| `src/wire/sixlowpan/nhc.rs:510` | 1 | bounds-check | `` | `get_field!(ports_field, 0b11, 0);` |

---

<a id="phase-2"></a>
## Phase 2 — xarxa PANIC

112 sites. An explicit panic!/unreachable!/assert!/expect. Needs a REACHABILITY argument, and the fact that kills the branch usually lives in another module. Blocked on picking a type invariant, not on effort.

### `src/iface/socket_set.rs` — 28 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/iface/socket_set.rs:83` | 2 | panic!(fmt) | `add` | `ManagedSlice::Borrowed(_) => panic!("adding a socket to a full SocketSet"),` |
| `src/iface/socket_set.rs:99` | 1 | bounds-check | `get` | `match self.sockets[handle.0].inner.as_ref() {` |
| `src/iface/socket_set.rs:101` | 1 | expect | `get` | `T::downcast(&item.socket).expect("handle refers to a socket of a wrong type")` |
| `src/iface/socket_set.rs:103` | 1 | panic!(fmt) | `get` | `None => panic!("handle does not refer to a valid socket"),` |
| `src/iface/socket_set.rs:113` | 7 | bounds-check | `get_mut` | `match self.sockets[handle.0].inner.as_mut() {` |
| `src/iface/socket_set.rs:115` | 7 | expect | `get_mut` | `.expect("handle refers to a socket of a wrong type"),` |
| `src/iface/socket_set.rs:116` | 7 | panic!(fmt) | `get_mut` | `None => panic!("handle does not refer to a valid socket"),` |
| `src/iface/socket_set.rs:126` | 1 | bounds-check | `remove` | `match self.sockets[handle.0].inner.take() {` |
| `src/iface/socket_set.rs:128` | 1 | panic!(fmt) | `remove` | `None => panic!("handle does not refer to a valid socket"),` |

### `src/wire/tcp.rs` — 24 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/tcp.rs:44` | 10 | panic!(fmt) | `add` | `panic!("attempt to add to sequence number with unsigned overflow")` |
| `src/wire/tcp.rs:55` | 1 | panic!(fmt) | `sub` | `panic!("attempt to subtract to sequence number with unsigned overflow")` |
| `src/wire/tcp.rs:73` | 7 | panic!(fmt) | `sub` | `panic!("attempt to subtract sequence numbers with underflow")` |
| `src/wire/tcp.rs:740` | 1 | bounds-check | `emit` | `buffer[0] = field::OPT_NOP;` |
| `src/wire/tcp.rs:744` | 1 | bounds-check | `emit` | `buffer[1] = length as u8;` |
| `src/wire/tcp.rs:753` | 1 | bounds-check | `emit` | `buffer[2] = value;` |
| `src/wire/tcp.rs:767` | 1 | slice-index | `emit` | `NetworkEndian::write_u32(&mut buffer[pos..], first);` |
| `src/wire/tcp.rs:781` | 1 | copy_from_slice | `emit` | `buffer[2..].copy_from_slice(provided)` |
| `src/wire/tcp.rs:786` | 1 | slice-index | `emit` | `&mut buffer[length..]` |

### `src/iface/packet.rs` — 11 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/iface/packet.rs:90` | 1 | panic!/unreachable! | `emit_payload` | `IpRepr::Ipv4(_) => unreachable!(),` |
| `src/iface/packet.rs:105` | 1 | panic!/unreachable! | `emit_payload` | `IpRepr::Ipv4(_) => unreachable!(),` |
| `src/iface/packet.rs:115` | 1 | slice-index | `emit_payload` | `&mut payload[..ipv6_ext_hdr.header_len()],` |
| `src/iface/packet.rs:121` | 1 | slice-index | `emit_payload` | `&mut payload[hbh_start..hbh_end],` |
| `src/iface/packet.rs:143` | 1 | copy_from_slice | `emit_payload` | `\|buf\| buf.copy_from_slice(inner_payload),` |
| `src/iface/packet.rs:234` | 2 | panic!/unreachable! | `as_sixlowpan_next_header` | `Self::Icmpv4(_) => unreachable!(),` |
| `src/iface/packet.rs:236` | 2 | panic!/unreachable! | `as_sixlowpan_next_header` | `Self::Dhcpv4(..) => unreachable!(),` |
| `src/iface/packet.rs:240` | 2 | panic!/unreachable! | `as_sixlowpan_next_header` | `Self::HopByHopIcmpv6(_, _) => unreachable!(),` |

### `src/iface/interface/sixlowpan.rs` — 9 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/iface/interface/sixlowpan.rs:303` | 1 | panic!/unreachable! | `dispatch_sixlowpan` | `Packet::Ipv4(_) => unreachable!(),` |
| `src/iface/interface/sixlowpan.rs:413` | 1 | slice-index | `dispatch_sixlowpan` | `let mut ieee_packet = Ieee802154Frame::new_unchecked(&mut tx_buf[..ieee_len]);` |
| `src/iface/interface/sixlowpan.rs:458` | 1 | slice-index | `ipv6_to_sixlowpan` | `&mut buffer[..iphc_repr.buffer_len()],` |
| `src/iface/interface/sixlowpan.rs:460` | 1 | slice-index | `ipv6_to_sixlowpan` | `buffer = &mut buffer[iphc_repr.buffer_len()..];` |
| `src/iface/interface/sixlowpan.rs:518` | 1 | slice-index | `ipv6_to_sixlowpan` | `&mut Icmpv6Packet::new_unchecked(&mut buffer[..icmp_repr.buffer_len()]),` |
| `src/iface/interface/sixlowpan.rs:527` | 1 | slice-index | `ipv6_to_sixlowpan` | `&mut buffer[..udp_repr.header_len() + payload.len()],` |
| `src/iface/interface/sixlowpan.rs:532` | 1 | copy_from_slice | `ipv6_to_sixlowpan` | `\|buf\| buf.copy_from_slice(payload),` |
| `src/iface/interface/sixlowpan.rs:539` | 1 | slice-index | `ipv6_to_sixlowpan` | `&mut TcpPacket::new_unchecked(&mut buffer[..tcp_repr.buffer_len()]),` |
| `src/iface/interface/sixlowpan.rs:549` | 1 | panic!/unreachable! | `ipv6_to_sixlowpan` | `_ => unreachable!(),` |

### `src/wire/sixlowpan/iphc.rs` — 6 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/sixlowpan/iphc.rs:147` | 1 | slice-index | `hop_limit` | `data[start..start + 1][0]` |
| `src/wire/sixlowpan/iphc.rs:206` | 2 | slice-index | `flow_label_field` | `&self.buffer.as_ref()[start..][2..4],` |
| `src/wire/sixlowpan/iphc.rs:212` | 2 | slice-index | `flow_label_field` | `&self.buffer.as_ref()[start..][1..3],` |
| `src/wire/sixlowpan/iphc.rs:845` | 1 | panic!/unreachable! | `buffer_len` | `_ => unreachable!(),` |

### `src/iface/neighbor.rs` — 4 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/iface/neighbor.rs:131` | 1 | unwrap | `fill_with_expiration` | `let _old_neighbor = self.storage.remove(&old_protocol_addr).unwrap();` |
| `src/iface/neighbor.rs:143` | 1 | panic!/unreachable! | `fill_with_expiration` | `_ => unreachable!(),` |
| `src/iface/neighbor.rs:150` | 2 | panic!/unreachable! | `lookup` | `assert!(protocol_addr.is_unicast());` |

### `src/wire/ip.rs` — 4 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ip.rs:992` | 4 | panic!/unreachable! | `pseudo_header` | `_ => unreachable!(),` |

### `src/wire/ipv6.rs` — 4 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ipv6.rs:163` | 3 | panic!/unreachable! | `mask` | `assert!(mask <= 128);` |
| `src/wire/ipv6.rs:178` | 1 | panic!/unreachable! | `solicited_node` | `assert!(self.x_is_unicast());` |

### `src/socket/dhcpv4.rs` — 3 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/socket/dhcpv4.rs:315` | 1 | panic!/unreachable! | `process` | `assert!(repr.src_port == self.server_port && repr.dst_port == self.client_port);` |
| `src/socket/dhcpv4.rs:333` | 1 | panic!(fmt) | `process` | `panic!("using DHCPv4 socket with a non-ethernet hardware address.");` |
| `src/socket/dhcpv4.rs:570` | 1 | panic!(fmt) | `dispatch` | `panic!("using DHCPv4 socket with a non-ethernet hardware address.");` |

### `src/wire/mld.rs` — 3 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/mld.rs:134` | 1 | panic!/unreachable! | `set_qrv` | `assert!(value < 8);` |
| `src/wire/mld.rs:282` | 1 | panic!/unreachable! | `set_mcast_addr` | `assert!(addr.is_multicast());` |
| `src/wire/mld.rs:284` | 1 | slice-index | `set_mcast_addr` | `data[field::RECORD_MCAST_ADDR].copy_from_slice(&addr.octets());` |

### `src/wire/mod.rs` — 3 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/mod.rs:441` | 2 | panic!(fmt) | `ethernet_or_panic` | `_ => panic!("HardwareAddress is not Ethernet."),` |
| `src/wire/mod.rs:450` | 1 | panic!(fmt) | `ieee802154_or_panic` | `_ => panic!("HardwareAddress is not Ethernet."),` |

### `src/wire/sixlowpan/nhc.rs` — 3 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/sixlowpan/nhc.rs:525` | 1 | slice-index | `src_port` | `NetworkEndian::read_u16(&data[start..start + 2])` |
| `src/wire/sixlowpan/nhc.rs:553` | 1 | slice-index | `dst_port` | `NetworkEndian::read_u16(&data[idx + 2..idx + 4])` |
| `src/wire/sixlowpan/nhc.rs:567` | 1 | slice-index | `dst_port` | `NetworkEndian::read_u16(&data[idx + 1..idx + 1 + 2])` |

### `src/iface/interface/ipv6.rs` — 2 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/iface/interface/ipv6.rs:31` | 1 | panic!/unreachable! | `get_source_address_ipv6` | `assert!(!dst_addr.is_unspecified());` |
| `src/iface/interface/ipv6.rs:98` | 1 | unwrap | `get_source_address_ipv6` | `.unwrap(); // NOTE: we check above that there is at least one IPv6 address.` |

### `src/storage/ring_buffer.rs` — 2 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/storage/ring_buffer.rs:345` | 1 | panic!/unreachable! | `enqueue_unallocated` | `assert!(count <= self.window());` |
| `src/storage/ring_buffer.rs:398` | 1 | panic!/unreachable! | `dequeue_allocated` | `assert!(count <= self.len());` |

### `src/iface/route.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/iface/route.rs:173` | 1 | panic!/unreachable! | `lookup` | `assert!(addr.is_unicast());` |

### `src/phy/mod.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/phy/mod.rs:67` | 1 | panic!(fmt) | `from_driver` | `medium => panic!(` |

### `src/socket/tcp.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/socket/tcp.rs:592` | 1 | panic!(fmt) | `new` | `panic!("receiving buffer too large, cannot exceed 1 GiB")` |

### `src/socket/udp.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/socket/udp.rs:643` | 1 | copy_from_slice | `process` | `Ok(buf) => buf.copy_from_slice(payload),` |

### `src/storage/packet_buffer.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/storage/packet_buffer.rs:215` | 1 | unwrap | `dequeue` | `Ok((meta.header.take().unwrap(), payload_buf))` |

### `src/wire/ipv4.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ipv4.rs:101` | 1 | panic!/unreachable! | `new` | `assert!(prefix_len <= 32);` |

---

<a id="phase-3"></a>
## Phase 3 — xarxa CORE

62 sites. Iterator / Option / Result chains Flux cannot see through. Same shape as the byteorder work in PR #14: copy the dependency closure from flux/lib/flux-core/src/ into flux_specs.rs. Do NOT load flux-core wholesale.

### `src/wire/sixlowpan/mod.rs` — 9 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/sixlowpan/mod.rs:90` | 1 | copy_from_slice | `resolve` | `bytes[8..].copy_from_slice(inline);` |
| `src/wire/sixlowpan/mod.rs:96` | 1 | copy_from_slice | `resolve` | `bytes[14..].copy_from_slice(inline);` |
| `src/wire/sixlowpan/mod.rs:117` | 1 | bounds-check | `resolve` | `bytes[1] = inline[0];` |
| `src/wire/sixlowpan/mod.rs:118` | 1 | slice-index | `resolve` | `bytes[11..].copy_from_slice(&inline[1..][..5]);` |
| `src/wire/sixlowpan/mod.rs:123` | 1 | bounds-check | `resolve` | `bytes[1] = inline[0];` |
| `src/wire/sixlowpan/mod.rs:124` | 1 | slice-index | `resolve` | `bytes[13..].copy_from_slice(&inline[1..][..3]);` |
| `src/wire/sixlowpan/mod.rs:130` | 1 | bounds-check | `resolve` | `bytes[15] = inline[0];` |
| `src/wire/sixlowpan/mod.rs:139` | 1 | slice-index | `resolve` | `bytes[16 - inline.len()..].copy_from_slice(inline);` |
| `src/wire/sixlowpan/mod.rs:144` | 1 | slice-index | `resolve` | `bytes[16 - inline.len()..].copy_from_slice(inline);` |

### `src/wire/ieee802154.rs` — 6 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ieee802154.rs:371` | 2 | slice-index | `frame_type` | `let raw = LittleEndian::read_u16(&data[field::FRAMECONTROL]);` |
| `src/wire/ieee802154.rs:388` | 1 | slice-index | `dst_addressing_mode` | `let raw = LittleEndian::read_u16(&data[field::FRAMECONTROL]);` |
| `src/wire/ieee802154.rs:406` | 1 | slice-index | `src_addressing_mode` | `let raw = LittleEndian::read_u16(&data[field::FRAMECONTROL]);` |
| `src/wire/ieee802154.rs:543` | 2 | slice-index | `src_pan_id` | `&addressing_fields[offset..][..2],` |

### `src/wire/ipv6.rs` — 6 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ipv6.rs:475` | 1 | slice-index | `src_addr` | `Address::from_octets(data[field::SRC_ADDR].try_into().unwrap())` |
| `src/wire/ipv6.rs:482` | 1 | slice-index | `dst_addr` | `Address::from_octets(data[field::DST_ADDR].try_into().unwrap())` |
| `src/wire/ipv6.rs:523` | 1 | bounds-check | `set_flow_label` | `let raw = (((data[1] & 0xf0) as u32) << 16) \| (value & 0x0fffff);` |
| `src/wire/ipv6.rs:524` | 3 | slice-index | `set_flow_label` | `NetworkEndian::write_u24(&mut data[1..4], raw);` |

### `src/wire/tcp.rs` — 6 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/tcp.rs:423` | 1 | slice-index | `set_seq_number` | `NetworkEndian::write_i32(&mut data[field::SEQ_NUM], value.0)` |
| `src/wire/tcp.rs:430` | 1 | slice-index | `set_ack_number` | `NetworkEndian::write_i32(&mut data[field::ACK_NUM], value.0)` |
| `src/wire/tcp.rs:694` | 1 | slice-index | `parse` | `let range_left = NetworkEndian::read_u32(&data[left..mid]);` |
| `src/wire/tcp.rs:695` | 1 | slice-index | `parse` | `let range_right = NetworkEndian::read_u32(&data[mid..right]);` |
| `src/wire/tcp.rs:712` | 1 | slice-index | `parse` | `Ok((&buffer[length..], option))` |
| `src/wire/tcp.rs:1053` | 1 | slice-index | `emit` | `packet.payload_mut()[..self.payload.len()].copy_from_slice(self.payload);` |

### `src/wire/icmpv6.rs` — 5 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/icmpv6.rs:680` | 1 | slice-index | `parse` | `let payload = &packet.payload()[ip_packet.header_len()..];` |
| `src/wire/icmpv6.rs:787` | 1 | slice-index | `emit` | `let payload = &mut ip_packet.into_inner()[header.buffer_len()..];` |
| `src/wire/icmpv6.rs:794` | 1 | slice-index | `emit` | `payload[..payload_len].copy_from_slice(&data[..payload_len]);` |
| `src/wire/icmpv6.rs:851` | 1 | slice-index | `emit` | `packet.payload_mut()[..data_len].copy_from_slice(&data[..data_len])` |
| `src/wire/icmpv6.rs:864` | 1 | slice-index | `emit` | `packet.payload_mut()[..data_len].copy_from_slice(&data[..data_len])` |

### `src/iface/interface/sixlowpan.rs` — 4 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/iface/interface/sixlowpan.rs:81` | 1 | slice-index | `process_sixlowpan` | `Ok(len) => &f.decompress_buf[..len],` |
| `src/iface/interface/sixlowpan.rs:771` | 1 | slice-index | `decompress_udp` | `let mut udp = UdpPacket::new_unchecked(&mut buffer[..payload.len() + 8]);` |
| `src/iface/interface/sixlowpan.rs:773` | 2 | slice-index | `decompress_udp` | `buffer[8..][..payload.len()].copy_from_slice(payload);` |

### `src/storage/ring_buffer.rs` — 4 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/storage/ring_buffer.rs:314` | 1 | slice-index | `get_unallocated` | `&mut self.storage[start_at..start_at + size]` |
| `src/storage/ring_buffer.rs:369` | 3 | slice-index | `get_allocated` | `&self.storage[start_at..start_at + size]` |

### `src/wire/icmpv4.rs` — 4 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/icmpv4.rs:529` | 1 | slice-index | `emit` | `let payload = &mut ip_packet.into_inner()[header.buffer_len()..];` |
| `src/wire/icmpv4.rs:530` | 1 | copy_from_slice | `emit` | `payload.copy_from_slice(data)` |
| `src/wire/icmpv4.rs:543` | 1 | slice-index | `emit` | `let payload = &mut ip_packet.into_inner()[header.buffer_len()..];` |
| `src/wire/icmpv4.rs:544` | 1 | copy_from_slice | `emit` | `payload.copy_from_slice(data)` |

### `src/wire/ndiscoption.rs` — 4 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ndiscoption.rs:369` | 1 | slice-index | `clear_redirected_reserved` | `data[field::REDIRECTED_RESERVED].fill_with(\|\| 0);` |
| `src/wire/ndiscoption.rs:488` | 1 | slice-index | `parse` | `data: &redirected_packet[ip_repr.buffer_len()..][..ip_repr.payload_len],` |
| `src/wire/ndiscoption.rs:574` | 1 | copy_from_slice | `emit` | `ip_packet.payload_mut().copy_from_slice(data);` |
| `src/wire/ndiscoption.rs:588` | 1 | copy_from_slice | `emit` | `opt.data_mut().copy_from_slice(data);` |

### `src/wire/dhcpv4.rs` — 3 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/dhcpv4.rs:428` | 1 | slice-index | `set_sname_and_boot_file_to_zero` | `for byte in &mut data[field::SNAME] {` |
| `src/wire/dhcpv4.rs:431` | 1 | slice-index | `set_sname_and_boot_file_to_zero` | `for byte in &mut data[field::FILE] {` |
| `src/wire/dhcpv4.rs:935` | 1 | slice-index | `emit` | `servers[(i * IP_SIZE)..((i + 1) * IP_SIZE)].copy_from_slice(&ip.octets());` |

### `src/wire/ipv6hbh.rs` — 2 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ipv6hbh.rs:104` | 1 | slice-index | `emit` | `&mut buffer[..opt.buffer_len()],` |
| `src/wire/ipv6hbh.rs:106` | 1 | slice-index | `emit` | `buffer = &mut buffer[opt.buffer_len()..];` |

### `src/wire/ndisc.rs` — 2 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ndisc.rs:81` | 1 | slice-index | `target_addr` | `Ipv6Address::from_octets(data[field::TARGET_ADDR].try_into().unwrap())` |
| `src/wire/ndisc.rs:107` | 1 | slice-index | `dest_addr` | `Ipv6Address::from_octets(data[field::DEST_ADDR].try_into().unwrap())` |

### `src/iface/interface/ipv6.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/iface/interface/ipv6.rs:317` | 1 | slice-index | `process_hopbyhop` | `&ip_payload[ext_repr.header_len() + ext_repr.data.len()..],` |

### `src/socket/tcp.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/socket/tcp.rs:2323` | 1 | unwrap | `seq_to_transmit` | `let ip_header_len = match self.tuple.unwrap().local.addr {` |

### `src/storage/assembler.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/storage/assembler.rs:233` | 1 | bounds-check | `add` | `self.contigs[i + 1].shrink_hole_by(offset + size);` |

### `src/storage/packet_buffer.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/storage/packet_buffer.rs:227` | 1 | unwrap | `peek` | `metadata.header.as_ref().unwrap(),` |

### `src/wire/ipv6option.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/ipv6option.rs:366` | 1 | slice-index | `emit` | `opt.data_mut().copy_from_slice(&data[..length as usize]);` |

### `src/wire/mld.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/mld.rs:52` | 1 | slice-index | `mcast_addr` | `Ipv6Address::from_octets(data[field::QUERY_MCAST_ADDR].try_into().unwrap())` |

### `src/wire/mod.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/wire/mod.rs:549` | 1 | slice-index | `as_bytes` | `&self.data[..self.len as usize]` |

---

<a id="phase-4"></a>
## Phase 4 — compiler work

20 sites. Flux itself falls over: `internal flux error`, or rustc aborts. Not delegable. The `<&T as AsRef<[u8]>>::idx` gap belongs here too -- it has no site of its own but gates payload() in 16 wire files.

**Also in this phase:** the `<&T as AsRef<[u8]>>::idx` gap. Repro is left uncommitted in `/Users/andrew/research/xarxa-icmpv6` at `src/wire/icmpv6.rs:529` — 0 `panicked`, exactly 2 errors, one function. ICE-2 made the signature convert; it still does not discharge.

### `src/storage/ring_buffer.rs` — 11 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/storage/ring_buffer.rs:154` | 3 | bounds-check | `dequeue_one_with` | `let res = f(&mut self.storage[self.read_at]);` |
| `src/storage/ring_buffer.rs:193` | 3 | slice-index | `enqueue_many_with` | `let (size, result) = f(&mut self.storage[write_at..write_at + max_size]);` |
| `src/storage/ring_buffer.rs:245` | 5 | slice-index | `dequeue_many_with` | `let (size, result) = f(&mut self.storage[self.read_at..self.read_at + max_size]);` |

### `src/iface/interface/mod.rs` — 7 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/iface/interface/mod.rs:212` | 1 | Medium> | `new` | `assert_eq!(` |
| `src/iface/interface/mod.rs:814` | 1 | expect | `socket_egress` | `neighbor_addr.expect("non-IP response packet"),` |
| `src/iface/interface/mod.rs:920` | 1 | panic!(fmt) | `check_ip_addrs` | `panic!("IP address {} is not unicast", cidr.address())` |
| `src/iface/interface/mod.rs:1122` | 1 | panic!/unreachable! | `lookup_hardware_addr` | `Medium::Ieee802154 => unreachable!(),` |
| `src/iface/interface/mod.rs:1245` | 1 | panic!/unreachable! | `dispatch_ip` | `assert!(!ip_repr.dst_addr().is_unspecified());` |
| `src/iface/interface/mod.rs:1281` | 1 | panic!/unreachable! | `dispatch_ip` | `(_, _) => unreachable!(),` |
| `src/iface/interface/mod.rs:1308` | 1 | slice-index | `dispatch_ip` | `let payload = &mut tx_buffer[repr.header_len()..];` |

### `src/storage/packet_buffer.rs` — 2 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `src/storage/packet_buffer.rs:195` | 1 | unwrap | `dequeue_with` | `metadata.header.as_mut().unwrap(),` |
| `src/storage/packet_buffer.rs:196` | 1 | slice-index | `dequeue_with` | `&mut payload_buf[..metadata.size],` |

---

<a id="phase-5"></a>
## Phase 5 — logging and formatting

33 sites. defmt, defmt-rtt and core's integer formatting. NOT proof targets: no annotation removes these, they only go away if the example builds without defmt. A decision about what the benchmark may be.

### `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/defmt-1.1.1/src/export/mod.rs` — 25 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/defmt-1.1.1/src/export/mod.rs:133` | 25 | defmt | `` | `unsafe { _defmt_panic() }` |

### `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/defmt-rtt-1.3.0/src/channel.rs` — 3 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/defmt-rtt-1.3.0/src/channel.rs:41` | 3 | slice-index | `` | `bytes = &bytes[consumed..];` |

### `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/defmt-rtt-1.3.0/src/lib.rs` — 2 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/defmt-rtt-1.3.0/src/lib.rs:173` | 1 | panic!(fmt) | `` | `panic!("defmt logger taken reentrantly")` |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/defmt-rtt-1.3.0/src/lib.rs:226` | 1 | panic!(fmt) | `` | `panic!("defmt release out of context")` |

### `/rustc/8bab26f4f68e0e26f0bb7960be334d5b520ea452/library/core/src/num/imp/int_log10.rs` — 2 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `/rustc/8bab26f4f68e0e26f0bb7960be334d5b520ea452/library/core/src/num/imp/int_log10.rs:45` | 1 | defmt | `` | `` |
| `/rustc/8bab26f4f68e0e26f0bb7960be334d5b520ea452/library/core/src/num/imp/int_log10.rs:90` | 1 | defmt | `` | `` |

### `/rustc/8bab26f4f68e0e26f0bb7960be334d5b520ea452/library/core/src/fmt/num.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `/rustc/8bab26f4f68e0e26f0bb7960be334d5b520ea452/library/core/src/fmt/num.rs:448` | 1 | unwrap | `` | `` |

---

<a id="phase-6"></a>
## Phase 6 — the embassy crates and other dependencies

164 sites. Outside xarxa entirely, so no xarxa proof reaches them. Lives in ninehusky/embassy, a fork we control, so the same opt-in method applies -- but this is async executors and USB state machines, expect it to be harder.

### `embassy-nrf/src/usb/mod.rs` — 20 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `embassy-nrf/src/usb/mod.rs` (no line) | 2 | defmt | `` | `` |
| `embassy-nrf/src/usb/mod.rs:189` | 1 | async-resumed | `` | `async fn enable(&mut self) {` |
| `embassy-nrf/src/usb/mod.rs:228` | 1 | async-resumed | `` | `async fn disable(&mut self) {` |
| `embassy-nrf/src/usb/mod.rs:419` | 3 | bounds-check | `` | `&EP_IN_WAKERS[i - 1]` |
| `embassy-nrf/src/usb/mod.rs:436` | 2 | bounds-check | `` | `&EP_OUT_WAKERS[i - 1]` |
| `embassy-nrf/src/usb/mod.rs:472` | 1 | async-resumed | `` | `async fn wait_enabled(&mut self) {` |
| `embassy-nrf/src/usb/mod.rs:503` | 2 | async-resumed | `` | `{` |
| `embassy-nrf/src/usb/mod.rs:576` | 1 | async-resumed | `` | `async fn read(&mut self, buf: &mut [u8]) -> Result<usize, EndpointError> {` |
| `embassy-nrf/src/usb/mod.rs:587` | 1 | async-resumed | `` | `async fn write(&mut self, buf: &[u8]) -> Result<(), EndpointError> {` |
| `embassy-nrf/src/usb/mod.rs:611` | 1 | async-resumed | `` | `async fn setup(&mut self) -> [u8; 8] {` |
| `embassy-nrf/src/usb/mod.rs:645` | 1 | async-resumed | `` | `async fn data_out(&mut self, buf: &mut [u8], _first: bool, _last: bool) -> Result<usize,` |
| `embassy-nrf/src/usb/mod.rs:679` | 1 | async-resumed | `` | `async fn data_in(&mut self, buf: &[u8], _first: bool, last: bool) -> Result<(), Endpoint` |
| `embassy-nrf/src/usb/mod.rs:713` | 1 | async-resumed | `` | `async fn accept(&mut self) {` |
| `embassy-nrf/src/usb/mod.rs:718` | 1 | async-resumed | `` | `async fn reject(&mut self) {` |
| `embassy-nrf/src/usb/mod.rs:723` | 1 | async-resumed | `` | `async fn accept_set_address(&mut self, _addr: u8) {` |

### `embassy-sync/src/zerocopy_channel.rs` — 18 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `embassy-sync/src/zerocopy_channel.rs:127` | 4 | RefCell | `` | `let s = &mut *s.borrow_mut();` |
| `embassy-sync/src/zerocopy_channel.rs:141` | 3 | RefCell | `` | `let s = &mut *s.borrow_mut();` |
| `embassy-sync/src/zerocopy_channel.rs:159` | 1 | RefCell | `` | `let s = &mut *s.borrow_mut();` |
| `embassy-sync/src/zerocopy_channel.rs:215` | 5 | RefCell | `` | `self.state.lock(\|s\| s.borrow_mut().push_done());` |
| `embassy-sync/src/zerocopy_channel.rs:234` | 1 | RefCell | `` | `let s = &mut *s.borrow_mut();` |
| `embassy-sync/src/zerocopy_channel.rs:248` | 1 | RefCell | `` | `let s = &mut *s.borrow_mut();` |
| `embassy-sync/src/zerocopy_channel.rs:266` | 1 | RefCell | `` | `let s = &mut *s.borrow_mut();` |
| `embassy-sync/src/zerocopy_channel.rs:329` | 2 | RefCell | `` | `self.state.lock(\|s\| s.borrow_mut().pop_done());` |

### `embassy-usb/src/lib.rs` — 18 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `embassy-usb/src/lib.rs:273` | 1 | async-resumed | `` | `pub async fn run_until_suspend(&mut self) {` |
| `embassy-usb/src/lib.rs:301` | 1 | async-resumed | `` | `pub async fn wait_resume(&mut self) {` |
| `embassy-usb/src/lib.rs:331` | 1 | async-resumed | `` | `async fn handle_control(&mut self, req: [u8; 8]) {` |
| `embassy-usb/src/lib.rs:342` | 1 | async-resumed | `` | `async fn handle_control_in(&mut self, req: Request) {` |
| `embassy-usb/src/lib.rs:360` | 1 | rem-by-zero | `` | `let needs_zlp = len != resp_length && (len % max_packet_size) == 0;` |
| `embassy-usb/src/lib.rs:370` | 1 | async-resumed | `` | `async fn handle_control_out(&mut self, req: Request) {` |
| `embassy-usb/src/lib.rs:395` | 1 | slice-index | `` | `let data = &self.control_buf[0..total];` |
| `embassy-usb/src/lib.rs:416` | 1 | async-resumed | `` | `async fn handle_bus_event(&mut self, evt: Event) {` |
| `embassy-usb/src/lib.rs:507` | 1 | bounds-check | `` | `let iface = &self.interfaces[ep.interface.0 as usize];` |
| `embassy-usb/src/lib.rs:609` | 1 | slice-index | `` | `buf[..2].copy_from_slice(&status.to_le_bytes());` |
| `embassy-usb/src/lib.rs:618` | 1 | bounds-check | `` | `buf[0] = status;` |
| `embassy-usb/src/lib.rs:631` | 1 | slice-index | `` | `buf[..2].copy_from_slice(&status.to_le_bytes());` |
| `embassy-usb/src/lib.rs:635` | 1 | bounds-check | `` | `buf[0] = iface.current_alt_setting;` |
| `embassy-usb/src/lib.rs:648` | 1 | slice-index | `` | `buf[..2].copy_from_slice(&status.to_le_bytes());` |
| `embassy-usb/src/lib.rs:708` | 1 | bounds-check | `` | `buf[0] = 4; // len` |
| `embassy-usb/src/lib.rs:709` | 1 | bounds-check | `` | `buf[1] = descriptor_type::STRING;` |
| `embassy-usb/src/lib.rs:710` | 1 | bounds-check | `` | `buf[2] = lang_id::ENGLISH_US as u8;` |
| `embassy-usb/src/lib.rs:711` | 1 | bounds-check | `` | `buf[3] = (lang_id::ENGLISH_US >> 8) as u8;` |

### `embassy-net-driver-channel/src/lib.rs` — 17 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `embassy-net-driver-channel/src/lib.rs:122` | 1 | slice-index | `` | `&self.0.buf[..len]` |
| `embassy-net-driver-channel/src/lib.rs:233` | 1 | RefCell | `` | `let s = &mut *s.borrow_mut();` |
| `embassy-net-driver-channel/src/lib.rs:260` | 1 | async-resumed | `` | `pub async fn rx_buf(&mut self) -> RxSlot<'_, MTU> {` |
| `embassy-net-driver-channel/src/lib.rs:280` | 1 | async-resumed | `` | `pub async fn tx_buf(&mut self) -> TxSlot<'_, MTU> {` |
| `embassy-net-driver-channel/src/lib.rs:400` | 2 | RefCell | `` | `self.shared.lock(\|s\| s.borrow().hardware_address)` |
| `embassy-net-driver-channel/src/lib.rs:405` | 1 | RefCell | `` | `let s = &mut *s.borrow_mut();` |
| `embassy-net-driver-channel/src/lib.rs:425` | 1 | panic!(fmt) | `` | `let mut pkt = unwrap!(self.rx.try_receive());` |
| `embassy-net-driver-channel/src/lib.rs:427` | 1 | slice-index | `` | `let r = f(&mut pkt.buf[..len]);` |
| `embassy-net-driver-channel/src/lib.rs:446` | 4 | panic!(fmt) | `` | `let mut pkt = unwrap!(self.tx.try_send());` |
| `embassy-net-driver-channel/src/lib.rs:447` | 4 | slice-index | `` | `let r = f(&mut pkt.buf[..len]);` |

### `embassy-usb/src/class/cdc_ncm/mod.rs` — 14 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `embassy-usb/src/class/cdc_ncm/mod.rs` (no line) | 3 | defmt, unwrap | `` | `` |
| `embassy-usb/src/class/cdc_ncm/mod.rs:115` | 1 | slice-index | `` | `&buf[..len]` |
| `embassy-usb/src/class/cdc_ncm/mod.rs:380` | 1 | async-resumed | `` | `pub async fn write_packet(&mut self, data: &[u8]) -> Result<(), EndpointError> {` |
| `embassy-usb/src/class/cdc_ncm/mod.rs:411` | 1 | slice-index | `` | `buf[OUT_HEADER_LEN..][..data.len()].copy_from_slice(data);` |
| `embassy-usb/src/class/cdc_ncm/mod.rs:414` | 1 | panic!(fmt) | `` | `let (d1, d2) = data.split_at(self.max_packet_size - OUT_HEADER_LEN);` |
| `embassy-usb/src/class/cdc_ncm/mod.rs:416` | 2 | copy_from_slice, slice-index | `` | `buf[OUT_HEADER_LEN..self.max_packet_size].copy_from_slice(d1);` |
| `embassy-usb/src/class/cdc_ncm/mod.rs:417` | 1 | slice-index | `` | `self.write_ep.write(&buf[..self.max_packet_size]).await?;` |
| `embassy-usb/src/class/cdc_ncm/mod.rs:439` | 1 | async-resumed | `` | `pub async fn read_packet(&mut self, buf: &mut [u8]) -> Result<usize, EndpointError> {` |
| `embassy-usb/src/class/cdc_ncm/mod.rs:446` | 1 | slice-index | `` | `let ntb = &ntb[..pos];` |
| `embassy-usb/src/class/cdc_ncm/mod.rs:483` | 1 | slice-index | `` | `buf[..datagram_len].copy_from_slice(datagram);` |
| `embassy-usb/src/class/cdc_ncm/mod.rs:490` | 1 | async-resumed | `` | `pub async fn wait_connection(&mut self) -> Result<(), EndpointError> {` |

### `embassy-usb/src/descriptor.rs` — 14 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `embassy-usb/src/descriptor.rs:98` | 1 | slice-index | `` | `&mut self.buf[..self.position]` |
| `embassy-usb/src/descriptor.rs:117` | 1 | bounds-check | `` | `self.buf[self.position] = (total_length + 2) as u8;` |
| `embassy-usb/src/descriptor.rs:118` | 1 | bounds-check | `` | `self.buf[self.position + 1] = descriptor_type;` |
| `embassy-usb/src/descriptor.rs:122` | 1 | slice-index | `` | `self.buf[start..start + descriptor_length].copy_from_slice(descriptor);` |
| `embassy-usb/src/descriptor.rs:123` | 1 | slice-index | `` | `self.buf[start + descriptor_length..start + total_length].copy_from_slice(extra_fields);` |
| `embassy-usb/src/descriptor.rs:154` | 1 | slice-index | `` | `self.buf[2..4].copy_from_slice(&position.to_le_bytes());` |
| `embassy-usb/src/descriptor.rs:218` | 1 | bounds-check | `` | `Some(mark) => self.buf[mark] += 1,` |
| `embassy-usb/src/descriptor.rs:261` | 1 | bounds-check | `` | `Some(mark) => self.buf[mark] += 1,` |
| `embassy-usb/src/descriptor.rs:431` | 1 | bounds-check | `` | `Some(mark) => self.writer.buf[mark] += 1,` |
| `embassy-usb/src/descriptor.rs:443` | 1 | bounds-check | `` | `self.writer.buf[start] = (blen + 3) as u8;` |
| `embassy-usb/src/descriptor.rs:444` | 1 | bounds-check | `` | `self.writer.buf[start + 1] = descriptor_type::CAPABILITY;` |
| `embassy-usb/src/descriptor.rs:445` | 1 | bounds-check | `` | `self.writer.buf[start + 2] = capability_type;` |
| `embassy-usb/src/descriptor.rs:448` | 1 | slice-index | `` | `self.writer.buf[start..start + blen].copy_from_slice(data);` |
| `embassy-usb/src/descriptor.rs:458` | 1 | slice-index | `` | `self.writer.buf[2..4].copy_from_slice(&position.to_le_bytes());` |

### `embassy-net/src/lib.rs` — 9 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `embassy-net/src/lib.rs:488` | 1 | RefCell | `` | `f(&self.inner.borrow())` |
| `embassy-net/src/lib.rs:492` | 8 | RefCell | `` | `f(&mut self.inner.borrow_mut())` |

### `embassy-usb-driver/src/lib.rs` — 9 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `embassy-usb-driver/src/lib.rs:273` | 1 | async-resumed | `` | `async fn read_transfer(&mut self, buf: &mut [u8]) -> Result<usize, EndpointError> {` |
| `embassy-usb-driver/src/lib.rs:276` | 1 | slice-index | `` | `let i = self.read(&mut buf[n..]).await?;` |
| `embassy-usb-driver/src/lib.rs:376` | 1 | async-resumed | `` | `async fn data_out_transfer(&mut self, buf: &mut [u8]) -> Result<usize, EndpointError> {` |
| `embassy-usb-driver/src/lib.rs:381` | 1 | panic!(fmt) | `` | `let chunks = buf.chunks_mut(self.max_packet_size());` |
| `embassy-usb-driver/src/lib.rs:399` | 1 | async-resumed | `` | `async fn data_in_transfer(&mut self, data: &[u8], needs_zlp: bool) -> Result<(), Endpoin` |
| `embassy-usb-driver/src/lib.rs:401` | 1 | panic!(fmt) | `` | `.chunks(self.max_packet_size())` |
| `embassy-usb-driver/src/lib.rs:449` | 1 | async-resumed | `` | `async fn write_transfer(&mut self, buf: &[u8], needs_zlp: bool) -> Result<(), EndpointEr` |
| `embassy-usb-driver/src/lib.rs:450` | 1 | panic!(fmt) | `` | `for chunk in buf.chunks(self.info().max_packet_size as usize) {` |
| `embassy-usb-driver/src/lib.rs:453` | 1 | rem-by-zero | `` | `if needs_zlp && buf.len() % self.info().max_packet_size as usize == 0 {` |

### `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/nrf-pac-0.4.0/src/./chips/nrf52840/pac.rs` — 8 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/nrf-pac-0.4.0/src/./chips/nrf52840/pac.rs:40264` | 1 | panic!/unreachable! | `` | `assert!(n < 8usize);` |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/nrf-pac-0.4.0/src/./chips/nrf52840/pac.rs:40275` | 1 | panic!/unreachable! | `` | `assert!(n < 8usize);` |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/nrf-pac-0.4.0/src/./chips/nrf52840/pac.rs:40367` | 2 | panic!/unreachable! | `` | `assert!(n < 8usize);` |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/nrf-pac-0.4.0/src/./chips/nrf52840/pac.rs:40658` | 1 | panic!/unreachable! | `` | `assert!(n < 8usize);` |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/nrf-pac-0.4.0/src/./chips/nrf52840/pac.rs:41119` | 2 | panic!/unreachable! | `` | `assert!(n < 8usize);` |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/nrf-pac-0.4.0/src/./chips/nrf52840/pac.rs:41254` | 1 | panic!/unreachable! | `` | `assert!(n < 8usize);` |

### `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/heapless-0.9.3/src/vec/mod.rs` — 5 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/heapless-0.9.3/src/vec/mod.rs:922` | 1 | panic!/unreachable! | `` | `assert!(index < self.len());` |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/heapless-0.9.3/src/vec/mod.rs:1094` | 4 | panic!(fmt) | `` | `panic!("removal index (is {index}) should be < len (is {len})");` |

### `/Users/andrew/.rustup/toolchains/1.97-aarch64-apple-darwin/lib/rustlib/src/rust/library/core/src/result.rs` — 5 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `/Users/andrew/.rustup/toolchains/1.97-aarch64-apple-darwin/lib/rustlib/src/rust/library/core/src/result.rs:1185` | 1 | unwrap | `` | `Err(e) => unwrap_failed(msg, &e),` |
| `/Users/andrew/.rustup/toolchains/1.97-aarch64-apple-darwin/lib/rustlib/src/rust/library/core/src/result.rs:1233` | 4 | unwrap | `` | `Err(e) => unwrap_failed("called `Result::unwrap()` on an `Err` value", &e),` |

### `embassy-usb/src/msos.rs` — 4 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `embassy-usb/src/msos.rs:72` | 1 | slice-index | `` | `descriptor: &self.buf[..self.position],` |
| `embassy-usb/src/msos.rs:164` | 3 | slice-index | `` | `buf[p..(p + 2)].copy_from_slice(&(len as u16).to_le_bytes());` |

### `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/byteorder-1.5.0/src/lib.rs` — 3 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/byteorder-1.5.0/src/lib.rs:1979` | 1 | slice-index | `` | `buf[..2].copy_from_slice(&n.to_be_bytes());` |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/byteorder-1.5.0/src/lib.rs:1984` | 2 | slice-index | `` | `buf[..4].copy_from_slice(&n.to_be_bytes());` |

### `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/embedded-io-async-0.7.0/src/lib.rs` — 3 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/embedded-io-async-0.7.0/src/lib.rs:139` | 1 | async-resumed | `` | `async fn write_all(&mut self, buf: &[u8]) -> Result<(), Self::Error> {` |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/embedded-io-async-0.7.0/src/lib.rs:143` | 1 | panic!(fmt) | `` | `Ok(0) => panic!("write() returned Ok(0)"),` |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/embedded-io-async-0.7.0/src/lib.rs:144` | 1 | slice-index | `` | `Ok(n) => buf = &buf[n..],` |

### `embassy-nrf/src/time_driver.rs` — 3 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `embassy-nrf/src/time_driver.rs:328` | 1 | RefCell | `` | `let mut next = self.queue.borrow(cs).borrow_mut().next_expiration(self.now());` |
| `embassy-nrf/src/time_driver.rs:330` | 1 | RefCell | `` | `next = self.queue.borrow(cs).borrow_mut().next_expiration(self.now());` |
| `embassy-nrf/src/time_driver.rs:428` | 1 | RefCell | `` | `let mut queue = self.queue.borrow(cs).borrow_mut();` |

### `/rustc/8bab26f4f68e0e26f0bb7960be334d5b520ea452/library/core/src/net/display_buffer.rs` — 2 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `/rustc/8bab26f4f68e0e26f0bb7960be334d5b520ea452/library/core/src/net/display_buffer.rs:21` | 2 | slice-index | `` | `` |

### `/rustc/8bab26f4f68e0e26f0bb7960be334d5b520ea452/library/core/src/result.rs` — 2 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `/rustc/8bab26f4f68e0e26f0bb7960be334d5b520ea452/library/core/src/result.rs:1233` | 2 | unwrap | `` | `` |

### `embassy-net/src/tcp.rs` — 2 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `embassy-net/src/tcp.rs:429` | 1 | async-resumed | `` | `{` |
| `embassy-net/src/tcp.rs:1019` | 1 | async-resumed | `` | `async fn write(&mut self, buf: &[u8]) -> Result<usize, Self::Error> {` |

### `embassy-usb/src/builder.rs` — 2 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `embassy-usb/src/builder.rs:392` | 1 | bounds-check | `` | `self.builder.config_descriptor.buf[i] += 1;` |
| `embassy-usb/src/builder.rs:460` | 1 | bounds-check | `` | `self.builder.interfaces[self.interface_number.0 as usize].num_alt_settings += 1;` |

### `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/static_cell-2.1.1/src/lib.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `/Users/andrew/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/static_cell-2.1.1/src/lib.rs:84` | 1 | panic!(fmt) | `` | `panic!("`StaticCell` is already full, it can't be initialized twice.");` |

### `/rustc/8bab26f4f68e0e26f0bb7960be334d5b520ea452/library/core/src/net/ip_addr.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `/rustc/8bab26f4f68e0e26f0bb7960be334d5b520ea452/library/core/src/net/ip_addr.rs:2192` | 1 | slice-index | `` | `` |

### `embassy-nrf/src/gpiote.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `embassy-nrf/src/gpiote.rs:246` | 1 | bounds-check | `` | `PORT_WAKERS[port * 32 + pin as usize].wake();` |

### `embassy-nrf/src/rng.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `embassy-nrf/src/rng.rs:300` | 1 | RefCell | `` | `self.inner.borrow(cs).borrow_mut()` |

### `embassy-sync/src/waitqueue/atomic_waker.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `embassy-sync/src/waitqueue/atomic_waker.rs:191` | 1 | unwrap | `` | `let w = (*self.waker.get()).take().unwrap();` |

### `examples/nrf52840/src/bin/usb_ethernet.rs` — 1 sites

| span | sites | kind | fn | source |
| --- | ---: | --- | --- | --- |
| `examples/nrf52840/src/bin/usb_ethernet.rs:146` | 1 | slice-index | `` | `info!("rxd {:02x}", &buf[..n]);` |

