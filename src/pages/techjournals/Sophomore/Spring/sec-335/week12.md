---
layout: /src/layouts/MarkdownLayout.astro
---
# Week 12 (Class on 4/22/24)

## Physical Access Lab
Changing `C:\\Windows\\System32\\Utilman.exe` and/or `C:\\Windows\\System32\\sethc.exe` for `cmd.exe` is a super easy way to get in to a Windows box, assuming you have a USB key of Kali or some other distro.

The only trouble that I encountered with this lab was that the VM spun up Windows once before I changed the boot option, so it was marked as hibernated when I tried to `mount /dev/sda2 /mnt/foo` in Kali. To fix this, I found [this post](https://unix.stackexchange.com/questions/163806/force-mount-windows-hibernated-partition-in-read-write-mode) which suggested `ntfsfix /dev/sda2`, which worked flawlessly for me!