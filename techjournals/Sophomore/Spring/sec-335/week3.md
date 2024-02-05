# Week 3 (Class on 2/5/24)

## Awful terrible one-liner for NMAP DNS Discovery
* Step 1: `sudo nmap -Pn 10.0.5.0/24 -p 53 --open -oG dns-servers2.txt`
* Step 2: `cat dns-servers2.txt | grep -v Nmap | egrep '[0-9]{2,3}\.' | awk '{split($0,a," "); print a[2]}' | uniq` (there's gotta be a better way! {but this works})

## Script content
Some of the items for this week's class activity are in my [scripts repo](https://git.goober.cloud/matt/sec335-scripts/src/branch/main/week3/activity3.1)

The most horrendous of them is [nmap enumeration](https://git.goober.cloud/matt/sec335-scripts/src/branch/main/week3/activity3.1/nmap_enumerate.sh)

All the variants of DNS enumeration are in that folder.

## Other one-line magic
After doing
```bash
dig axfr @nsztm1.digi.ninja zonetransfer.me >> zt.txt
# and
dig axfr @nsztm2.digi.ninja zonetransfer.me >> zt.txt
```

Then I wrote out
```bash
cat zt.txt | grep -v ";" | egrep "\sA\s" | awk '{print $1" - "$5}'
```

To grab the DNS names and host IPs. It's not too complicated, but it took me way too long to just use `egrep` instead of trying to get a conditional to work in pure AWK (sorry to  Brian Kernighan, I tried my best.)

## Overall
DNS enumeration is important to find all of the potential targets in a given IP range and/or under a target domain name.
Combining this with prior recon to find appropriate domain names should give a fairly complete picture of a target profile for a given company/org/govt