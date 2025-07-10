---
layout: /src/layouts/MarkdownLayout.astro
---
# Week 1 (Class on 1/22/24)

## Passive Recon
Before investigating a target directly, you should always do research on the target to expand your information on it as much as possible without triggering log entries related 
to your activity (i.e. direct network scans, attempting to connect, etc) (also known as active recon)

Examples of this include, but are not limited to
1. Googling (and likely [google dorking](https://en.wikipedia.org/wiki/Google_hacking)) the target for details related to the company, other websites/IP's etc
2. Checking known domains/IPs with tools like https://shodan.io
3. Using tools like [theHarvester](https://github.com/laramies/theHarvester) or [BlackBird](https://github.com/p1ngul1n0/blackbird) (if the target is an individual/org) to find related web URLs, emails, ASN numbers, etc
4. Tools like exiftool to find metadata from related documents/files.

## Compiling
Make sure to take good notes on what you find during passive recon, as it will likely come in useful in future steps.