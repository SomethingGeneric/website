---
layout: /src/layouts/MarkdownLayout.astro
---
 
# Milestone 6 - Hyper V

## Setting up Hyper V & Management Tools
(I really should know the exact names for `Add-WindowsFeature`, but I just used RSAT to pick the HyperV role and didn't un-check the management tools option.)

## Configuring Hyper V Networks
First, I disabled all my interfaces except for 1 (our supermicros have 8 phys interfaces, and most students seem to have many ethernet patch cables used for them.... idk why?). Then, with the one remaining interface, I assigned my designated IPv4 as static.

Then, in the HyperV manager, I created my vSwitch by selecting the same interface name as I could see when I hovered over the correct adapter in the Network & Sharing center (this is really clunky, I miss Linux interface naming {sentence that should never be uttered by man, btw})

Then adding an internal-only network was ezpz (one click, just worked.)

## Configuring Firewall
I just used the pfSense CE 2.7 ISO from the cyber.local share {but you can always check files.thibble.org :) }

The only non-standard thing was going into the manual vm setings menu (after initial setup) to make sure I had a second net interface (on the internal-only network)

When installing pfSense, I realized that the HyperV UI doesn't show the mac addresses for your VMs interfaces in the settings page (_why????_), so I just guessed that hn0 was the first adapter, and hn1 was the second, which was correct!

## Importing a VM
The .zip mentioned in the lab assignment is a VMDX file, so you can't actually "import" it, but instead you go through the "create a vm" flow, and just select the existing VMDX instead of having it create one for you.

Also, this VM template is really slow, so I'm glad I have a second VM that I installed manually with an ISO.