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
set protocols static route 0.0.0.0/0 next hop GATEWAYIPHERE
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
set service dns allow-from 172.16.50.0/29
set service dns forwarding system
commit ; save ; exit
```

## End steps done in lab 1.1 (sec350)