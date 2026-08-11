# Panic sites by source file

Every source line in the measured `usb_ethernet` binary that can panic. `sites` counts machine call sites; one source line becomes several when generics or inlining duplicate it, so `lines` is what tracks effort.

A `?` line means DWARF attributed the site to the file but to no statement — generic or heavily inlined code. The site is real; find it by its address in `results/modified.blame.tsv`.

| file | sites | lines |
| --- | --- | --- |
| [src/wire/sixlowpan/iphc.rs](#srcwiresixlowpaniphcrs) | 49 | 13 |
| [src/wire/tcp.rs](#srcwiretcprs) | 34 | 23 |
| [src/wire/ipv6.rs](#srcwireipv6rs) | 33 | 17 |
| [src/iface/socket_set.rs](#srcifacesocket_setrs) | 28 | 9 |
| [src/wire/icmpv6.rs](#srcwireicmpv6rs) | 26 | 13 |
| [src/wire/sixlowpan/nhc.rs](#srcwiresixlowpannhcrs) | 25 | 15 |
| [src/wire/ipv4.rs](#srcwireipv4rs) | 21 | 12 |
| [src/storage/ring_buffer.rs](#srcstoragering_bufferrs) | 20 | 9 |
| [src/wire/ieee802154.rs](#srcwireieee802154rs) | 18 | 7 |
| [src/wire/mld.rs](#srcwiremldrs) | 18 | 11 |
| [src/wire/udp.rs](#srcwireudprs) | 18 | 10 |
| [src/iface/interface/sixlowpan.rs](#srcifaceinterfacesixlowpanrs) | 16 | 14 |
| [src/wire/ndisc.rs](#srcwirendiscrs) | 16 | 14 |
| [src/wire/ndiscoption.rs](#srcwirendiscoptionrs) | 13 | 11 |
| [src/iface/packet.rs](#srcifacepacketrs) | 12 | 9 |
| [src/wire/sixlowpan/mod.rs](#srcwiresixlowpanmodrs) | 10 | 6 |
| [src/wire/arp.rs](#srcwirearprs) | 9 | 9 |
| [src/socket/tcp.rs](#srcsockettcprs) | 8 | 5 |
| [src/wire/icmpv4.rs](#srcwireicmpv4rs) | 8 | 7 |
| [src/iface/interface/mod.rs](#srcifaceinterfacemodrs) | 7 | 7 |
| [src/wire/ethernet.rs](#srcwireethernetrs) | 7 | 3 |
| [src/wire/ipv6option.rs](#srcwireipv6optionrs) | 7 | 4 |
| [src/storage/packet_buffer.rs](#srcstoragepacket_bufferrs) | 5 | 5 |
| [src/iface/neighbor.rs](#srcifaceneighborrs) | 4 | 3 |
| [src/wire/dhcpv4.rs](#srcwiredhcpv4rs) | 4 | 4 |
| [src/wire/ip.rs](#srcwireiprs) | 4 | 1 |
| [src/wire/mod.rs](#srcwiremodrs) | 4 | 3 |
| [src/iface/interface/ipv6.rs](#srcifaceinterfaceipv6rs) | 3 | 3 |
| [src/socket/dhcpv4.rs](#srcsocketdhcpv4rs) | 3 | 3 |
| [src/iface/route.rs](#srcifacerouters) | 2 | 2 |
| [src/wire/ipv6ext_header.rs](#srcwireipv6ext_headerrs) | 2 | 2 |
| [src/wire/ipv6hbh.rs](#srcwireipv6hbhrs) | 2 | 2 |
| [src/phy/mod.rs](#srcphymodrs) | 1 | 1 |
| [src/socket/udp.rs](#srcsocketudprs) | 1 | 1 |
| [src/storage/assembler.rs](#srcstorageassemblerrs) | 1 | 1 |

## src/wire/sixlowpan/iphc.rs

49 sites across 13 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| ? | 35 | bounds-check, slice-index | *no DWARF line; blamed to this file only* |
| 22 | 2 | slice-index | `let raw = NetworkEndian::read_u16(&data[field::IPHC_FIELD]);` |
| 133 | 1 | slice-index | `let nh = data[start..start + 1][0];` |
| 147 | 1 | slice-index | `data[start..start + 1][0]` |
| 206 | 1 | slice-index | `&self.buffer.as_ref()[start..][2..4],` |
| 212 | 1 | slice-index | `&self.buffer.as_ref()[start..][1..3],` |
| 332 | 1 | slice-index | `AddressMode::Multicast48bits(&data[start..][..6]),` |
| 335 | 1 | slice-index | `AddressMode::Multicast32bits(&data[start..][..4]),` |
| 338 | 1 | slice-index | `AddressMode::Multicast8bits(&data[start..][..1]),` |
| 455 | 1 | slice-index | `&data[len..]` |
| 462 | 1 | slice-index | `let data = &mut self.buffer.as_mut()[field::IPHC_FIELD];` |
| 481 | 2 | slice-index | `raw[idx..idx + value.len()].copy_from_slice(value);` |
| 845 | 1 | panic!/unreachable! | `_ => unreachable!(),` |

## src/wire/tcp.rs

34 sites across 23 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 44 | 7 | panic!(fmt) | `panic!("attempt to add to sequence number with unsigned overflow")` |
| 55 | 1 | panic!(fmt) | `panic!("attempt to subtract to sequence number with unsigned overflow")` |
| 73 | 6 | panic!(fmt) | `panic!("attempt to subtract sequence numbers with underflow")` |
| 392 | 1 | slice-index | `&data[field::OPTIONS(header_len)]` |
| 400 | 1 | slice-index | `&data[header_len..]` |
| 409 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[field::SRC_PORT], value)` |
| 416 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[field::DST_PORT], value)` |
| 423 | 1 | slice-index | `NetworkEndian::write_i32(&mut data[field::SEQ_NUM], value.0)` |
| 430 | 1 | slice-index | `NetworkEndian::write_i32(&mut data[field::ACK_NUM], value.0)` |
| 572 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[field::WIN_SIZE], value)` |
| 586 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[field::URGENT], value)` |
| 611 | 1 | slice-index | `&mut data[field::OPTIONS(header_len)]` |
| 619 | 1 | slice-index | `&mut data[header_len..]` |
| 694 | 1 | slice-index | `let range_left = NetworkEndian::read_u32(&data[left..mid]);` |
| 695 | 1 | slice-index | `let range_right = NetworkEndian::read_u32(&data[mid..right]);` |
| 712 | 1 | slice-index | `Ok((&buffer[length..], option))` |
| 740 | 1 | bounds-check | `buffer[0] = field::OPT_NOP;` |
| 744 | 1 | bounds-check | `buffer[1] = length as u8;` |
| 753 | 1 | bounds-check | `buffer[2] = value;` |
| 767 | 1 | slice-index | `NetworkEndian::write_u32(&mut buffer[pos..], first);` |
| 781 | 1 | copy_from_slice | `buffer[2..].copy_from_slice(provided)` |
| 786 | 1 | slice-index | `&mut buffer[length..]` |
| 1053 | 1 | slice-index | `packet.payload_mut()[..self.payload.len()].copy_from_slice(self.payload);` |

## src/wire/ipv6.rs

33 sites across 17 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| ? | 2 | bounds-check | *no DWARF line; blamed to this file only* |
| 163 | 2 | panic!/unreachable! | `assert!(mask <= 128);` |
| 178 | 1 | panic!/unreachable! | `assert!(self.x_is_unicast());` |
| 448 | 2 | slice-index | `NetworkEndian::read_u16(&data[field::LENGTH])` |
| 475 | 1 | slice-index | `Address::from_octets(data[field::SRC_ADDR].try_into().unwrap())` |
| 482 | 1 | slice-index | `Address::from_octets(data[field::DST_ADDR].try_into().unwrap())` |
| 492 | 1 | slice-index | `&data[range]` |
| 503 | 2 | bounds-check | `data[0] = (data[0] & 0x0f) \| ((value & 0x0f) << 4);` |
| 515 | 3 | bounds-check | `data[1] = (data[1] & 0x0f) \| ((value & 0x0f) << 4);` |
| 523 | 1 | bounds-check | `let raw = (((data[1] & 0xf0) as u32) << 16) \| (value & 0x0fffff);` |
| 524 | 3 | slice-index | `NetworkEndian::write_u24(&mut data[1..4], raw);` |
| 531 | 3 | slice-index | `NetworkEndian::write_u16(&mut data[field::LENGTH], value);` |
| 538 | 1 | bounds-check | `data[field::NXT_HDR] = value.into();` |
| 545 | 3 | bounds-check | `data[field::HOP_LIMIT] = value;` |
| 552 | 3 | slice-index | `data[field::SRC_ADDR].copy_from_slice(&value.octets());` |
| 559 | 3 | slice-index | `data[field::DST_ADDR].copy_from_slice(&value.octets());` |
| 567 | 1 | slice-index | `&mut data[range]` |

## src/iface/socket_set.rs

28 sites across 9 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 83 | 2 | panic!(fmt) | `ManagedSlice::Borrowed(_) => panic!("adding a socket to a full SocketSet"),` |
| 99 | 1 | bounds-check | `match self.sockets[handle.0].inner.as_ref() {` |
| 101 | 1 | expect | `T::downcast(&item.socket).expect("handle refers to a socket of a wrong type")` |
| 103 | 1 | panic!(fmt) | `None => panic!("handle does not refer to a valid socket"),` |
| 113 | 7 | bounds-check | `match self.sockets[handle.0].inner.as_mut() {` |
| 115 | 7 | expect | `.expect("handle refers to a socket of a wrong type"),` |
| 116 | 7 | panic!(fmt) | `None => panic!("handle does not refer to a valid socket"),` |
| 126 | 1 | bounds-check | `match self.sockets[handle.0].inner.take() {` |
| 128 | 1 | panic!(fmt) | `None => panic!("handle does not refer to a valid socket"),` |

## src/wire/icmpv6.rs

26 sites across 13 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| ? | 5 | slice-index | *no DWARF line; blamed to this file only* |
| 458 | 5 | slice-index | `&data[self.header_len()..]` |
| 470 | 2 | bounds-check | `data[field::TYPE] = value.into()` |
| 479 | 3 | bounds-check | `data[field::CODE] = value` |
| 502 | 2 | slice-index | `NetworkEndian::write_u32(&mut data[field::UNUSED], 0);` |
| 507 | 1 | bounds-check | `data[field::SQRV] &= 0xf;` |
| 511 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[field::RECORD_RESV], 0);` |
| 544 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[field::ECHO_IDENT], value)` |
| 554 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[field::ECHO_SEQNO], value)` |
| 600 | 2 | slice-index | `&mut data[range]` |
| 680 | 1 | slice-index | `let payload = &packet.payload()[ip_packet.header_len()..];` |
| 787 | 1 | slice-index | `let payload = &mut ip_packet.into_inner()[header.buffer_len()..];` |
| 794 | 1 | slice-index | `payload[..payload_len].copy_from_slice(&data[..payload_len]);` |

## src/wire/sixlowpan/nhc.rs

25 sites across 15 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| ? | 4 | bounds-check, slice-index | *no DWARF line; blamed to this file only* |
| 16 | 3 | bounds-check | `let raw = &data[0];` |
| 179 | 2 | bounds-check | `self.buffer.as_ref()[1 + self.next_header_size()]` |
| 208 | 2 | slice-index | `&self.buffer.as_ref()[start..][..len]` |
| 525 | 1 | slice-index | `NetworkEndian::read_u16(&data[start..start + 2])` |
| 553 | 1 | slice-index | `NetworkEndian::read_u16(&data[idx + 2..idx + 4])` |
| 567 | 1 | slice-index | `NetworkEndian::read_u16(&data[idx + 1..idx + 1 + 2])` |
| 586 | 1 | slice-index | `Some(NetworkEndian::read_u16(&data[start..start + 2]))` |
| 618 | 3 | slice-index | `&self.buffer.as_ref()[start..]` |
| 626 | 2 | slice-index | `&mut self.buffer.as_mut()[start..]` |
| 632 | 1 | bounds-check | `data[0] = (data[0] & !(0b11111 << 3)) \| (DISPATCH_UDP_HEADER << 3);` |
| 657 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[idx..idx + 2], dst_port);` |
| 665 | 1 | bounds-check | `data[idx] = (dst_port - 0xf000) as u8;` |
| 673 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[idx..idx + 2], dst_port);` |
| 682 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[idx..idx + 2], checksum);` |

## src/wire/ipv4.rs

21 sites across 12 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 101 | 1 | panic!/unreachable! | `assert!(prefix_len <= 32);` |
| 369 | 1 | slice-index | `checksum::data(&data[..self.header_len() as usize]) == !0` |
| 389 | 1 | slice-index | `&data[range]` |
| 398 | 2 | bounds-check | `data[field::VER_IHL] = (data[field::VER_IHL] & !0xf0) \| (value << 4);` |
| 411 | 2 | bounds-check | `data[field::DSCP_ECN] = (data[field::DSCP_ECN] & !0xfc) \| (value << 2)` |
| 424 | 2 | slice-index | `NetworkEndian::write_u16(&mut data[field::LENGTH], value)` |
| 431 | 2 | slice-index | `NetworkEndian::write_u16(&mut data[field::IDENT], value)` |
| 438 | 2 | slice-index | `let raw = NetworkEndian::read_u16(&data[field::FLG_OFF]);` |
| 474 | 2 | bounds-check | `data[field::TTL] = value` |
| 481 | 2 | bounds-check | `data[field::PROTOCOL] = value.into()` |
| 495 | 2 | slice-index | `data[field::SRC_ADDR].copy_from_slice(&value.octets())` |
| 502 | 2 | slice-index | `data[field::DST_ADDR].copy_from_slice(&value.octets())` |

## src/storage/ring_buffer.rs

20 sites across 9 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| ? | 1 | slice-index | *no DWARF line; blamed to this file only* |
| 110 | 4 | rem-by-zero | `(self.read_at + idx) % self.capacity()` |
| 154 | 3 | bounds-check | `let res = f(&mut self.storage[self.read_at]);` |
| 193 | 2 | slice-index | `let (size, result) = f(&mut self.storage[write_at..write_at + max_size]);` |
| 245 | 5 | slice-index | `let (size, result) = f(&mut self.storage[self.read_at..self.read_at + max_size]);` |
| 314 | 1 | slice-index | `&mut self.storage[start_at..start_at + size]` |
| 345 | 1 | panic!/unreachable! | `assert!(count <= self.window());` |
| 369 | 2 | slice-index | `&self.storage[start_at..start_at + size]` |
| 398 | 1 | panic!/unreachable! | `assert!(count <= self.len());` |

## src/wire/ieee802154.rs

18 sites across 7 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| ? | 10 | bounds-check, slice-index | *no DWARF line; blamed to this file only* |
| 371 | 2 | slice-index | `let raw = LittleEndian::read_u16(&data[field::FRAMECONTROL]);` |
| 388 | 1 | slice-index | `let raw = LittleEndian::read_u16(&data[field::FRAMECONTROL]);` |
| 406 | 1 | slice-index | `let raw = LittleEndian::read_u16(&data[field::FRAMECONTROL]);` |
| 450 | 2 | slice-index | `Some(&data[field::ADDRESSING][..offset])` |
| 543 | 1 | slice-index | `&addressing_fields[offset..][..2],` |
| 721 | 1 | slice-index | `Some(&data[index..])` |

## src/wire/mld.rs

18 sites across 11 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| ? | 8 | bounds-check, copy_from_slice, slice-index | *no DWARF line; blamed to this file only* |
| 52 | 1 | slice-index | `Ipv6Address::from_octets(data[field::QUERY_MCAST_ADDR].try_into().unwrap())` |
| 59 | 1 | bounds-check | `(data[field::SQRV] & 0x08) != 0` |
| 73 | 1 | bounds-check | `data[field::QQIC]` |
| 80 | 1 | slice-index | `NetworkEndian::read_u16(&data[field::QUERY_NUM_SRCS])` |
| 134 | 1 | panic!/unreachable! | `assert!(value < 8);` |
| 143 | 1 | bounds-check | `data[field::QQIC] = value;` |
| 150 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[field::QUERY_NUM_SRCS], value);` |
| 273 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[field::RECORD_NUM_SRCS], num_srcs);` |
| 282 | 1 | panic!/unreachable! | `assert!(addr.is_multicast());` |
| 284 | 1 | slice-index | `data[field::RECORD_MCAST_ADDR].copy_from_slice(&addr.octets());` |

## src/wire/udp.rs

18 sites across 10 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 94 | 1 | slice-index | `NetworkEndian::read_u16(&data[field::LENGTH])` |
| 101 | 1 | slice-index | `NetworkEndian::read_u16(&data[field::CHECKSUM])` |
| 145 | 1 | slice-index | `checksum::data(&data[..self.len() as usize]),` |
| 156 | 1 | slice-index | `&data[field::PAYLOAD(length)]` |
| 165 | 3 | slice-index | `NetworkEndian::write_u16(&mut data[field::SRC_PORT], value)` |
| 172 | 3 | slice-index | `NetworkEndian::write_u16(&mut data[field::DST_PORT], value)` |
| 179 | 3 | slice-index | `NetworkEndian::write_u16(&mut data[field::LENGTH], value)` |
| 186 | 2 | slice-index | `NetworkEndian::write_u16(&mut data[field::CHECKSUM], value)` |
| 200 | 1 | slice-index | `checksum::data(&data[..self.len() as usize]),` |
| 215 | 2 | slice-index | `&mut data[field::PAYLOAD(length)]` |

## src/iface/interface/sixlowpan.rs

16 sites across 14 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| ? | 2 | slice-index | *no DWARF line; blamed to this file only* |
| 81 | 1 | slice-index | `Ok(len) => &f.decompress_buf[..len],` |
| 303 | 1 | panic!/unreachable! | `Packet::Ipv4(_) => unreachable!(),` |
| 413 | 1 | slice-index | `let mut ieee_packet = Ieee802154Frame::new_unchecked(&mut tx_buf[..ieee_len]);` |
| 458 | 1 | slice-index | `&mut buffer[..iphc_repr.buffer_len()],` |
| 460 | 1 | slice-index | `buffer = &mut buffer[iphc_repr.buffer_len()..];` |
| 527 | 1 | slice-index | `&mut buffer[..udp_repr.header_len() + payload.len()],` |
| 532 | 1 | copy_from_slice | `\|buf\| buf.copy_from_slice(payload),` |
| 549 | 1 | panic!/unreachable! | `_ => unreachable!(),` |
| 720 | 1 | slice-index | `&data[ext_repr.length as usize + ext_repr.buffer_len()..],` |
| 732 | 1 | slice-index | `&mut buffer[..ipv6_ext_hdr.header_len()],` |
| 734 | 1 | slice-index | `buffer[ipv6_ext_hdr.header_len()..][..ipv6_ext_hdr.data.len()]` |
| 771 | 1 | slice-index | `let mut udp = UdpPacket::new_unchecked(&mut buffer[..payload.len() + 8]);` |
| 773 | 2 | slice-index | `buffer[8..][..payload.len()].copy_from_slice(payload);` |

## src/wire/ndisc.rs

16 sites across 14 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| ? | 2 | slice-index | *no DWARF line; blamed to this file only* |
| 59 | 1 | slice-index | `Duration::from_millis(NetworkEndian::read_u32(&data[field::REACHABLE_TM]) as u64)` |
| 66 | 1 | slice-index | `Duration::from_millis(NetworkEndian::read_u32(&data[field::RETRANS_TM]) as u64)` |
| 81 | 1 | slice-index | `Ipv6Address::from_octets(data[field::TARGET_ADDR].try_into().unwrap())` |
| 107 | 1 | slice-index | `Ipv6Address::from_octets(data[field::DEST_ADDR].try_into().unwrap())` |
| 120 | 1 | bounds-check | `data[field::CUR_HOP_LIMIT] = value;` |
| 126 | 1 | bounds-check | `self.buffer.as_mut()[field::ROUTER_FLAGS] = flags.bits();` |
| 133 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[field::ROUTER_LT], value.secs() as u16);` |
| 140 | 1 | slice-index | `NetworkEndian::write_u32(&mut data[field::REACHABLE_TM], value.total_millis() as u32);` |
| 147 | 1 | slice-index | `NetworkEndian::write_u32(&mut data[field::RETRANS_TM], value.total_millis() as u32);` |
| 162 | 2 | slice-index | `data[field::TARGET_ADDR].copy_from_slice(&value.octets());` |
| 187 | 1 | slice-index | `data[field::DEST_ADDR].copy_from_slice(&value.octets());` |
| 240 | 1 | slice-index | `let pkt = NdiscOption::new_checked(&packet.payload()[offset..])?;` |
| 451 | 1 | slice-index | `NdiscOption::new_unchecked(&mut packet.payload_mut()[offset..]);` |

## src/wire/ndiscoption.rs

13 sites across 11 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 289 | 1 | bounds-check | `data[field::TYPE] = value.into();` |
| 296 | 2 | bounds-check | `data[field::LENGTH] = value;` |
| 306 | 1 | slice-index | `data[2..2 + addr.len()].copy_from_slice(addr.as_bytes())` |
| 316 | 1 | slice-index | `NetworkEndian::write_u32(&mut data[field::MTU], value);` |
| 352 | 1 | slice-index | `NetworkEndian::write_u32(&mut data[field::PREF_RESERVED], 0);` |
| 359 | 1 | slice-index | `data[field::PREFIX].copy_from_slice(&addr.octets());` |
| 369 | 1 | slice-index | `data[field::REDIRECTED_RESERVED].fill_with(\|\| 0);` |
| 379 | 2 | slice-index | `&mut data[field::DATA(len)]` |
| 488 | 1 | slice-index | `data: &redirected_packet[ip_repr.buffer_len()..][..ip_repr.payload_len],` |
| 574 | 1 | copy_from_slice | `ip_packet.payload_mut().copy_from_slice(data);` |
| 588 | 1 | copy_from_slice | `opt.data_mut().copy_from_slice(data);` |

## src/iface/packet.rs

12 sites across 9 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 90 | 1 | panic!/unreachable! | `IpRepr::Ipv4(_) => unreachable!(),` |
| 105 | 1 | panic!/unreachable! | `IpRepr::Ipv4(_) => unreachable!(),` |
| 115 | 1 | slice-index | `&mut payload[..ipv6_ext_hdr.header_len()],` |
| 121 | 1 | slice-index | `&mut payload[hbh_start..hbh_end],` |
| 143 | 1 | copy_from_slice | `\|buf\| buf.copy_from_slice(inner_payload),` |
| 179 | 1 | unwrap | `\|buf\| dhcp_repr.emit(&mut DhcpPacket::new_unchecked(buf)).unwrap(),` |
| 234 | 2 | panic!/unreachable! | `Self::Icmpv4(_) => unreachable!(),` |
| 236 | 2 | panic!/unreachable! | `Self::Dhcpv4(..) => unreachable!(),` |
| 240 | 2 | panic!/unreachable! | `Self::HopByHopIcmpv6(_, _) => unreachable!(),` |

## src/wire/sixlowpan/mod.rs

10 sites across 6 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| ? | 5 | bounds-check, slice-index | *no DWARF line; blamed to this file only* |
| 86 | 1 | unwrap | `Ok(ipv6::Address::from_octets(addr.try_into().unwrap()))` |
| 90 | 1 | copy_from_slice | `bytes[8..].copy_from_slice(inline);` |
| 96 | 1 | copy_from_slice | `bytes[14..].copy_from_slice(inline);` |
| 118 | 1 | slice-index | `bytes[11..].copy_from_slice(&inline[1..][..5]);` |
| 124 | 1 | slice-index | `bytes[13..].copy_from_slice(&inline[1..][..3]);` |

## src/wire/arp.rs

9 sites across 9 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 176 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[field::HTYPE], value.into())` |
| 183 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[field::PTYPE], value.into())` |
| 190 | 1 | bounds-check | `data[field::HLEN] = value` |
| 197 | 1 | bounds-check | `data[field::PLEN] = value` |
| 204 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[field::OPER], value.into())` |
| 214 | 1 | slice-index | `data[field::SHA(hardware_len, protocol_len)].copy_from_slice(value)` |
| 224 | 1 | slice-index | `data[field::SPA(hardware_len, protocol_len)].copy_from_slice(value)` |
| 234 | 1 | slice-index | `data[field::THA(hardware_len, protocol_len)].copy_from_slice(value)` |
| 244 | 1 | slice-index | `data[field::TPA(hardware_len, protocol_len)].copy_from_slice(value)` |

## src/socket/tcp.rs

8 sites across 5 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| ? | 4 | panic!(fmt) | *no DWARF line; blamed to this file only* |
| 592 | 1 | panic!(fmt) | `panic!("receiving buffer too large, cannot exceed 1 GiB")` |
| 1641 | 1 | panic!/unreachable! | `(State::Listen, _, Some(_)) => unreachable!(),` |
| 1799 | 1 | slice-index | `&repr.payload[overlap_start - segment_start..overlap_end - segment_start],` |
| 2323 | 1 | unwrap | `let ip_header_len = match self.tuple.unwrap().local.addr {` |

## src/wire/icmpv4.rs

8 sites across 7 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| ? | 2 | slice-index | *no DWARF line; blamed to this file only* |
| 308 | 1 | bounds-check | `data[field::CODE] = value` |
| 325 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[field::ECHO_IDENT], value)` |
| 335 | 1 | slice-index | `NetworkEndian::write_u16(&mut data[field::ECHO_SEQNO], value)` |
| 355 | 1 | slice-index | `&mut data[range]` |
| 530 | 1 | copy_from_slice | `payload.copy_from_slice(data)` |
| 544 | 1 | copy_from_slice | `payload.copy_from_slice(data)` |

## src/iface/interface/mod.rs

7 sites across 7 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 212 | 1 | assert! | `assert_eq!(` |
| 814 | 1 | expect | `neighbor_addr.expect("non-IP response packet"),` |
| 920 | 1 | panic!(fmt) | `panic!("IP address {} is not unicast", cidr.address())` |
| 1122 | 1 | panic!/unreachable! | `Medium::Ieee802154 => unreachable!(),` |
| 1245 | 1 | panic!/unreachable! | `assert!(!ip_repr.dst_addr().is_unspecified());` |
| 1281 | 1 | panic!/unreachable! | `(_, _) => unreachable!(),` |
| 1308 | 1 | slice-index | `let payload = &mut tx_buffer[repr.header_len()..];` |

## src/wire/ethernet.rs

7 sites across 3 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 76 | 1 | copy_from_slice | `bytes.copy_from_slice(data);` |
| 287 | 3 | slice-index | `data[field::SOURCE].copy_from_slice(value.as_bytes())` |
| 294 | 3 | slice-index | `NetworkEndian::write_u16(&mut data[field::ETHERTYPE], value.into())` |

## src/wire/ipv6option.rs

7 sites across 4 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 229 | 1 | bounds-check | `data[field::TYPE] = value.into();` |
| 239 | 2 | bounds-check | `data[field::LENGTH] = value;` |
| 252 | 3 | slice-index | `&mut data[field::DATA(len)]` |
| 366 | 1 | slice-index | `opt.data_mut().copy_from_slice(&data[..length as usize]);` |

## src/storage/packet_buffer.rs

5 sites across 5 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| ? | 1 | slice-index | *no DWARF line; blamed to this file only* |
| 195 | 1 | unwrap | `metadata.header.as_mut().unwrap(),` |
| 196 | 1 | slice-index | `&mut payload_buf[..metadata.size],` |
| 215 | 1 | unwrap | `Ok((meta.header.take().unwrap(), payload_buf))` |
| 227 | 1 | unwrap | `metadata.header.as_ref().unwrap(),` |

## src/iface/neighbor.rs

4 sites across 3 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 131 | 1 | unwrap | `let _old_neighbor = self.storage.remove(&old_protocol_addr).unwrap();` |
| 143 | 1 | panic!/unreachable! | `_ => unreachable!(),` |
| 150 | 2 | panic!/unreachable! | `assert!(protocol_addr.is_unicast());` |

## src/wire/dhcpv4.rs

4 sites across 4 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 428 | 1 | slice-index | `for byte in &mut data[field::SNAME] {` |
| 431 | 1 | slice-index | `for byte in &mut data[field::FILE] {` |
| 495 | 1 | slice-index | `let field = &mut self.buffer.as_mut()[field::MAGIC_NUMBER];` |
| 935 | 1 | slice-index | `servers[(i * IP_SIZE)..((i + 1) * IP_SIZE)].copy_from_slice(&ip.octets());` |

## src/wire/ip.rs

4 sites across 1 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 992 | 4 | panic!/unreachable! | `_ => unreachable!(),` |

## src/wire/mod.rs

4 sites across 3 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 441 | 2 | panic!(fmt) | `_ => panic!("HardwareAddress is not Ethernet."),` |
| 450 | 1 | panic!(fmt) | `_ => panic!("HardwareAddress is not Ethernet."),` |
| 549 | 1 | slice-index | `&self.data[..self.len as usize]` |

## src/iface/interface/ipv6.rs

3 sites across 3 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 31 | 1 | panic!/unreachable! | `assert!(!dst_addr.is_unspecified());` |
| 98 | 1 | unwrap | `.unwrap(); // NOTE: we check above that there is at least one IPv6 address.` |
| 317 | 1 | slice-index | `&ip_payload[ext_repr.header_len() + ext_repr.data.len()..],` |

## src/socket/dhcpv4.rs

3 sites across 3 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 315 | 1 | panic!/unreachable! | `assert!(repr.src_port == self.server_port && repr.dst_port == self.client_port);` |
| 333 | 1 | panic!(fmt) | `panic!("using DHCPv4 socket with a non-ethernet hardware address.");` |
| 570 | 1 | panic!(fmt) | `panic!("using DHCPv4 socket with a non-ethernet hardware address.");` |

## src/iface/route.rs

2 sites across 2 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 173 | 1 | panic!/unreachable! | `assert!(addr.is_unicast());` |
| 187 | 1 | panic!/unreachable! | `.max_by_key(\|route\| route.cidr.prefix_len())` |

## src/wire/ipv6ext_header.rs

2 sites across 2 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 102 | 1 | bounds-check | `data[field::NXT_HDR] = value.into();` |
| 110 | 1 | bounds-check | `data[field::LENGTH] = value;` |

## src/wire/ipv6hbh.rs

2 sites across 2 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 104 | 1 | slice-index | `&mut buffer[..opt.buffer_len()],` |
| 106 | 1 | slice-index | `buffer = &mut buffer[opt.buffer_len()..];` |

## src/phy/mod.rs

1 sites across 1 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 67 | 1 | panic!(fmt) | `medium => panic!(` |

## src/socket/udp.rs

1 sites across 1 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 643 | 1 | copy_from_slice | `Ok(buf) => buf.copy_from_slice(payload),` |

## src/storage/assembler.rs

1 sites across 1 lines.

| line | sites | kind | source |
| --- | --- | --- | --- |
| 233 | 1 | bounds-check | `self.contigs[i + 1].shrink_hole_by(offset + size);` |
