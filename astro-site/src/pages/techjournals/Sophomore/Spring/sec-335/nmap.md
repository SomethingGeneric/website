---
layout: /src/layouts/MarkdownLayout.astro
---
# nmap cheatsheet

General syntax is `sudo nmap <host>`

Where `<host>` is an IP, domain name, or range of IP's.

## Host Spec Examples

* Single IP: `sudo nmap 10.0.1.1 <options>`
* Domain: `sudo nmap goober.cloud <options>`
* IP Range: `sudo nmap 10.0.0.0/24` (network ID)
* Multiple IPs (not net ID): `sudo nmap 10.0.0-10` (first 11)

## Flags breakdown

* `-A`: Enable OS detection, version detection, script scanning, and traceroute (good flag if you're doing a general look-see)
* `-p <number>`: Scan only this port(s). You can do things like `-p 22` but also `-p 22-80` or `-p 22,25`
* `-sV`: Determine version info of discovered services
* `-O`: Enable OS detection
* `-sn`: Ping scan (default if you're not using `sudo` or logged in as root)
* `-Pn`: Treat all host(s) as online

See all flags with `man nmap` or online at https://linux.die.net/man/1/nmap

### FYI
If you use `-A`, you're essentially doing `-sV sC -O --traceroute`