# Linux

* `ip addr` - Similar information to `ipconfig` on Windows
* `ip route show` - Also fairly similar to `ipconfig`
* `route -n` - Seemed to be the fastest way to get default gateway
* `ifconfig` - Also fairly similar to `ipconfig`
* `ping -c 3` - Pretty much the same usage as for windows, but include `-c <some_number>` so that it doesn't loop forever.
* `traceroute` - Same as `tracert` in Windows.
* `arp -d <ip>` - Remove arp entry for `ip`
* `arp -n` - list known MAC's
* `ip -s -s neigh flush all` - Remove all known MAC's from ARP
