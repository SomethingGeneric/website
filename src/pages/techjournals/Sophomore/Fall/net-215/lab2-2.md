---
layout: /src/layouts/MarkdownLayout.astro
---
# Lab 2-2

## First PCAP
* The Ethernet header is 14 bytes.
* It looks like the very very first 6 bytes are the destination MAC address.
* The IPv4 header is 20 bytes.
* The ethernet header is the first one we see because it’s the most fundamental part of moving a packet between devices.
* Packet capture file is: [tcipg](/public/images/tcipg.pcapng)

## Second PCAP
* The ethernet header is 32 bytes
* The padding is 18 bytes
* The padding is included because the response ARP payload is so short that the entire packet would be too small otherwise. (Source: “... which means an additional 18 bytes of padding had to be added to ensure this frame reaches the minimum acceptable length of 64 bytes.” from: https://www.practicalnetworking.net/series/arp/traditional-arp/)
* Packet capture file is [switch_ping](/public/images/switch_ping.pcapng)