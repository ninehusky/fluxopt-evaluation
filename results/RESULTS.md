# usb_ethernet, nRF52840: upstream vs ninehusky

Produced by `./run.py`. See ../README.md for what the numbers mean.

```
toolchain 1.97   target thumbv7em-none-eabi   profile release   bin usb_ethernet
baseline  embassy https://github.com/embassy-rs/embassy @ 7c2eac8a1450dbfbcc138a03c79aef4b880aff7b
baseline  xarxa   https://github.com/embassy-rs/xarxa @ 1f332ac32cc33d86aefc8e1c1a9749b93234a6de
modified  embassy https://github.com/ninehusky/embassy @ 460e274e50c0d799eceedd8e6192f31f6ded5c35
modified  xarxa   local /Users/andrew/research/xarxa-conv51-0908 @ 6c341714870437947d9acb6b94e968abe5b76252 (DIRTY: uncommitted edits included)
```

| metric | baseline | modified | delta | delta % |
| --- | --- | --- | --- | --- |
| .text | 105840 | 102704 | -3136 | -3.0% |
| .rodata | 17152 | 14356 | -2796 | -16.3% |
| .data | 24 | 24 | +0 | +0.0% |
| .bss | 32388 | 32388 | +0 | +0.0% |
| flash total | 123272 | 117340 | -5932 | -4.8% |
| RAM (.data+.bss+.uninit) | 32412 | 32412 | +0 | +0.0% |
| panic call sites | 503 | 407 | -96 | -19.1% |
| panicking functions | 135 | 128 | -7 | -5.2% |

### Panic call sites by crate

| crate | baseline | modified | delta |
| --- | --- | --- | --- |
| xarxa | 292 | 211 | -81 |
| embassy_usb | 58 | 58 | +0 |
| embassy_net | 38 | 50 | +12 |
| embassy_futures | 35 | 35 | +0 |
| embassy_net_driver_channel | 26 | 1 | -25 |
| embassy_executor | 25 | 25 | +0 |
| embassy_nrf | 15 | 15 | +0 |
| core | 9 | 7 | -2 |
| RTC1 | 2 | 2 | +0 |
| __embassy_time_queue_item_from_waker | 1 | 1 | +0 |
| GPIOTE | 1 | 1 | +0 |
| embassy_sync | 1 | 1 | +0 |

### Which symbols hold the panics

Inlining moves branches between symbols, so a function appearing on one side only usually means the same panic was attributed elsewhere in the other build, not that a panic was added or removed.

