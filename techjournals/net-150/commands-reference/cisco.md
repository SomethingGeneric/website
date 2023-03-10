# Cisco

### Routers

* `enable` allows privileged config (if the router has a password, you'd be prompted for it.)
* `config` to enter config mode
  * `router rip` to enter RIP
    * Set V2 with `version 2`
    * Add network with `network <ID>`
    * Exit with just `exit`
  * `exit` to exit (and save!)
* `show ip route` shows information about routing settings (seems to include RIP and/or static)

**VLANs**

Once in `config`,

* To create a vlan:
  * `vlan <id>`
  * `name <something>`
  * `end`
* To assign a port to a vlan:
  * `interface <if_name>`
  * `switchport access vlan <id>`
  * `exit`
* To set a port as trunk:
  * `interface <if_name>`
  * `switchport mode trunk`
  * To permit/add a vlan id: `switchport trunk allowed vlan <add/remove> <id>`
  * `end`

**Virtual Interfaces**

(Once in `config` )

```
R1(config)#interface fastEthernet 0/0
R1(config-if)#no shutdown
R1(config-if)#exit

R1(config)#interface fastEthernet 0/0.10
R1(config-subif)#encapsulation dot1Q 10
R1(config-subif)#ip address 192.168.10.254 255.255.255.0
R1(config-subif)#exit

R1(config)#interface fastEthernet 0/0.20
R1(config-subif)#encapsulation dot1Q 20                 
R1(config-subif)#ip address 192.168.20.254 255.255.255.0
```

Borrowed from [https://networklessons.com/cisco/ccna-routing-switching-icnd1-100-105/how-to-configure-router-on-a-stick](https://networklessons.com/cisco/ccna-routing-switching-icnd1-100-105/how-to-configure-router-on-a-stick)
