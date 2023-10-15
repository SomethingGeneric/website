# CentOS 7 Combined Reference
(Useful for SEC260 and SYS255)

## From SEC 260
* `dhclient` - to use DHCP to request an ip address
* Firewall:
    * `firewall-cmd --permanent --add-port=80/tcp` - Example for adding port 80 over TCP (otherwise known as HTTP)
    * `firewall-cmd --reload` - Reload config to apply changes
    * `firewall-cmd --query-port=80/tcp` - Query if port 80 is open
* `ip addr` - Show interface ip addresses
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
* `systemctl start ...` - Start a service (like `dhcpd` or `sshd`)
* `systemctl enable ...` - Enable a service to auto-start on boot
* `chown USER:GROUP ...` - Change the owner (and group if specified) of given file/directory
* `chmod PERMS ...` - Set the permissions of file/dir to `PERMS`, described in [this assignment](sys-255/pre-assesment/linux_file_permissions.md)
* `groups` - Show groups your user is a member of
* `su ...` - (S)witch (U)ser, defaults to `root` if not specified.

## Manual Page Tags
* `man hier` - Show the manual page for the filesystem layout

## Package Commands:
* `yum install ...` - Install package
* `yum update` - Sync repos
* `yum upgrade` - Install newer versions over current versions

## Package Names
* `httpd` - Apache2, for some reason
* `mod_ssl` - Apache2 SSL functionality

## Paths
* `/etc/pki/tls/{certs,private}` - for SSL certs