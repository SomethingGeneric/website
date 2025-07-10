---
layout: /src/layouts/MarkdownLayout.astro
---
# Week 9 (Class on 3/25/24)

This week was _really_ good fun. I enjoyed the challenge of having absolutely no hints as to what angle to take with this target.

The two things that tripped me up the most 

1. I couldn't get a DNS server to give up the (non-public) IP of `gloin.shire.org` (btw, outside of range environment, it's a real domain name, and I obviously didn't want to get in any real trouble.) I actually never found a solution to this, but Erik suggested just grabbing the IP from it's summary panel in vSphere, which I did, and it was right, but still feels a bit like cheating.

2. I spent an awful lot of time looking for applicable vulnerabilities to the specific versions of Apache, SSH, and Terminal Services on the box, especially since it seems like they tend to happen a lot for the SSH/HTTPD builds for Windows 10. However, ultimately, I was thinking way too hard, and then I had a much easier time of it when I googled the specific web app that the server's HTTPD was giving me. (Being intentionally obtuse to avoid runining your fun, if you're another student in ethhack in the future. :p) 