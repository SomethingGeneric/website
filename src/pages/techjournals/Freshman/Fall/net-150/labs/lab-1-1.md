---
layout: /src/layouts/MarkdownLayout.astro
title: "Lab 1-1"
---
# Lab 1-1

## Summary:

Listing network device information on my desktop PC, from my Linux install.

## Answers to questions:

In Linux, on my desktop machine in my dorm, (connected to WiFi), my ethernet adapter has:

* IPv4: `184.171.147.46`
* Gateway: `184.171.147.0`
* Subnet mask: `255.255.255.0`
* Physcial Address: `2c:8d:b1:5b:97:cb`
* DNS Server(s): `216.93.145.253`

For some reason, the supposed default gateway wouldn't repond to my pings. I also included the output of both ways that I thought to find the default gateway, and both show the same IP. ![image](/images/github_cdn_95933568.png)

Pinging `google.com`, though, does respond, which is good since my PC does have an internet connection. ![image](/images/github_cdn_b165132e.png)

It seems like the Wi-Fi DHCP does some funny stuff, because there are different leading digits for my PC, iPhone, and laptop, even though they're all connected to the same SSID, which would make me think that they're talking to the same AP.... Right?

There are 13 hops between my desktop and google.com. The named ones were:

* `stu-253-147-171-184.champlain.edu`
* `112-0-0-10.champlain.edu`
* `65-183-130-25-static.burlingtontelecom.net`
* `15169-dc10.equinix.com`
* `lga34s36-in-f14.1e100.net` ![image](/images/github_cdn_bcb72f9e.png)

After running `nslookup`, DNS reports: 3 addresses for `bing.com`: ![image](/images/github_cdn_dfd0156f.png)

And 1 address for `www.champlain.edu` ![image](/images/github_cdn_5a1c7856.png)
