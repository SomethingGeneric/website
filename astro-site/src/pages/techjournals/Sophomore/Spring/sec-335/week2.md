---
layout: /src/layouts/MarkdownLayout.astro
---
# Week 2 (Class on 1/29/24)

## Active Recon
Network scanning, ping, etc

## NMAP Suggestions
Recommendation for multiple targets:
1. Do host discovery and port scanning first
2. Then perform -sV against specific ports (using `-p <port_list>`)

## 2.1 Host Discovery Script (Item 2)
```bash
#!/usr/bin/env bash
for d in $(seq 2 50); do
        ip="10.0.5.$d"
        ping -c 1 -W 5 $ip

        if [[ "$?" == "0" ]]; then

                echo "Host $ip is up"
                echo "$ip" >> sweep.txt

        fi

done
```
Thankfully, the ping command only exits with 0 if it gets back the response it wants, so `$?` was a godsend for this one.

## 2.1 fping Host Discover One-Liner (Item 3)
```bash
sudo fping -a -g 10.0.5.2 10.0.5.50 | grep --invert-match "ICMP" >> sweep2.txt
```
This was a bit silly, but it kept me from needing to use regex yet.

## 2.1 nmap Host Discovery One-Liner (Item 6)
```bash
sudo nmap -sn 10.0.5.2-50 | egrep '[0-9]{2,3}\.' | awk '{n=split($0,a," "); print a[n]}' >> sweep3.txt
```
There is probably a better way to strip away the rest of the nmap output than this awful `awk` syntax, but it does work.
The AWK script was adapted from [this post](https://stackoverflow.com/a/39703302)