# Lab 01 - Network Management / Monitoring

## web01-matt details
* IP: `10.0.5.200`
* **NOT** on AD
* Admin: `matt` (which is in the `wheel` group)

## pfSense (fw01) SNMP
* Community string: `JoeOfTheEast`
* All modules enabled
* No traps
* Only on the LAN interface
* The page has a silly restart icon which will reboot the daemon

## nmon01-matt details
* IP: `10.0.5.11`
* **NOT** in AD
* Same admin as `web01-matt`
* SNMP utils installed (see [CentOS Notes](/techjournals/centos-commands.md))

## web01-matt SNMPD Config
Path: `/etc/snmp/snmpd.conf`
```
com2sec myNetwork 10.0.5.0/24 JoeOfTheEast
group myROGroup v2c myNetwork
view all included .1 80
access myROGroup "" any noauth exact all none none
```

Allowed port `161/udp` in `firewall-cmd`