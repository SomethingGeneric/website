---
layout: /src/layouts/MarkdownLayout.astro
---
# Lab 2-1

## Part 1
### Ping request outbound:
Source MAC: `48:21:0b:33:57:99`
Destination MAC: `d0:81:c5:23:bd:80`

### Ping reply inbound:
Source MAC: `d0:81:c5:23:bd:80`
Destination MAC: `48:21:0b:33:57:99`

### Q1: My MAC is 48:21:0b:33:57:99, and the default gateway MAC address is d0:81:c5:23:bd:80

## Part 2
### Ping request MAC addresses:
Source MAC: `48:21:0b:33:57:99`
Destination: `d0:81:c5:23:bd:80`

### Q2: The MAC of 34.174.229.22 “is” d0:81:c5:23:bd:80


## Part 3
### MAC addresses:
Source: `48:21:0b:33:57:99`
Destination: `48:21:0b:33:5e:44`

### Q3: The next PC over has the MAC of 48:21:0b:33:5e:44

## Part 4
The “next layer” field in an ethernet header seems to be `Type: IPv4 (0x0800)`
The “next layer” field in the IPV4 header seems to be `Protocol: ICMP`
I believe the very first 6 bytes are a representation of the destination MAC address of the packet.
