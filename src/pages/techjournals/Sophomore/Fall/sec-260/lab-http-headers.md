---
layout: /src/layouts/MarkdownLayout.astro
---
# "Lab": 3.x(??): HTTP Headers

## Part 1: Manual HEAD request
I recieved a 200 response.
![response for HTTP HEAD request](/images/telnet_8008_HEAD_sec260.png)

## Part 2: Chrome Web Inspection bit
My User-Agent is `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36`

This page didn't have have a content type header (not explicitly anyways)

The date that the page was last modified NOT SET

### Picture Questions
It's content-type: `image/jpeg`

The Referrer was: `https://web.ics.purdue.edu/~gchopra/class/public/pages/webdesign/05_simple.html`

The referrer is that URL since it’s the page with the HTML tag that embeds “prettypicture.jpg”

### Another web page
Yes, I did get a 304 response code.

I assume that the “cache-control” header tells the browser that it doesn’t necessarily need to re-request the same content