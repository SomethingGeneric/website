# CentOS Combined Reference
(Useful for SEC260 and SYS255)

## From SEC 260
* `dhclient` - to use DHCP to request an ip address
* Firewall:
    * `firewall-cmd --permanent --add-port=80/tcp` - Example for adding port 80 over TCP (otherwise known as HTTP)
    * `firewall-cmd --reload` - Reload config to apply changes
    * `firewall-cmd --query-port=80/tcp` - Query if port 80 is open
* `ip addr` - Show interface ip addresses
* `yum install ...` - Package manager
* `vi` - Silly editor
* `nano` - Slightly less silly editor
* `systemctl restart ...` - Restart a running service (like `httpd`, or `sshd`)

## From SYS 255
* `nmtui` - Edit network settings for interfaces managed by NetworkManager (like `eth0`)
* `adduser <username>` - Add a new user (and home directory)
* `useradd -m <username>` - Add a new user (and home directory) (for more options see `useradd --help` or `man useradd`)
* `passwd <username>` - Set the password for a user
* `usermod -aG wheel <username>` - Add a user to the wheel group (for more options see `usermod --help` or `man usermod`)
* `history | head -n 10` - Show the first 10 entries 

## Manual Page Tags
* `man hier` - Show the manual page for the filesystem layout