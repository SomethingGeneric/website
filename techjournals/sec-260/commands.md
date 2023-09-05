# Command Reference

## CentOS 7
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