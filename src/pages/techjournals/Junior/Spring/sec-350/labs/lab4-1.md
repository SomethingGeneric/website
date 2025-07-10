---
layout: /src/layouts/MarkdownLayout.astro
---
# Lab 4.1 - Network Firewalls 1

## Where's the notes?
Most of my documentation for this lab involved editing/expanding the VyOS reference sheet, specifically the sections "Setting up zone policy" and "RIP"

## Troubleshooting issues
The main issue I had in this particular lab was that I accidentally disabled new connections outbound from `fw01` by setting `state established enable` in rule 1 of `LAN-to-WAN` firewall, rather than simply `rule 1 accept`. 
As stated in my VyOS reference page, I tested to see if that firewall was the problem by `set firewall name LAN-to-WAN default-action accept ; commit ; save`, and when my pings started working again, I ran `show firewall name LAN-to-WAN`, and noticed my mistake. Oopsies!

## Exporting VyOS Config
I created a Git repository: https://github.com/SomethingGeneric/sec350 
Installing git on VyOS was a bit of an adventure. 

The tl;dr is that you need to create a file like: `sudo nano /etc/apt/sources.list.d/sec350.list` 
And input:
```
deb https://deb.debian.org/debian bullseye main contrib non-free
```

Then you can run `sudo apt update` (DO NOT RUN `apt upgrade` !!! The internet says it will break VyOS (thankfully I read that and did not try it myself))

Finally, you can now run `sudo apt install -y git`

And then git should work as normal, only without bash tab-completion like you'd be used to on a more "normal" linux machine.