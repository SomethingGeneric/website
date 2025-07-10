---
layout: /src/layouts/MarkdownLayout.astro
---
# Lab 1.1

IP Assignment Sheet: https://docs.google.com/spreadsheets/d/1QfUMFhFyiDqfvJU24Fav5s71LYY_LKGA/edit?gid=2000835468#gid=2000835468

## rw01-matt
* Changed `champuser` password
* Added `sudo` user `matt`
* Set IP with `nmtui` (netplan makes me sad)
* Set hostname with `hostnamectl set-hostname`

## fw01-matt

Steps taken for the firewall are listed in the VyOS reference sheet, from the top to the noted stop point.


## web01-matt

* Changed root password
* Made `matt` sudo user, set password
* Set IP address, DNS, etc
* IP on DMZ: `172.16.50.3`

## log01-matt

* Same steps as web01-matt
* IP on DMZ: `172.16.50.5`

Had to edit `/etc/rsyslog.conf` to recieve entries from `web01`:

![config file changes](/sec350-rsyslog-log01.png)