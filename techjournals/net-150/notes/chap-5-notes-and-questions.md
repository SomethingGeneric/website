# Chap 5: Notes & Questions

## Notes

* LAN's only allow communication "nic-to-nic"
* Hubs are "dumb" layer 1 devices, thus all they do is copy incoming packets to all other ports
* Switches are layer 2 devices, and only forward traffic to a port with the appropriate MAC
* Switches store the destination MAC's in an internal table, which could have one of a few names
  * CAM Table
  * MAC Table
  * Lookup table
* Switches act like hubs on boot, until they build their table by watching thru-traffic and storing source information
* If the switch doesn't know a MAC, it'll broadcast the backet to all ports to hopefully find an answer for the future
* To get a MAC address for a destination, computers use ARP Broadcasts. This basically asks all devices on the network: `What's the physical address for ip <some_ip>`
* Computers store the response in an ARP Cache, so that they don't have to ask over-and-over again
* While a packet is in-transit, between LAN's, the destination MAC is constantly updated to be the next hop.

## Questions

* Can an attacker on LAN steal traffic simply by spoofing their MAC to be the same as the victim? (I know most traffic is encrypted, but, regardless??)
* Can you impersonate the router/gateway by responding first to an ARP query?