Holds panics in baseline only (42):
  - <core::slice::iter::IterMut<core::option::Option<(u32, u32)>> as core::iter::traits::iterator::Iterator>::fold::<(), <core::iter::adapters::enumerate::Enumerate<_> as core::iter::traits::iterator::Iterator>::fold::enumerate<&mut core::option::Option<(u32, u32)>, (), core::iter::traits::iterator::Iterator::for_each::call<(usize, &mut core::option::Option<(u32, u32)>), <xarxa::wire::tcp::TcpOption>::parse::{closure#0}>::{closure#0}>::{closure#0}>
  - <embassy_net::Stack>::with_mut::<core::result::Result<(), xarxa::socket::tcp::ListenError>, <embassy_net::tcp::TcpIo>::with_mut<core::result::Result<(), xarxa::socket::tcp::ListenError>, <embassy_net::tcp::TcpSocket>::accept<u16>::{closure#0}::{closure#0}>::{closure#0}>
  - <embassy_net_driver_channel::Device<1514> as embassy_net_driver::Driver>::receive
  - <embassy_net_driver_channel::RxToken<1514> as embassy_net_driver::RxToken>::consume::<xarxa::iface::interface::PollIngressSingleResult, <embassy_net::driver_util::RxTokenAdapter<embassy_net_driver_channel::RxToken<1514>> as xarxa_driver::RxToken>::consume<xarxa::iface::interface::PollIngressSingleResult, <xarxa::iface::interface::Interface>::socket_ingress<embassy_net::driver_util::DriverAdapter<embassy_net_driver_channel::Device<1514>>>::{closure#0}>::{closure#0}>
  - <embassy_net_driver_channel::TxToken<1514> as embassy_net_driver::TxToken>::consume::<(), <embassy_net::driver_util::TxTokenAdapter<embassy_net_driver_channel::TxToken<1514>> as xarxa_driver::TxToken>::consume<(), <xarxa::iface::interface::InterfaceInner>::dispatch_ethernet<embassy_net::driver_util::TxTokenAdapter<embassy_net_driver_channel::TxToken<1514>>, <xarxa::iface::interface::InterfaceInner>::dispatch<embassy_net::driver_util::TxTokenAdapter<embassy_net_driver_channel::TxToken<1514>>>::{closure#0}>::{closure#0}>::{closure#0}>
  - <embassy_net_driver_channel::TxToken<1514> as embassy_net_driver::TxToken>::consume::<(), <embassy_net::driver_util::TxTokenAdapter<embassy_net_driver_channel::TxToken<1514>> as xarxa_driver::TxToken>::consume<(), <xarxa::iface::interface::InterfaceInner>::dispatch_ethernet<embassy_net::driver_util::TxTokenAdapter<embassy_net_driver_channel::TxToken<1514>>, <xarxa::iface::interface::InterfaceInner>::lookup_hardware_addr<embassy_net::driver_util::TxTokenAdapter<embassy_net_driver_channel::TxToken<1514>>>::{closure#0}>::{closure#0}>::{closure#0}>
  - <embassy_net_driver_channel::TxToken<1514> as embassy_net_driver::TxToken>::consume::<(), <embassy_net::driver_util::TxTokenAdapter<embassy_net_driver_channel::TxToken<1514>> as xarxa_driver::TxToken>::consume<(), <xarxa::iface::interface::InterfaceInner>::dispatch_ip<embassy_net::driver_util::TxTokenAdapter<embassy_net_driver_channel::TxToken<1514>>>::{closure#3}>::{closure#0}>
  - <xarxa::iface::interface::Interface>::set_hardware_addr
  - <xarxa::socket::dhcpv4::Socket>::dispatch::<<xarxa::iface::interface::Interface>::socket_egress<embassy_net::driver_util::DriverAdapter<embassy_net_driver_channel::Device<1514>>>::{closure#4}, <xarxa::iface::interface::Interface>::socket_egress::EgressError>
  - <xarxa::storage::assembler::Assembler>::add
  - <xarxa::storage::ring_buffer::RingBuffer<u8>>::enqueue_many_with::<&mut [u8], <xarxa::storage::ring_buffer::RingBuffer<u8>>::enqueue_many::{closure#0}>
  - <xarxa::storage::ring_buffer::RingBuffer<u8>>::write_unallocated
  - <xarxa::storage::ring_buffer::RingBuffer<xarxa::storage::packet_buffer::PacketMetadata<xarxa::socket::udp::UdpMetadata>>>::dequeue_one_with::<(), <xarxa::iface::interface::Interface>::socket_egress::EgressError, <xarxa::storage::packet_buffer::PacketBuffer<xarxa::socket::udp::UdpMetadata>>::dequeue_with<(), <xarxa::iface::interface::Interface>::socket_egress::EgressError, <xarxa::socket::udp::Socket>::dispatch<<xarxa::iface::interface::Interface>::socket_egress<embassy_net::driver_util::DriverAdapter<embassy_net_driver_channel::Device<1514>>>::{closure#2}, <xarxa::iface::interface::Interface>::socket_egress::EgressError>::{closure#0}>::{closure#0}>
  - <xarxa::wire::arp::Repr>::emit::<&mut [u8]>
  - <xarxa::wire::dhcpv4::Repr>::emit::<[u8]>
  - <xarxa::wire::icmpv4::Repr>::emit::<[u8]>
  - <xarxa::wire::icmpv6::Packet<&[u8]>>::msg_type
  - <xarxa::wire::icmpv6::Packet<&mut [u8]>>::clear_reserved
  - <xarxa::wire::icmpv6::Repr>::emit::<[u8]>
  - <xarxa::wire::icmpv6::Repr>::emit::emit_contained_packet::<[u8]>
  - <xarxa::wire::icmpv6::Repr>::parse::<[u8]>
  - <xarxa::wire::icmpv6::Repr>::parse::create_packet_from_payload::<[u8]>
  - <xarxa::wire::ip::Repr>::emit::<&mut [u8]>
  - <xarxa::wire::ip::Repr>::new
  - <xarxa::wire::ipv4::Repr>::emit::<&mut [u8]>
  - <xarxa::wire::ipv4::Repr>::parse::<[u8]>
  - <xarxa::wire::ipv6::Repr>::emit::<&mut [u8]>
  - <xarxa::wire::ipv6hbh::Repr>::emit::<[u8]>
  - <xarxa::wire::ipv6option::Repr>::emit::<[u8]>
  - <xarxa::wire::mld::Repr>::emit::<[u8]>
  - <xarxa::wire::mld::Repr>::parse::<[u8]>
  - <xarxa::wire::ndisc::Repr>::emit::<[u8]>
  - <xarxa::wire::ndisc::Repr>::parse::<[u8]>
  - <xarxa::wire::ndiscoption::Repr>::emit::<[u8]>
  - <xarxa::wire::ndiscoption::Repr>::parse::<[u8]>
  - <xarxa::wire::tcp::Repr>::emit::<[u8]>
  - <xarxa::wire::tcp::Repr>::parse::<[u8]>
  - <xarxa::wire::udp::Packet<&[u8]>>::payload
  - <xarxa::wire::udp::Packet<&[u8]>>::verify_checksum
  - <xarxa::wire::udp::Packet<&mut [u8]>>::fill_checksum
  - <xarxa::wire::udp::Repr>::emit::<[u8], <xarxa::iface::packet::Packet>::emit_payload::{closure#0}>
  - <xarxa::wire::udp::Repr>::emit::<[u8], <xarxa::iface::packet::Packet>::emit_payload::{closure#1}>

Holds panics in modified only (35):
  - <embassy_net::driver_util::DriverAdapter<embassy_net_driver_channel::Device<1514>> as xarxa_driver::Device>::receive
  - <embassy_net::driver_util::RxTokenAdapter<embassy_net_driver_channel::RxToken<1514>> as xarxa_driver::RxToken>::consume::<xarxa::iface::interface::PollIngressSingleResult, <xarxa::iface::interface::Interface>::socket_ingress<embassy_net::driver_util::DriverAdapter<embassy_net_driver_channel::Device<1514>>>::{closure#0}>
  - <embassy_net::driver_util::TxTokenAdapter<embassy_net_driver_channel::TxToken<1514>> as xarxa_driver::TxToken>::consume::<(), <xarxa::iface::interface::InterfaceInner>::dispatch_ethernet<embassy_net::driver_util::TxTokenAdapter<embassy_net_driver_channel::TxToken<1514>>, <xarxa::iface::interface::InterfaceInner>::dispatch<embassy_net::driver_util::TxTokenAdapter<embassy_net_driver_channel::TxToken<1514>>>::{closure#0}>::{closure#0}>
  - <embassy_net::driver_util::TxTokenAdapter<embassy_net_driver_channel::TxToken<1514>> as xarxa_driver::TxToken>::consume::<(), <xarxa::iface::interface::InterfaceInner>::dispatch_ethernet<embassy_net::driver_util::TxTokenAdapter<embassy_net_driver_channel::TxToken<1514>>, <xarxa::iface::interface::InterfaceInner>::lookup_hardware_addr<embassy_net::driver_util::TxTokenAdapter<embassy_net_driver_channel::TxToken<1514>>>::{closure#0}>::{closure#0}>
  - <embassy_net::driver_util::TxTokenAdapter<embassy_net_driver_channel::TxToken<1514>> as xarxa_driver::TxToken>::consume::<(), <xarxa::iface::interface::InterfaceInner>::dispatch_ip<embassy_net::driver_util::TxTokenAdapter<embassy_net_driver_channel::TxToken<1514>>>::{closure#1}>
  - <embassy_net::tcp::TcpIo>::with_mut::<core::result::Result<(), xarxa::socket::tcp::ListenError>, <embassy_net::tcp::TcpSocket>::accept<u16>::{closure#0}::{closure#0}>
  - <xarxa::iface::interface::Interface>::socket_egress_one::<embassy_net::driver_util::DriverAdapter<embassy_net_driver_channel::Device<1514>>>::{closure#3}
  - <xarxa::iface::interface::InterfaceInner>::emit_ethernet_into
  - <xarxa::socket::tcp::Socket>::dispatch::<<xarxa::iface::interface::Interface>::socket_egress_one<embassy_net::driver_util::DriverAdapter<embassy_net_driver_channel::Device<1514>>>::{closure#2}, xarxa::iface::interface::EgressError>
  - <xarxa::storage::ring_buffer::RingBuffer<u8>>::dequeue_many_with::<&mut [u8], <xarxa::storage::ring_buffer::RingBuffer<u8>>::dequeue_many::{closure#0}>
  - <xarxa::storage::ring_buffer::RingBuffer<xarxa::storage::packet_buffer::PacketMetadata<xarxa::socket::udp::UdpMetadata>>>::dequeue_one_with::<(), xarxa::iface::interface::EgressError, <xarxa::storage::packet_buffer::PacketBuffer<xarxa::socket::udp::UdpMetadata>>::dequeue_with<(), xarxa::iface::interface::EgressError, xarxa::socket::udp::dequeue_payload<(), xarxa::iface::interface::EgressError, <xarxa::socket::udp::Socket>::dispatch<<xarxa::iface::interface::Interface>::socket_egress_one<embassy_net::driver_util::DriverAdapter<embassy_net_driver_channel::Device<1514>>>::{closure#1}, xarxa::iface::interface::EgressError>::{closure#0}>::{closure#0}>::{closure#0}>
  - <xarxa::wire::arp::Repr>::emit::<xarxa::wire::buf::Buf>
  - <xarxa::wire::buf::Buf>::copy_at
  - <xarxa::wire::dhcpv4::Repr>::emit::<xarxa::wire::buf::Buf>
  - <xarxa::wire::icmpv4::Repr>::emit::<xarxa::wire::buf::Buf>
  - <xarxa::wire::icmpv6::Repr>::emit::<xarxa::wire::buf::Buf>
  - <xarxa::wire::icmpv6::Repr>::emit::emit_contained_packet::<xarxa::wire::buf::Buf>
  - <xarxa::wire::ipv4::Packet<xarxa::wire::buf::Ref>>::next_header
  - <xarxa::wire::ipv4::Repr>::emit::<xarxa::wire::buf::Buf>
  - <xarxa::wire::ipv4::Repr>::parse_ref
  - <xarxa::wire::ipv6::Repr>::emit::<xarxa::wire::buf::Buf>
  - <xarxa::wire::ipv6option::Repr>::emit::<xarxa::wire::buf::Buf>
  - <xarxa::wire::mld::Repr>::emit::<xarxa::wire::buf::Buf>
  - <xarxa::wire::mld::Repr>::parse
  - <xarxa::wire::ndisc::Repr>::emit::<xarxa::wire::buf::Buf>
  - <xarxa::wire::ndisc::Repr>::parse
  - <xarxa::wire::ndiscoption::Repr>::emit::<xarxa::wire::buf::Buf>
  - <xarxa::wire::tcp::Repr>::emit::<xarxa::wire::buf::Buf>
  - <xarxa::wire::tcp::Repr>::parse_ref
  - <xarxa::wire::udp::Packet<xarxa::wire::buf::Ref>>::verify_checksum
  - <xarxa::wire::udp::Repr>::emit_checksum::<xarxa::wire::buf::Buf>
  - <xarxa::wire::udp::Repr>::emit_slice::<xarxa::wire::buf::Buf>
  - xarxa::storage::packet_buffer::dequeue_one::<xarxa::socket::udp::UdpMetadata, (), xarxa::iface::interface::EgressError, xarxa::socket::udp::dequeue_payload<(), xarxa::iface::interface::EgressError, <xarxa::socket::udp::Socket>::dispatch<<xarxa::iface::interface::Interface>::socket_egress_one<embassy_net::driver_util::DriverAdapter<embassy_net_driver_channel::Device<1514>>>::{closure#1}, xarxa::iface::interface::EgressError>::{closure#0}>::{closure#0}>
  - xarxa::wire::buf::copy_window_at
  - xarxa::wire::buf::write_u16_at

Full lists: `results/*.panicking-functions.txt`; every call site with its address: `results/*.panic-call-sites.txt`
