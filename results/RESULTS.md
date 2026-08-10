# usb_ethernet, nRF52840: upstream vs ninehusky

Produced by `./run.sh`. See ../README.md for what the numbers mean.

```
toolchain      1.97   target thumbv7em-none-eabi   profile release   bin usb_ethernet
baseline  embassy https://github.com/embassy-rs/embassy @ 7c2eac8a1450dbfbcc138a03c79aef4b880aff7b
baseline  xarxa   https://github.com/embassy-rs/xarxa @ 1f332ac32cc33d86aefc8e1c1a9749b93234a6de
modified  embassy https://github.com/ninehusky/embassy @ 460e274e50c0d799eceedd8e6192f31f6ded5c35
modified  xarxa   https://github.com/ninehusky/xarxa @ f42ae2866a63f32b3230a8dc24c95f209ccc22ad
```

| metric | baseline | modified | delta | delta % |
| --- | --- | --- | --- | --- |
| .text | 138124 | 137620 | -504 | -0.4% |
| .rodata | 18936 | 18924 | -12 | -0.1% |
| .data | 80 | 80 | +0 | +0.0% |
| .bss | 34004 | 34004 | +0 | +0.0% |
| flash (.text+.rodata+.data) | 157140 | 156624 | -516 | -0.3% |
| panic call sites | 660 | 657 | -3 | -0.5% |
| panicking functions | 169 | 167 | -2 | -1.2% |

Panicking in baseline but not modified (4):
  - <xarxa::iface::interface::Interface>::set_hardware_addr
  - <xarxa::storage::ring_buffer::RingBuffer<xarxa::storage::packet_buffer::PacketMetadata<xarxa::socket::udp::UdpMetadata>>>::dequeue_one_with::<(), (), <xarxa::storage::packet_buffer::PacketBuffer<xarxa::socket::udp::UdpMetadata>>::dequeue_padding::{closure#0}>
  - <xarxa::storage::ring_buffer::RingBuffer<xarxa::storage::packet_buffer::PacketMetadata<xarxa::socket::udp::UdpMetadata>>>::dequeue_one_with::<(), <xarxa::iface::interface::Interface>::socket_egress::EgressError, <xarxa::storage::packet_buffer::PacketBuffer<xarxa::socket::udp::UdpMetadata>>::dequeue_with<(), <xarxa::iface::interface::Interface>::socket_egress::EgressError, <xarxa::socket::udp::Socket>::dispatch<<xarxa::iface::interface::Interface>::socket_egress<embassy_net::driver_util::DriverAdapter<embassy_net_driver_channel::Device<1514>>>::{closure#2}, <xarxa::iface::interface::Interface>::socket_egress::EgressError>::{closure#0}>::{closure#0}>
  - <xarxa::wire::ip::Repr>::new

Panicking in modified but not baseline (2):
  - <core::iter::adapters::map::Map<core::iter::adapters::filter::Filter<core::slice::iter::Iter<xarxa::iface::route::Route>, <xarxa::iface::route::Routes>::lookup::{closure#0}>, core::iter::traits::iterator::Iterator::max_by_key::key<&xarxa::iface::route::Route, u8, <xarxa::iface::route::Routes>::lookup::{closure#1}>::{closure#0}> as core::iter::traits::iterator::Iterator>::fold::<(u8, &xarxa::iface::route::Route), core::iter::traits::iterator::Iterator::max_by::fold<(u8, &xarxa::iface::route::Route), core::iter::traits::iterator::Iterator::max_by_key::compare<&xarxa::iface::route::Route, u8>>::{closure#0}>
  - <xarxa::socket::udp::Socket>::dispatch::<<xarxa::iface::interface::Interface>::socket_egress<embassy_net::driver_util::DriverAdapter<embassy_net_driver_channel::Device<1514>>>::{closure#2}, <xarxa::iface::interface::Interface>::socket_egress::EgressError>

Full lists: results/*.panicking-functions.txt; every call site: results/*.panic-call-sites.txt
