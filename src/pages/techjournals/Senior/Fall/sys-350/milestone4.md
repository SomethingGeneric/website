---
layout: /src/layouts/MarkdownLayout.astro
---
 
# Milestone 4 - Nested Virtualization

## Objectives:
1. Create three nested ESXi hosts, and add them to vCenter
2. Make two Linux template VMs, and set up a customization flow so that newly cloned VMs have a pre-set hostname and IP address.

## Results:
This milestone was pretty straightforward, with just a few hiccups.

1. To set up the customization flows, you have to click the top-most left three dashes menu, which we never really used when Champlain's cyber.local environment was running vCenter, so I didn't even think to look there, I had to google it, and even then, the explanation for where it was didn't immediately get me there.
2. My MGMT box kept seemingly "fighting" me about DNS server assignment, so it would periodically make the vCenter UI hiccup and think my ESXi host wasn't responding... Very weird. Even weirder is that it went away on it's own....
3. My pfSense box kept giving MGMT net IPs via DHCP to hosts on my LAN (or the reverse, I can't quite remember??), and yet the adapter settings were correct, and everything worked as normal.... That was really bizzare. I "fixed" it by disabling DHCP on all but the one I needed at a given time (and my lease times were quite high so it's fine™)
4. It took me a bit to figure out that the vSwitch settings we needed to change for allowing nested hosts were in the ESXi panel not vCenter.
5. The vm-tools version that ESXi/vCenter have is super old, and failed on some (but not all) Linux OS's, as it seems to be a version from before-systemd. However, all of the distros I tried had a system package "open-vm-tools" or similar, which seems to provide at least a majority of the same functionality, and installed with no issues at all.
