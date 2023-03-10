# Chap 1: Intro To Networking Notes/Questions

## Notes

* Modern LAN's are usually Ethernet or WiFi
* Different topologies:
  * Bus Topology: Used by origional ethernet w/ coaxial cable, went from one device to the next. Connected from one device to the next.
  * Ring Topology: Not commonly used, all traffic basses between other members
  * Mesh Topolgy: Not commonly used, can be for high-reliability setups. Requires lots of cabling.
  * Star Topolgy: Most common for modern LANs. Cable break only affects one device, but if the central device fails, the whole network is down.
  * Star-mesh hybrid: Common for enterprise. Balances effeciency and redundancy. Star connects to uyser devices, and backbone devices are in mesh
* MAC Addresses:
  * 12 hex digits (6 bytes {48 bits}) long.
  * First six are used to indicate the NIC's vendor
  * Last sick are unique to the device
* IP Addresses:
  * 32 bit number
  * Typically displayed as four 8-bit numbers with dots in-between (This is called dotted decimal notation, in which each 8-bit number is called an octet)
  * The Net ID is always the beginning of the address
  * While they're always 32 bits, the groupings can differ.
    * Net ID can be anywhere from 8 to 30 bits.
    * Host ID is the rest
    * Subnet mask defines how long the Net ID is.
  * Breakdown of IP address example:
    * Binary rep: `10000001101010100001001011011100`
    * Dotted-decimal: `129.170.18.220`
    * Subnet mask is `/24`
    * So, the Network ID is `129.170.18` and the host ID is `220`
* IP Ranges:
  * If an organization owns `129.170.0.0/16`, then they can assign addresses between `129.170.0.1` - `129.70.255.254`
* More on subnet masks:
  * `/16` is `255.255.0.0`
  * `/24` is `255.255.255.0`
  * Essentially, all `1`'s for Network ID length.
* Integration with the OSI Model:
  * IP Addresses belong to Layer 3 (Network layer)
  * MAC Addresses belong to layer 2 (datalink)

## Questions

* In a topology like bus, ring, or mesh, where (in theory) other devices could see the traffic for your MAC, is there anything to prevent them from snagging it, assuming they had your MAC?
