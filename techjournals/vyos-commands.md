# VyOS Cheatsheet

### Changing user password
```
configure
set system login user vyos authentication plaintext-password PasswordGoesHere
commit
save
exit
```
from: https://support.vyos.io/support/solutions/articles/103000096301-set-change-the-password-of-a-user

### Changing hostname
```
configure
set system host-name fw01-matt
commit
save
exit 
```

### Set system DNS server
```
configure
set system name-server IPHERE
commit ; save ; exit
```

### Setting interfaces
```
configure
set interfaces ethernet eth0 description SEC350-WAN
set interfaces ethernet eth0 address IPADDRESS/MASK
commit
save
exit
```

### Upstream gateway
```
configure
set protocols static route 0.0.0.0/0 next-hop GATEWAYIPHERE
commit ; save ; exit
```

### NAT & DNS Forwarding
```
configure
set nat source rule 10 description "NAT FROM DMZ to WAN"
set nat source rule 10 outbound-interface eth0
set nat source rule 10 source address 172.16.50.0/29
set nat source rule 10 translation address masquerade
commit ; save ; exit
```

### DNS Forwarding from subnets
```
configure
set service dns forwarding listen-address 172.16.50.2
set service dns forwarding allow-from 172.16.50.0/29
set service dns forwarding system
commit ; save ; exit
```

## End steps done in lab 1.1 (sec350)

### Remote syslog for VyOS
```
configure
set system syslog host 172.16.50.5 facility authpriv level info
commit ; save ; exit
```

## Setting up zone policy
```
configure

set zone-policy zone <NAME> interface ethX
set zone-policy zone <NAME> from <NAME> firewall name <SOME_FIREWALL>
# repeat if you have more than one inbound for this zone

# then you need to create the actual firewall configs that go with each zone:
set firewall name <FROM_ZONE>-to-<TO_ZONE> default-action drop
set firewall name <FROM_ZONE>-to-<TO_ZONE> enable-default-log

# allow return traffic:
set firewall name <FROM_ZONE>-to-<TO_ZONE> rule 1 action accept
set firewall name <FROM_ZONE>-to-<TO_ZONE> rule 1 state established enable
set firewall name <FROM_ZONE>-to-<TO_ZONE> rule 1 state related enable

# allow other services
set firewall name set firewall name <FROM_ZONE>-to-<TO_ZONE> rule 10 action accept
set firewall name <FROM_ZONE>-to-<TO_ZONE> rule 10 description "some service forwarding"
set firewall name <FROM_ZONE>-to-<TO_ZONE> rule 10 destination address <IP_HERE>
set firewall name <FROM_ZONE>-to-<TO_ZONE> rule 10 destination port <N>
set firewall name <FROM_ZONE>-to-<TO_ZONE> rule 10 protocol <TCP/UDP>

# repeat above block with a different rule ID (e.g. 11, etc) for other services that need to pass a given firewall

commit ; save ; exit
```

If you need to debug a given firewall, easiest way is to temporarily:
```
configure
set firewall name <BROKEN_FIREWALL_NAME> default-action accept
commit;save;exit
```

To see if that firewall is indeed the problem.

## RIP
```
configure

set protocols rip interface ethX # which interface to talk to other routers
set protocols rip network <NETID>/<MASK> # advertise this network (it's directly connected to this router)

commit ; save ; exit
```