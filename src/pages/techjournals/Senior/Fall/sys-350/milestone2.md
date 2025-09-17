---
layout: /src/layouts/MarkdownLayout.astro
---
 
# Milestone 2 - vCenter

vCenter was pretty complicated, and took a while, even after deploying a Windows Server VM, sysprepping it, and installing ADDS as we've done in previous sysadmin classes.

Things that went wrong:

## Sysprep
I had some weird error when trying to follow along with Devin's 480prep script that goes through adding SSH to Windows, and then running sysprep with a `unattend.xml` file: https://github.com/gmcyber/480share/blob/master/ssh-prep.ps1

I was running all the lines manually, and for some reason, a couple reboots finally got sysprep going. (I did also have to close the sysprep UI window that had been spawned by entering into the sysprep desktop thing with ctrl+shift+f8)

## vCenter
The first time I deployed it, I didn't notice that I said it should be on the `VM network` instead of my `350-internal` network.

The vCenter installer took it's merry time, and somehow did manage to complete stage 1, but then failed at stage 2, at which point I tried to load it in the browser, which finally showed an error related to DNS or networking, which made me realize the mistake I had made.

At that point, I just went in to the ESXi web interface, and manually nuked the vCenter VM, before starting over from my Xubuntu mgmt box. 

Everything went smoothly with my second install (on the correct network), until I got to the step where we were supposed to update the version of vCenter.

At that point, when I would click for updates, it would say "could not reach update server" (or something to that effect), which I thought was odd, as I was fairly certain I had configured the network correctly, and indeed, upon inspection in the web UI, I had.

So, to debug this, I enabled SSH and Bash through the `:5480` "admin" UI for vCenter (*sidenote*: this is really annoying terminology, since the "normal" vCenter UI has some administrative functions, like adding SSO, but then some *different* admin tasks get banished to this second admin panel on a different port number for,,,,, some reason.....?)

And after `ssh`-ing to it as `root@vcenter.matt.local`, and running `shell` for bash, I could indeed confirm that I could ping `1.1.1.1`, and `nslookup google.com` just fine.

At that point, I decided that 8.0.0 was probably good enough, and just moved on with the lab. (I reckon that the reason it "can't" reach the update server is just because this is an older version with an 'eval' license, which I believe is one of many things Broadcom has clamped down on? But I could be wrong).

After that nonsense, adding my vCenter to the domain went fine, but it did take a concerning amount of time to come back up, so much so that I thought I had broken something, but I ended up finding out that I just had to fully close and reopen firefox on mgmt01 for whatever reason.

And with that, the lab was done.