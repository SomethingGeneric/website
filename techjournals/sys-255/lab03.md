# Lab 03 - Linux

## Some of the items in here involved editing my (CentOS Reference)[/techjournals/centos-commands.md] page.

## Setting up the ethernet interface
Using `nmtui` command, set the network interface `ens192` to the following:
* IPv4 Configuration: Manual
* IP Address: 10.0.5.3/24
* Gateway: 10.0.5.2
* DNS Server: 10.0.5.5
* Search domain: matt.local

Outside of the interface, set the hostname to `dhcp01-matt`

## Adding a new user, and setting them as a wheel member
* `adduser matt` (OR `useradd -m matt`)
* `passwd matt`
* `usermod -aG wheel matt`

## Deliverable 1 (somehow)
![Deliverable 1](/lab03_deliverable1.png)
This deliverable demonstrates correctly configured networking on `dhcp01-matt`

## Deliverable 2
![Deliverable 2](/lab03_deliverable2.png)
This deliverable demonstrates that the correct A record has been created on `ad01-matt` for `dhcp01-matt`

## Deliverable 3
![Deliverable 3](/lab03_deliverable3.png)
This deliverable shows logging in as the local user `matt` on `dhcp01-matt` from `wks01-matt` using SSH

## Deliverable 4
![Deliverable 4](/lab03_deliverable4.png)
This deliverable shows the first 10 commands I ran after signing in to `dhcp01-matt`

## Deliverable 5
* Pros and cons of bash's history function: It’s a useful reference for if you forget how you did something, or if you later find out you broke something. On the other hand, it would allow any user with admin privileges to the system to view all commands you have executed, or if a bad actor has access to your user account.
* How to clear bash history: A combination of `history -c && rm .bash_history && history -c` did the trick for me