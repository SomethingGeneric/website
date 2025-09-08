---
layout: /src/layouts/MarkdownLayout.astro
---
 
# Milestone 1

This first milestone largely went smoothly for me, so hence I only have a couple general notes.

(To future me: hopefully I wrote down anything that was important!!)
(Also, there's a note in Bitwarden with passwords)

## ESXi Misc Notes:
* Installed ESXi on the smaller disk (~250gb), set root password, rebooted.
* Had to then immediately change password with the device console, I guess I didn’t type it right the first time??
* Updated networking via IPMI to the ESXi console in order to use my static ipv4 assignment.
* Changed hostname by going to manage -> system -> advanced settings (not sure if that’s the “correct” way to do it, but it worked.)


## ESXi vSwitch Notes (I find this quite confusing personally)
For networking so that my firewall can talk to both the Freeman network and also the internal virtual LAN, you set one vNIC to the VM Network (which apparently is pre-configured as passthru to the physical NIC, AKA on the same LAN as the hypervisor itself), and then make another vNIC to talk to your 350 virtual internal network.

## Xubuntu
Xubuntu MGMT box is 10.0.17.100, DNS name matt.local
And it's on the internal vnet
(Creds in Bitwarden?? (I hope?))
