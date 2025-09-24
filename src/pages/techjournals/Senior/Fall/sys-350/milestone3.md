---
layout: /src/layouts/MarkdownLayout.astro
---
 
# Milestone 3 - Additional networks

Creating additional networks is easy, but then I had a bit of a headache with pfSense.

Adding new networks in esxi is easy, you just go to "networking" and add new "port groups".

Then, you add two new interfaces to your pfSense box, and assign one to each network.

Then, make sure you keep an eye on the virtual MAC interface, so you won't mix it up twice like I did.

**NOTE** for some reason, adding the two interfaces flipped the `vmX` names of my WAN and LAN, so I actually had to go and re-validate my existing interfaces as well. 🙃

Next, go into Interfaces, and give each a name corresponding to the ESXi port group, MAKE SURE to match the MAC addresses.

Then you can also assign them each to their new network. I did:
* LAN - 10.0.17.0/24
* DMZ - 10.0.18.0/24
* MGMT - 10.0.19.0/24

Then, verify in Firewall -> NAT -> outbound that each new interface (presumably renamed to MGMT and DMZ) has it's network listed in the automatic outbound nat rules that pfSense should have made for you.

Finally, the thing that I had the most trouble with, which is allowing traffic on these OPTx interfaces.

In Firewall -> Rules -> interface_name, create a rule with the "Add ⤵️" button, and allow traffic from source any, protocol any, to destination any, to allow all traffic by default.

Then, for your DMZ network, go back and add rules for source any, protocol any, destination LAN net, and one rule for destination MGMT net, and set those rules action to "block".