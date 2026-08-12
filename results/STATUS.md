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
| [`src/wire/ipv6.rs`](#srcwireipv6rs) | 34 | 23 | 4 | 6 | 0 | 1 | -416 | andrew |
| [`src/wire/icmpv6.rs`](#srcwireicmpv6rs) | 29 | 20 | 0 | 3 | 0 | 6 | -180 | andrew |
| [`src/wire/ipv4.rs`](#srcwireipv4rs) | 21 | 20 | 1 | 0 | 0 | 0 | -212 | agent |
| [`src/wire/udp.rs`](#srcwireudprs) | 18 | 18 | 0 | 0 | 0 | 0 | -628 | agent |
| [`src/wire/sixlowpan/iphc.rs`](#srcwiresixlowpaniphcrs) | 49 | 13 | 6 | 0 | 0 | 30 | -- |  |
| [`src/wire/ndisc.rs`](#srcwirendiscrs) | 16 | 12 | 0 | 2 | 0 | 2 | -204 | andrew |
| [`src/wire/sixlowpan/nhc.rs`](#srcwiresixlowpannhcrs) | 25 | 12 | 3 | 0 | 0 | 10 | -220 | agent |
| [`src/wire/arp.rs`](#srcwirearprs) | 9 | 9 | 0 | 0 | 0 | 0 | 84 | blocked: const fn new_unchecked |
| [`src/wire/ndiscoption.rs`](#srcwirendiscoptionrs) | 13 | 9 | 0 | 4 | 0 | 0 | -128 | agent |
| [`src/wire/tcp.rs`](#srcwiretcprs) | 38 | 8 | 24 | 6 | 0 | 0 | -- |  |
| [`src/wire/ethernet.rs`](#srcwireethernetrs) | 7 | 7 | 0 | 0 | 0 | 0 | -- |  |
| [`src/wire/ipv6option.rs`](#srcwireipv6optionrs) | 7 | 6 | 0 | 1 | 0 | 0 | -- |  |
| [`src/wire/mld.rs`](#srcwiremldrs) | 15 | 6 | 3 | 1 | 0 | 5 | -- |  |
| [`src/storage/ring_buffer.rs`](#srcstorageringbufferrs) | 21 | 4 | 2 | 4 | 11 | 0 | -- |  |
| [`src/wire/icmpv4.rs`](#srcwireicmpv4rs) | 8 | 4 | 0 | 2 | 0 | 2 | -- |  |
| [`src/iface/interface/sixlowpan.rs`](#srcifaceinterfacesixlowpanrs) | 16 | 3 | 7 | 4 | 0 | 2 | -- |  |
| [`src/wire/ieee802154.rs`](#srcwireieee802154rs) | 34 | 3 | 0 | 6 | 0 | 25 | -- |  |
| [`src/wire/ipv6ext_header.rs`](#srcwireipv6extheaderrs) | 2 | 2 | 0 | 0 | 0 | 0 | -- |  |
| [`src/wire/dhcpv4.rs`](#srcwiredhcpv4rs) | 4 | 1 | 0 | 3 | 0 | 0 | -- |  |
| [`src/iface/interface/ipv6.rs`](#srcifaceinterfaceipv6rs) | 3 | 0 | 2 | 1 | 0 | 0 | -- |  |
| [`src/iface/interface/mod.rs`](#srcifaceinterfacemodrs) | 7 | 0 | 0 | 0 | 7 | 0 | -- |  |
| [`src/iface/neighbor.rs`](#srcifaceneighborrs) | 4 | 0 | 4 | 0 | 0 | 0 | -- |  |
| [`src/iface/packet.rs`](#srcifacepacketrs) | 11 | 0 | 11 | 0 | 0 | 0 | -- |  |
| [`src/iface/route.rs`](#srcifacerouters) | 1 | 0 | 1 | 0 | 0 | 0 | -- |  |
| [`src/iface/socket_set.rs`](#srcifacesocketsetrs) | 28 | 0 | 28 | 0 | 0 | 0 | -- |  |
| [`src/phy/mod.rs`](#srcphymodrs) | 1 | 0 | 1 | 0 | 0 | 0 | -- |  |
| [`src/socket/dhcpv4.rs`](#srcsocketdhcpv4rs) | 3 | 0 | 3 | 0 | 0 | 0 | -- |  |
| [`src/socket/tcp.rs`](#srcsockettcprs) | 4 | 0 | 1 | 1 | 0 | 2 | -- |  |
| [`src/socket/udp.rs`](#srcsocketudprs) | 1 | 0 | 1 | 0 | 0 | 0 | -- |  |
| [`src/storage/assembler.rs`](#srcstorageassemblerrs) | 1 | 0 | 0 | 1 | 0 | 0 | -- |  |
| [`src/storage/packet_buffer.rs`](#srcstoragepacketbufferrs) | 4 | 0 | 1 | 1 | 2 | 0 | -- |  |
| [`src/wire/ip.rs`](#srcwireiprs) | 4 | 0 | 4 | 0 | 0 | 0 | -- |  |
| [`src/wire/ipv6hbh.rs`](#srcwireipv6hbhrs) | 2 | 0 | 0 | 2 | 0 | 0 | -- |  |
| [`src/wire/mod.rs`](#srcwiremodrs) | 4 | 0 | 3 | 1 | 0 | 0 | -- |  |
| [`src/wire/sixlowpan/mod.rs`](#srcwiresixlowpanmodrs) | 9 | 0 | 0 | 4 | 0 | 5 | -- |  |
| **total** | **453** | **180** | **110** | **53** | **20** | **90** | | |

`other` is mostly UNATTRIBUTED: a site the blame data puts in this file but that falls outside any function the triage parser recognised -- macro bodies, derives, closures. Those sites are real and counted in the metric; they just have no Flux obligation attached yet.

## Every panic site, by file

One row per source line. `sites` exceeds lines because generics and inlining duplicate a line into several machine call sites -- lines track effort, sites track the metric. A `?` line means DWARF blamed the file but no statement.

<a id="srcwireipv6rs"></a>
### `src/wire/ipv6.rs`

34 sites across 17 lines. churn 23, panic 4, core 6. Owner: andrew.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 163 | 3 | panic!/unreachable! | PANIC | `mask` | `assert!(mask <= 128);` |
| 178 | 1 | panic!/unreachable! | PANIC | `solicited_node` | `assert!(self.x_is_unicast());` |
| 448 | 2 | slice-index | CHURN | `payload_len` | `pub fn payload_len(&self) -> u16 {` |
| 475 | 1 | slice-index | CORE | `src_addr` | `pub fn src_addr(&self) -> Address {` |
| 482 | 1 | slice-index | CORE | `dst_addr` | `pub fn dst_addr(&self) -> Address {` |
| 492 | 1 | slice-index | CHURN | `payload` | `let data = self.buffer.as_ref();` |
| 503 | 3 | bounds-check | CHURN | `set_version` | `// Make sure to retain the lower order bits which contain` |
| 512 | 1 | bounds-check | UNATTRIBUTED | `` | `// Put the higher order 4-bits of value in the lower order` |
| 515 | 3 | bounds-check | CHURN | `set_traffic_class` | `// Put the lower order 4-bits of value in the higher order` |
| 523 | 1 | bounds-check | CORE | `set_flow_label` | `let data = self.buffer.as_mut();` |
| 524 | 3 | slice-index | CORE | `set_flow_label` | `// Retain the lower order 4-bits of the traffic class` |
| 531 | 3 | slice-index | CHURN | `set_payload_len` | `pub fn set_payload_len(&mut self, value: u16) {` |
| 538 | 1 | bounds-check | CHURN | `set_next_header` | `pub fn set_next_header(&mut self, value: Protocol) {` |
| 545 | 3 | bounds-check | CHURN | `set_hop_limit` | `pub fn set_hop_limit(&mut self, value: u8) {` |
| 552 | 3 | slice-index | CHURN | `set_src_addr` | `pub fn set_src_addr(&mut self, value: Address) {` |
| 559 | 3 | slice-index | CHURN | `set_dst_addr` | `pub fn set_dst_addr(&mut self, value: Address) {` |
| 567 | 1 | slice-index | CHURN | `payload_mut` | `let range = self.header_len()..self.total_len();` |

<a id="srcwireicmpv6rs"></a>
### `src/wire/icmpv6.rs`

29 sites across 18 lines. churn 20, panic 0, core 3. Owner: andrew.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 458 | 5 | slice-index | CHURN | `payload` | `let data = self.buffer.as_ref();` |
| 470 | 3 | bounds-check | CHURN | `set_msg_type` | `self.ty = value;` |
| 479 | 4 | bounds-check | CHURN | `set_msg_code` | `pub fn set_msg_code(&mut self, value: u8) {` |
| 502 | 2 | slice-index | CHURN | `clear_reserved` | `\| Message::Redirect => {` |
| 506 | 1 | slice-index | UNATTRIBUTED | `` | `Message::MldQuery => {` |
| 507 | 1 | bounds-check | CHURN | `clear_reserved` | `let data = self.buffer.as_mut();` |
| 511 | 1 | slice-index | CHURN | `clear_reserved` | `Message::MldReport => {` |
| 534 | 1 | slice-index | UNATTRIBUTED | `` | `pub fn set_checksum(&mut self, value: u16) {` |
| 544 | 1 | slice-index | CHURN | `set_echo_ident` | `pub fn set_echo_ident(&mut self, value: u16) {` |
| 554 | 1 | slice-index | CHURN | `set_echo_seq_no` | `pub fn set_echo_seq_no(&mut self, value: u16) {` |
| 564 | 1 | slice-index | UNATTRIBUTED | `` | `pub fn set_pkt_too_big_mtu(&mut self, value: u32) {` |
| 574 | 1 | slice-index | UNATTRIBUTED | `` | `pub fn set_param_problem_ptr(&mut self, value: u32) {` |
| 600 | 2 | slice-index | CHURN | `payload_mut` | `let range = self.header_len()..;` |
| 680 | 1 | slice-index | CORE | `parse` | `Ipv6Packet::new_unchecked(packet.payload())` |
| 787 | 1 | slice-index | CORE | `emit` | `T: AsRef<[u8]> + AsMut<[u8]> + ?Sized,` |
| 794 | 1 | slice-index | CORE | `emit` | `// much space we have for the packet due to IPv6 options and etc` |
| 851 | 1 | slice-index | UNATTRIBUTED | `` | `packet.set_msg_type(Message::EchoRequest);` |
| 864 | 1 | slice-index | UNATTRIBUTED | `` | `packet.set_msg_type(Message::EchoReply);` |

<a id="srcwireipv4rs"></a>
### `src/wire/ipv4.rs`

21 sites across 12 lines. churn 20, panic 1, core 0. Owner: agent.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 101 | 1 | panic!/unreachable! | PANIC | `new` | `assert!(prefix_len <= 32);` |
| 369 | 1 | slice-index | CHURN | `verify_checksum` | `` |
| 389 | 1 | slice-index | CHURN | `payload` | `let range = self.header_len() as usize..self.total_len() as usize;` |
| 398 | 2 | bounds-check | CHURN | `set_version` | `pub fn set_version(&mut self, value: u8) {` |
| 411 | 2 | bounds-check | CHURN | `set_dscp` | `pub fn set_dscp(&mut self, value: u8) {` |
| 424 | 2 | slice-index | CHURN | `set_total_len` | `pub fn set_total_len(&mut self, value: u16) {` |
| 431 | 2 | slice-index | CHURN | `set_ident` | `pub fn set_ident(&mut self, value: u16) {` |
| 438 | 2 | slice-index | CHURN | `clear_flags` | `pub fn clear_flags(&mut self) {` |
| 474 | 2 | bounds-check | CHURN | `set_hop_limit` | `pub fn set_hop_limit(&mut self, value: u8) {` |
| 481 | 2 | bounds-check | CHURN | `set_next_header` | `pub fn set_next_header(&mut self, value: Protocol) {` |
| 495 | 2 | slice-index | CHURN | `set_src_addr` | `pub fn set_src_addr(&mut self, value: Address) {` |
| 502 | 2 | slice-index | CHURN | `set_dst_addr` | `pub fn set_dst_addr(&mut self, value: Address) {` |

<a id="srcwireudprs"></a>
### `src/wire/udp.rs`

18 sites across 10 lines. churn 18, panic 0, core 0. Owner: agent.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 94 | 1 | slice-index | CHURN | `len` | `pub fn len(&self) -> u16 {` |
| 101 | 1 | slice-index | CHURN | `checksum` | `pub fn checksum(&self) -> u16 {` |
| 145 | 1 | slice-index | CHURN | `verify_checksum` | `checksum::combine(&[` |
| 156 | 1 | slice-index | CHURN | `payload` | `let length = self.len();` |
| 165 | 3 | slice-index | CHURN | `set_src_port` | `pub fn set_src_port(&mut self, value: u16) {` |
| 172 | 3 | slice-index | CHURN | `set_dst_port` | `pub fn set_dst_port(&mut self, value: u16) {` |
| 179 | 3 | slice-index | CHURN | `set_len` | `pub fn set_len(&mut self, value: u16) {` |
| 186 | 2 | slice-index | CHURN | `set_checksum` | `pub fn set_checksum(&mut self, value: u16) {` |
| 200 | 1 | slice-index | CHURN | `fill_checksum` | `!checksum::combine(&[` |
| 215 | 2 | slice-index | CHURN | `payload_mut` | `let length = self.len();` |

<a id="srcwiresixlowpaniphcrs"></a>
### `src/wire/sixlowpan/iphc.rs`

49 sites across 28 lines. churn 13, panic 6, core 0. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 133 | 1 | slice-index | CHURN | `next_header` | `let nh = data[start..start + 1][0];` |
| 147 | 1 | slice-index | PANIC | `hop_limit` | `data[start..start + 1][0]` |
| 160 | 1 | bounds-check | UNATTRIBUTED | `` | `Some(data[2] >> 4)` |
| 170 | 1 | bounds-check | UNATTRIBUTED | `` | `Some(data[2] & 0x0f)` |
| 181 | 2 | bounds-check, slice-index | UNATTRIBUTED | `` | `Some(self.buffer.as_ref()[start..][0] & 0b1100_0000)` |
| 193 | 2 | bounds-check, slice-index | UNATTRIBUTED | `` | `Some(self.buffer.as_ref()[start..][0] & 0b111111)` |
| 206 | 2 | slice-index | PANIC | `flow_label_field` | `&self.buffer.as_ref()[start..][2..4],` |
| 212 | 2 | slice-index | PANIC | `flow_label_field` | `&self.buffer.as_ref()[start..][1..3],` |
| 230 | 2 | slice-index | UNATTRIBUTED | `` | `&data[start..][..16],` |
| 233 | 2 | slice-index | UNATTRIBUTED | `` | `AddressMode::InLine64bits(&data[start..][..8]),` |
| 236 | 2 | slice-index | UNATTRIBUTED | `` | `AddressMode::InLine16bits(&data[start..][..2]),` |
| 247 | 2 | slice-index | UNATTRIBUTED | `` | `AddressMode::InLine64bits(&data[start..][..8]),` |
| 257 | 2 | slice-index | UNATTRIBUTED | `` | `AddressMode::InLine16bits(&data[start..][..2]),` |
| 288 | 2 | slice-index | UNATTRIBUTED | `` | `&data[start..][..16],` |
| 291 | 2 | slice-index | UNATTRIBUTED | `` | `AddressMode::InLine64bits(&data[start..][..8]),` |
| 294 | 2 | slice-index | UNATTRIBUTED | `` | `AddressMode::InLine16bits(&data[start..][..2]),` |
| 302 | 2 | slice-index | UNATTRIBUTED | `` | `AddressMode::InLine64bits(&data[start..][..8]),` |
| 312 | 2 | slice-index | UNATTRIBUTED | `` | `AddressMode::InLine16bits(&data[start..][..2]),` |
| 329 | 2 | slice-index | UNATTRIBUTED | `` | `&data[start..][..16],` |
| 332 | 2 | slice-index | CHURN | `dst_addr` | `AddressMode::Multicast48bits(&data[start..][..6]),` |
| 335 | 2 | slice-index | CHURN | `dst_addr` | `AddressMode::Multicast32bits(&data[start..][..4]),` |
| 338 | 2 | slice-index | CHURN | `dst_addr` | `AddressMode::Multicast8bits(&data[start..][..1]),` |
| 349 | 1 | slice-index | UNATTRIBUTED | `` | `get_field!(dispatch_field, 0b111, 13);` |
| 353 | 1 | slice-index | UNATTRIBUTED | `` | `get_field!(cid_field, 0b1, 7);` |
| 455 | 1 | slice-index | CHURN | `payload` | `&data[len..]` |
| 462 | 1 | slice-index | CHURN | `set_dispatch_field` | `let data = &mut self.buffer.as_mut()[field::IPHC_FIELD];` |
| 481 | 4 | slice-index | CHURN | `set_field` | `raw[idx..idx + value.len()].copy_from_slice(value);` |
| 845 | 1 | panic!/unreachable! | PANIC | `buffer_len` | `_ => unreachable!(),` |

<a id="srcwirendiscrs"></a>
### `src/wire/ndisc.rs`

16 sites across 15 lines. churn 12, panic 0, core 2. Owner: andrew.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
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
| 389 | 1 | slice-index | UNATTRIBUTED | `` | `NdiscOption::new_unchecked(&mut packet.payload_mut()[offset..]);` |
| 395 | 1 | slice-index | UNATTRIBUTED | `` | `NdiscOption::new_unchecked(&mut packet.payload_mut()[offset..]);` |
| 451 | 1 | slice-index | CHURN | `emit` | `NdiscOption::new_unchecked(&mut packet.payload_mut()[offset..]);` |

<a id="srcwiresixlowpannhcrs"></a>
### `src/wire/sixlowpan/nhc.rs`

25 sites across 20 lines. churn 12, panic 3, core 0. Owner: agent.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 160 | 1 | bounds-check | UNATTRIBUTED | `` | `get_field!(eid_field, 0b111, 1);` |
| 161 | 1 | bounds-check | UNATTRIBUTED | `` | `get_field!(nh_field, 0b1, 0);` |
| 179 | 2 | bounds-check | CHURN | `length` | `self.buffer.as_ref()[1 + self.next_header_size()]` |
| 208 | 2 | slice-index | CHURN | `payload` | `&self.buffer.as_ref()[start..][..len]` |
| 510 | 1 | bounds-check | UNATTRIBUTED | `` | `get_field!(ports_field, 0b11, 0);` |
| 525 | 1 | slice-index | PANIC | `src_port` | `NetworkEndian::read_u16(&data[start..start + 2])` |
| 553 | 1 | slice-index | PANIC | `dst_port` | `NetworkEndian::read_u16(&data[idx + 2..idx + 4])` |
| 567 | 1 | slice-index | PANIC | `dst_port` | `NetworkEndian::read_u16(&data[idx + 1..idx + 1 + 2])` |
| 586 | 1 | slice-index | CHURN | `checksum` | `Some(NetworkEndian::read_u16(&data[start..start + 2]))` |
| 618 | 3 | slice-index | CHURN | `payload` | `&self.buffer.as_ref()[start..]` |
| 626 | 2 | slice-index | CHURN | `payload_mut` | `&mut self.buffer.as_mut()[start..]` |
| 632 | 1 | bounds-check | CHURN | `set_dispatch_field` | `data[0] = (data[0] & !(0b11111 << 3)) \| (DISPATCH_UDP_HEADER << 3);` |
| 648 | 1 | bounds-check | UNATTRIBUTED | `` | `data[idx] = (((src_port - 0xf0b0) as u8) << 4) & ((dst_port - 0xf0b0) as u8);` |
| 654 | 1 | bounds-check | UNATTRIBUTED | `` | `data[idx] = (src_port - 0xf000) as u8;` |
| 657 | 1 | slice-index | CLEAN | `set_ports` | `NetworkEndian::write_u16(&mut data[idx..idx + 2], dst_port);` |
| 663 | 1 | slice-index | UNATTRIBUTED | `` | `NetworkEndian::write_u16(&mut data[idx..idx + 2], src_port);` |
| 665 | 1 | bounds-check | CLEAN | `set_ports` | `data[idx] = (dst_port - 0xf000) as u8;` |
| 671 | 1 | slice-index | UNATTRIBUTED | `` | `NetworkEndian::write_u16(&mut data[idx..idx + 2], src_port);` |
| 673 | 1 | slice-index | CLEAN | `set_ports` | `NetworkEndian::write_u16(&mut data[idx..idx + 2], dst_port);` |
| 682 | 1 | slice-index | CHURN | `set_checksum` | `NetworkEndian::write_u16(&mut data[idx..idx + 2], checksum);` |

<a id="srcwirearprs"></a>
### `src/wire/arp.rs`

9 sites across 9 lines. churn 9, panic 0, core 0. Owner: blocked: const fn new_unchecked.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 176 | 1 | slice-index | CHURN | `set_hardware_type` | `pub fn set_hardware_type(&mut self, value: Hardware) {` |
| 183 | 1 | slice-index | CHURN | `set_protocol_type` | `pub fn set_protocol_type(&mut self, value: Protocol) {` |
| 190 | 1 | bounds-check | CHURN | `set_hardware_len` | `pub fn set_hardware_len(&mut self, value: u8) {` |
| 197 | 1 | bounds-check | CHURN | `set_protocol_len` | `pub fn set_protocol_len(&mut self, value: u8) {` |
| 204 | 1 | slice-index | CHURN | `set_operation` | `pub fn set_operation(&mut self, value: Operation) {` |
| 214 | 1 | slice-index | CHURN | `set_source_hardware_addr` | `let (hardware_len, protocol_len) = (self.hardware_len(), self.protocol_len());` |
| 224 | 1 | slice-index | CHURN | `set_source_protocol_addr` | `let (hardware_len, protocol_len) = (self.hardware_len(), self.protocol_len());` |
| 234 | 1 | slice-index | CHURN | `set_target_hardware_addr` | `let (hardware_len, protocol_len) = (self.hardware_len(), self.protocol_len());` |
| 244 | 1 | slice-index | CHURN | `set_target_protocol_addr` | `let (hardware_len, protocol_len) = (self.hardware_len(), self.protocol_len());` |

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

<a id="srcwiretcprs"></a>
### `src/wire/tcp.rs`

38 sites across 23 lines. churn 8, panic 24, core 6. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 44 | 10 | panic!(fmt) | PANIC | `add` | `panic!("attempt to add to sequence number with unsigned overflow")` |
| 55 | 1 | panic!(fmt) | PANIC | `sub` | `panic!("attempt to subtract to sequence number with unsigned overflow")` |
| 73 | 7 | panic!(fmt) | PANIC | `sub` | `panic!("attempt to subtract sequence numbers with underflow")` |
| 392 | 1 | slice-index | CHURN | `options` | `let header_len = self.header_len();` |
| 400 | 1 | slice-index | CHURN | `payload` | `let header_len = self.header_len() as usize;` |
| 409 | 1 | slice-index | CHURN | `set_src_port` | `pub fn set_src_port(&mut self, value: u16) {` |
| 416 | 1 | slice-index | CHURN | `set_dst_port` | `pub fn set_dst_port(&mut self, value: u16) {` |
| 423 | 1 | slice-index | CORE | `set_seq_number` | `pub fn set_seq_number(&mut self, value: SeqNumber) {` |
| 430 | 1 | slice-index | CORE | `set_ack_number` | `pub fn set_ack_number(&mut self, value: SeqNumber) {` |
| 572 | 1 | slice-index | CHURN | `set_window_len` | `pub fn set_window_len(&mut self, value: u16) {` |
| 586 | 1 | slice-index | CHURN | `set_urgent_at` | `pub fn set_urgent_at(&mut self, value: u16) {` |
| 611 | 1 | slice-index | CHURN | `options_mut` | `let header_len = self.header_len();` |
| 619 | 1 | slice-index | CHURN | `payload_mut` | `let header_len = self.header_len() as usize;` |
| 694 | 1 | slice-index | CORE | `parse` | `sack_ranges.iter_mut().enumerate().for_each(\|(i, nmut)\| {` |
| 695 | 1 | slice-index | CORE | `parse` | `let left = i * 8;` |
| 712 | 1 | slice-index | CORE | `parse` | `}` |
| 740 | 1 | bounds-check | PANIC | `emit` | `*p = field::OPT_END;` |
| 744 | 1 | bounds-check | PANIC | `emit` | `length = 1;` |
| 753 | 1 | bounds-check | PANIC | `emit` | `buffer[0] = field::OPT_MSS;` |
| 767 | 1 | slice-index | PANIC | `emit` | `.filter(\|s\| s.is_some())` |
| 781 | 1 | copy_from_slice | PANIC | `emit` | `&TcpOption::Unknown {` |
| 786 | 1 | slice-index | PANIC | `emit` | `buffer[2..].copy_from_slice(provided)` |
| 1053 | 1 | slice-index | CORE | `emit` | `if !options.is_empty() {` |

<a id="srcwireethernetrs"></a>
### `src/wire/ethernet.rs`

7 sites across 3 lines. churn 7, panic 0, core 0. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 76 | 1 | copy_from_slice | CHURN | `from_bytes` | `bytes.copy_from_slice(data);` |
| 287 | 3 | slice-index | CHURN | `set_src_addr` | `pub fn set_src_addr(&mut self, value: Address) {` |
| 294 | 3 | slice-index | CHURN | `set_ethertype` | `pub fn set_ethertype(&mut self, value: EtherType) {` |

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

15 sites across 15 lines. churn 6, panic 3, core 1. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 52 | 1 | slice-index | CORE | `mcast_addr` | `Ipv6Address::from_octets(data[field::QUERY_MCAST_ADDR].try_into().unwrap())` |
| 59 | 1 | bounds-check | CHURN | `s_flag` | `(data[field::SQRV] & 0x08) != 0` |
| 73 | 1 | bounds-check | CHURN | `qqic` | `data[field::QQIC]` |
| 80 | 1 | slice-index | CHURN | `num_srcs` | `NetworkEndian::read_u16(&data[field::QUERY_NUM_SRCS])` |
| 134 | 1 | panic!/unreachable! | PANIC | `set_qrv` | `assert!(value < 8);` |
| 143 | 1 | bounds-check | CHURN | `set_qqic` | `data[field::QQIC] = value;` |
| 150 | 1 | slice-index | CHURN | `set_num_srcs` | `NetworkEndian::write_u16(&mut data[field::QUERY_NUM_SRCS], value);` |
| 163 | 1 | slice-index | UNATTRIBUTED | `` | `NetworkEndian::write_u16(&mut data[field::NR_MCAST_RCRDS], value)` |
| 259 | 1 | bounds-check | UNATTRIBUTED | `` | `data[field::RECORD_TYPE] = rty.into();` |
| 266 | 1 | bounds-check | UNATTRIBUTED | `` | `data[field::AUX_DATA_LEN] = len;` |
| 273 | 1 | slice-index | CHURN | `set_num_srcs` | `NetworkEndian::write_u16(&mut data[field::RECORD_NUM_SRCS], num_srcs);` |
| 282 | 1 | panic!/unreachable! | PANIC | `set_mcast_addr` | `assert!(addr.is_multicast());` |
| 284 | 1 | slice-index | PANIC | `set_mcast_addr` | `data[field::RECORD_MCAST_ADDR].copy_from_slice(&addr.octets());` |
| 432 | 1 | copy_from_slice | UNATTRIBUTED | `` | `packet.payload_mut().copy_from_slice(&data[..]);` |
| 442 | 1 | copy_from_slice | UNATTRIBUTED | `` | `packet.payload_mut().copy_from_slice(&data[..]);` |

<a id="srcstorageringbufferrs"></a>
### `src/storage/ring_buffer.rs`

21 sites across 8 lines. churn 4, panic 2, core 4. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 110 | 4 | rem-by-zero | CHURN | `get_idx_unchecked` | `(self.read_at + idx) % self.capacity()` |
| 154 | 3 | bounds-check | FLUXBUG | `dequeue_one_with` | `let res = f(&mut self.storage[self.read_at]);` |
| 193 | 3 | slice-index | FLUXBUG | `enqueue_many_with` | `let (size, result) = f(&mut self.storage[write_at..write_at + max_size]);` |
| 245 | 5 | slice-index | FLUXBUG | `dequeue_many_with` | `let (size, result) = f(&mut self.storage[self.read_at..self.read_at + max_size]);` |
| 314 | 1 | slice-index | CORE | `get_unallocated` | `&mut self.storage[start_at..start_at + size]` |
| 345 | 1 | panic!/unreachable! | PANIC | `enqueue_unallocated` | `assert!(count <= self.window());` |
| 369 | 3 | slice-index | CORE | `get_allocated` | `&self.storage[start_at..start_at + size]` |
| 398 | 1 | panic!/unreachable! | PANIC | `dequeue_allocated` | `assert!(count <= self.len());` |

<a id="srcwireicmpv4rs"></a>
### `src/wire/icmpv4.rs`

8 sites across 8 lines. churn 4, panic 0, core 2. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 308 | 1 | bounds-check | CHURN | `set_msg_code` | `pub fn set_msg_code(&mut self, value: u8) {` |
| 325 | 1 | slice-index | CHURN | `set_echo_ident` | `pub fn set_echo_ident(&mut self, value: u16) {` |
| 335 | 1 | slice-index | CHURN | `set_echo_seq_no` | `pub fn set_echo_seq_no(&mut self, value: u16) {` |
| 355 | 1 | slice-index | CHURN | `data_mut` | `let range = self.header_len()..;` |
| 529 | 1 | slice-index | UNATTRIBUTED | `` | `packet.set_msg_type(Message::DstUnreachable);` |
| 530 | 1 | copy_from_slice | CORE | `emit` | `packet.set_msg_code(reason.into());` |
| 543 | 1 | slice-index | UNATTRIBUTED | `` | `packet.set_msg_type(Message::TimeExceeded);` |
| 544 | 1 | copy_from_slice | CORE | `emit` | `packet.set_msg_code(reason.into());` |

<a id="srcifaceinterfacesixlowpanrs"></a>
### `src/iface/interface/sixlowpan.rs`

16 sites across 15 lines. churn 3, panic 7, core 4. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 81 | 1 | slice-index | CORE | `process_sixlowpan` | `Ok(len) => &f.decompress_buf[..len],` |
| 303 | 1 | panic!/unreachable! | PANIC | `dispatch_sixlowpan` | `Packet::Ipv4(_) => unreachable!(),` |
| 413 | 1 | slice-index | PANIC | `dispatch_sixlowpan` | `let mut ieee_packet = Ieee802154Frame::new_unchecked(&mut tx_buf[..ieee_len]);` |
| 458 | 1 | slice-index | PANIC | `ipv6_to_sixlowpan` | `&mut buffer[..iphc_repr.buffer_len()],` |
| 460 | 1 | slice-index | PANIC | `ipv6_to_sixlowpan` | `buffer = &mut buffer[iphc_repr.buffer_len()..];` |
| 518 | 1 | slice-index | UNATTRIBUTED | `` | `&mut Icmpv6Packet::new_unchecked(&mut buffer[..icmp_repr.buffer_len()]),` |
| 527 | 1 | slice-index | PANIC | `ipv6_to_sixlowpan` | `&mut buffer[..udp_repr.header_len() + payload.len()],` |
| 532 | 1 | copy_from_slice | PANIC | `ipv6_to_sixlowpan` | `\|buf\| buf.copy_from_slice(payload),` |
| 539 | 1 | slice-index | UNATTRIBUTED | `` | `&mut TcpPacket::new_unchecked(&mut buffer[..tcp_repr.buffer_len()]),` |
| 549 | 1 | panic!/unreachable! | PANIC | `ipv6_to_sixlowpan` | `_ => unreachable!(),` |
| 720 | 1 | slice-index | CHURN | `decompress_ext_hdr` | `&data[ext_repr.length as usize + ext_repr.buffer_len()..],` |
| 732 | 1 | slice-index | CHURN | `decompress_ext_hdr` | `&mut buffer[..ipv6_ext_hdr.header_len()],` |
| 734 | 1 | slice-index | CHURN | `decompress_ext_hdr` | `buffer[ipv6_ext_hdr.header_len()..][..ipv6_ext_hdr.data.len()]` |
| 771 | 1 | slice-index | CORE | `decompress_udp` | `let mut udp = UdpPacket::new_unchecked(&mut buffer[..payload.len() + 8]);` |
| 773 | 2 | slice-index | CORE | `decompress_udp` | `buffer[8..][..payload.len()].copy_from_slice(payload);` |

<a id="srcwireieee802154rs"></a>
### `src/wire/ieee802154.rs`

34 sites across 27 lines. churn 3, panic 0, core 6. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 371 | 2 | slice-index | CORE | `frame_type` | `let raw = LittleEndian::read_u16(&data[field::FRAMECONTROL]);` |
| 388 | 1 | slice-index | CORE | `dst_addressing_mode` | `let raw = LittleEndian::read_u16(&data[field::FRAMECONTROL]);` |
| 406 | 1 | slice-index | CORE | `src_addressing_mode` | `let raw = LittleEndian::read_u16(&data[field::FRAMECONTROL]);` |
| 450 | 2 | slice-index | CHURN | `addressing_fields` | `Some(&data[field::ADDRESSING][..offset])` |
| 501 | 1 | slice-index | UNATTRIBUTED | `` | `Some(Pan(LittleEndian::read_u16(&addressing_fields[..2])))` |
| 518 | 1 | slice-index | UNATTRIBUTED | `` | `raw.clone_from_slice(&addressing_fields[offset..offset + 2]);` |
| 524 | 1 | slice-index | UNATTRIBUTED | `` | `raw.clone_from_slice(&addressing_fields[offset..offset + 8]);` |
| 543 | 2 | slice-index | CORE | `src_pan_id` | `&addressing_fields[offset..][..2],` |
| 563 | 1 | slice-index | UNATTRIBUTED | `` | `raw.clone_from_slice(&addressing_fields[offset..offset + 2]);` |
| 569 | 1 | slice-index | UNATTRIBUTED | `` | `raw.clone_from_slice(&addressing_fields[offset..offset + 8]);` |
| 640 | 2 | bounds-check, slice-index | UNATTRIBUTED | `` | `let b = self.buffer.as_ref()[index..][0];` |
| 647 | 2 | bounds-check, slice-index | UNATTRIBUTED | `` | `let b = self.buffer.as_ref()[index..][0];` |
| 721 | 1 | slice-index | CHURN | `payload` | `Some(&data[index..])` |
| 732 | 1 | slice-index | UNATTRIBUTED | `` | `let data = &mut self.buffer.as_mut()[field::FRAMECONTROL];` |
| 758 | 1 | bounds-check | UNATTRIBUTED | `` | `data[field::SEQUENCE_NUMBER] = value;` |
| 769 | 2 | slice-index | UNATTRIBUTED | `` | `data[field::ADDRESSING][..2].copy_from_slice(&value.as_bytes());` |
| 781 | 2 | slice-index | UNATTRIBUTED | `` | `data[field::ADDRESSING][2..2 + 2].copy_from_slice(&value);` |
| 787 | 1 | slice-index | UNATTRIBUTED | `` | `let data = &mut self.buffer.as_mut()[field::ADDRESSING];` |
| 788 | 1 | slice-index | UNATTRIBUTED | `` | `data[2..2 + 8].copy_from_slice(&value);` |
| 811 | 1 | panic!/unreachable! | UNATTRIBUTED | `` | `_ => unreachable!(),` |
| 814 | 1 | slice-index | UNATTRIBUTED | `` | `let data = &mut self.buffer.as_mut()[field::ADDRESSING];` |
| 815 | 1 | slice-index | UNATTRIBUTED | `` | `data[offset..offset + 2].copy_from_slice(&value.as_bytes());` |
| 825 | 1 | panic!/unreachable! | UNATTRIBUTED | `` | `_ => unreachable!(),` |
| 835 | 1 | slice-index | UNATTRIBUTED | `` | `let data = &mut self.buffer.as_mut()[field::ADDRESSING];` |
| 836 | 1 | slice-index | UNATTRIBUTED | `` | `data[offset..offset + 2].copy_from_slice(&value);` |
| 842 | 1 | slice-index | UNATTRIBUTED | `` | `let data = &mut self.buffer.as_mut()[field::ADDRESSING];` |
| 843 | 1 | slice-index | UNATTRIBUTED | `` | `data[offset..offset + 8].copy_from_slice(&value);` |

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

11 sites across 8 lines. churn 0, panic 11, core 0. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 90 | 1 | panic!/unreachable! | PANIC | `emit_payload` | `IpRepr::Ipv4(_) => unreachable!(),` |
| 105 | 1 | panic!/unreachable! | PANIC | `emit_payload` | `IpRepr::Ipv4(_) => unreachable!(),` |
| 115 | 1 | slice-index | PANIC | `emit_payload` | `&mut payload[..ipv6_ext_hdr.header_len()],` |
| 121 | 1 | slice-index | PANIC | `emit_payload` | `&mut payload[hbh_start..hbh_end],` |
| 143 | 1 | copy_from_slice | PANIC | `emit_payload` | `\|buf\| buf.copy_from_slice(inner_payload),` |
| 234 | 2 | panic!/unreachable! | PANIC | `as_sixlowpan_next_header` | `Self::Icmpv4(_) => unreachable!(),` |
| 236 | 2 | panic!/unreachable! | PANIC | `as_sixlowpan_next_header` | `Self::Dhcpv4(..) => unreachable!(),` |
| 240 | 2 | panic!/unreachable! | PANIC | `as_sixlowpan_next_header` | `Self::HopByHopIcmpv6(_, _) => unreachable!(),` |

<a id="srcifacerouters"></a>
### `src/iface/route.rs`

1 sites across 1 lines. churn 0, panic 1, core 0. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 173 | 1 | panic!/unreachable! | PANIC | `lookup` | `assert!(addr.is_unicast());` |

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

4 sites across 4 lines. churn 0, panic 1, core 1. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
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

4 sites across 4 lines. churn 0, panic 1, core 1. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
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

9 sites across 9 lines. churn 0, panic 0, core 4. Owner: --.

| line | sites | kind | work | fn | source |
| ---: | ---: | --- | --- | --- | --- |
| 90 | 1 | copy_from_slice | CORE | `resolve` | `bytes[8..].copy_from_slice(inline);` |
| 96 | 1 | copy_from_slice | CORE | `resolve` | `bytes[14..].copy_from_slice(inline);` |
| 117 | 1 | bounds-check | UNATTRIBUTED | `` | `bytes[1] = inline[0];` |
| 118 | 1 | slice-index | CORE | `resolve` | `bytes[11..].copy_from_slice(&inline[1..][..5]);` |
| 123 | 1 | bounds-check | UNATTRIBUTED | `` | `bytes[1] = inline[0];` |
| 124 | 1 | slice-index | CORE | `resolve` | `bytes[13..].copy_from_slice(&inline[1..][..3]);` |
| 130 | 1 | bounds-check | UNATTRIBUTED | `` | `bytes[15] = inline[0];` |
| 139 | 1 | slice-index | UNATTRIBUTED | `` | `bytes[16 - inline.len()..].copy_from_slice(inline);` |
| 144 | 1 | slice-index | UNATTRIBUTED | `` | `bytes[16 - inline.len()..].copy_from_slice(inline);` |

## Caveats

- **Ablation is a ceiling, not a forecast.** `get_unchecked` removes a check whether or not anything proved it safe. These binaries are measured, never flashed.
- **Per-file deltas do not sum.** The eight files' CHURN lines total -1904 B alone but -3624 B of flash together -- superadditive, because shared panic machinery only dies with its last user. Rank with the per-file column; never total it.
- **Noise floor.** An identical rebuild reproduced `.text` exactly (0 B), so there is no link noise -- but a real source change shifts inlining, and the largest INCREASE seen was +332 B. Treat a single-file delta under ~300 B as unresolved.
- **Categories come from the HARDEST Flux error on a function**, not the first. Flux's diagnostic order is not reproducible: two runs of identical code disagreed on 29 rows. A line counts as churn only if every error on its function is churn.
- **`src/wire/mod.rs` and `src/storage/assembler.rs` are excluded from the ceiling** -- the ablator cannot rewrite them (`[u8; N]` has no `__ai` impl; `assembler.rs` hits borrowck). 5 sites.
- **Two files under-ablated** against their targets: `ndiscoption` removed 4 of 7 targeted, `nhc` 5 of 7, mostly `const fn` bodies the rewriter skips. Their small deltas are understated.
