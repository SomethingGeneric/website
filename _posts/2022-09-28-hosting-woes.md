---
layout: post
title:  "Hosting Woes"
date:   2022-09-28 18:29:00 -0400
categories: hosting nginx fail2ban linux
---
# Irritations with Hosting
As I'm sure you know (since I mentioned it on the site at least once), I help host Crystal Linux's infrastructure, using two different nodes. 
One of which is a home server, that, of my own admission, was a little lacking in the security department.
So, when someone came along scraping for servers to exploit, they spent quite a bit of time on my node that happens to also be (temporarily) serving the role of primary Crystal Linux package server.
Hence, poof went the package updates. And oh, in come the discord messages.
As an added Murphy's law moment, around the same time, we were due for a new ISO image release. Except, GitHub now couldn't pull packages from _me_ either!

## Nginx Limiting
Through a combination of sources, most of which are so far buiried in my firefox history as to be inaccesible, I managed to eek out some request limits on nginx, which seems to have (mostly?) solved the issue.

## Fail2ban
Fail2ban seems to be incredibly versatile, if you have the willpower to spend ages configuring it. Luckily for me, combining the default `nginx-limit-req` rule and `ufw` seemed to work _well enough._ (And by that, I mean that editing the nginx conf worked, and the rest was a disaster)

## Conclusion
Please hurry up and fix mirroring, OSSPlanet!!

## Next-Day Update
We're setting up a strong VPS with our new OpenCollective money 👀, so even if we keep delaying OSSPlanet, this should still be resolved Soon:tm:
