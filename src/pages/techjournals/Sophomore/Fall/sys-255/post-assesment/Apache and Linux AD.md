---
layout: /src/layouts/MarkdownLayout.astro
---
# Apache & Linux AD Lab

## Setup pt 1 (on web01)
* Reset root password & make a user & make sure user is in `wheel`
* Set `PermitRootLogin no` in `/etc/ssh/sshd_config`
* Use `nmtui` to set desired IP, gateway, DNS, search domain
* Change hostname w/ `sudo hostnamectl set-hostname <something> && sudo vi /etc/hosts && sudo reboot`

## Deliverable 1
Proves:
* ssh to web01 by A record
* named sudo user
* Working networking
(screenshot omitted)

## Setup pt 2 (still web01)
* `yum install httpd`
* `firewall-cmd --add-port=80/tcp --permanent`
* `firewall-cmd --add-port=443/tcp --permanenet`
* `firewall-cmd --reload`

## Deliverable 2
Output of `firewall-cmd --list-all`
(screenshot omitted)

## Turn on apache (YAY)
* `systemctl enable --now httpd`

## Deliverable 3
Screenshot of browser on ad or wks browsing to `http://web01-matt`

## Apache edits
* Comment out everything in `/etc/httpd/conf.d/welcome.conf`
* `vi /var/www/html/index.html`
* `systemctl restart httpd`

## Deliverable 4
Screenshot of your custom webpage having replaced the default from Deliverable 3

## PHP Install & Script
* `yum install -y php`
* `vi /var/www/html/index.php`
```
<?php
echo 'Hello SYS 255<br/>';
for ($x=1; $x <= 10; $x++) {
  echo "X is $x<br/>";
}
?>
```

## Deliverable 5
(Screenshot of rendered PHP)

## AD Setup (on web01)
* `yum install -y realmd samba samba-common oddjob oddjob-mkhomedir sssd`
* `realm join --user=matt.compton-adm@matt.local matt.local && realm list`

## Deliverable 6
After `ssh alice@matt.local@web01-matt`, `id`, `whoami`, `pwd`

## Deliverable 7
Screenshot of AD Users & Computers showing that `web01` is in there with `fs01`
