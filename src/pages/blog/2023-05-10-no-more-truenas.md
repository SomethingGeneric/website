---
layout: /src/layouts/MarkdownLayout.astro
title: "Moving away from TrueNAS"
---
# TrueNAS is pretty mediocre
I only really used it to begin with because a lot of YouTube and online resources reccomend it as a starting place for running your own fileserver.

And, for the record, it is pretty good at doing exactly that.

However, over time, as I've spent more time hands-on with Debian and other more traditional server operating systems, it's been a pain in the ass to adapt other processes around TrueNAS's web-UI only style of doing things.

So, I decided it was time to get rid of it.

## Migration process

I'm not one to do things well-planned in advance, so I burned a USB stick with Debian 11.7, and shut down TrueNAS without any more thought to it.

(For anyone curious, I *did* check to make sure that nothing important was on the TrueNAS boot device, and instead on the ZFS mirrored disks that I wanted to preserve.)

When my server Chewie was running TrueNAS (first CORE, then later SCALE), the disks were as follows:
* ~250GB SATA SSD (boot device, I have absolutely 0 idea how they partitioned it)
* 4 TB WDC HDD (ZFS Mirror disk #1)
* 4 TB WDC HDD (ZFS Mirror disk #2)

I had over a terrabyte of disk space used on the total ZFS array, and no other disk large enough to hold all of the data, so I was banking on OpenZFS being as easy to use as I had read online. Thankfully for my sanity, that turned out to be the case.

Like with any other server, the first thing I did was a base Debian install with only "common utils" and "ssh server", and had the installer do a one-partition setup on the 250GB SSD device.

One I was booted in to my new Debian install, I did some light googling to figure out what I would have to set up for ZFS. Turns out, it's not hard at all. 

Following the instructions from the OpenZFS website (except note that I personally skipped backports, as I think they skimp on stability sometimes) (https://openzfs.github.io/openzfs-docs/Getting%20Started/Debian/)

The instructions are basically the following steps:
```
# if you haven't enabled 'contrib' in your /etc/apt/sources.list yet (I hadn't)
sudo nano /etc/apt/sources.list
sudo apt update
sudo apt install build-essential dpkg-dev linux-headers-generic linux-image-generic -y
sudo apt install zfs-dkms zfsutils-linux -y
```

Now since I had the ZFS kernel module, I had to reboot.

Next, I ran across this AskUbuntu post (https://askubuntu.com/questions/123126/how-do-i-mount-a-zfs-pool), which kind've answered my question in a round-about way.

My pool had been named "Storag" in TrueNAS (not sure where the "e" went. Oh well), so I tried
```
sudo zpool import Storag
```
And to my suprise, it worked! 

(Side note, the OP in the thread (or maybe a reply?) mentioned this older blog post, of someone doing much what I was, but I didn't end up needing it. https://web.archive.org/web/20171211140530/http://www.servercobra.com/freenas-to-ubuntu-initial-fileserver-setup-with-zfs)

Then, all I had to do was figure out how to set up NFS shares (as I had previously only used TrueNAS's awful webUI for it.)

Turns out, this too, was super easy.

This Atlantic.net article was super helpful (once you scroll past their quick self-advertisement): https://www.atlantic.net/dedicated-server-hosting/how-to-install-and-configure-nfs-server-on-debian-11/

TL;DR for Debian:
```
sudo apt-get update -y
sudo apt-get install nfs-kernel-server -y
```

Then you need to edit `/etc/exports` like:
```
/some_path 10.0.0.69(rw,sync,no_subtree_check)
```

(The article documents the options in the `()`'s, and the IP is made up.)

Finally, you just
```
sudo systemctl restart nfs-server
```

And, done!

## Conclusion

Obviously for some people the migration of TrueNAS could be more complex, but personally, half the reason I felt the need to move was because I wasn't using the machine for anything but ZFS and NFS, as I find the webUI just that frustrating.

It would obviously have been more taxing to migrate if I had been running apps from the TrueNAS marketplace still, but if that had been true, I probably wouldn't have been motivated to switch the machine at all.

Hopefully this short post can be SEO'd well enough to help out someone else! :D