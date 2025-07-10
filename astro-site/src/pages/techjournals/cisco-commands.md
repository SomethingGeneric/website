---
layout: /src/layouts/MarkdownLayout.astro
---
# Cisco iOS Cheatsheet

## Routers General

* `enable` allows privileged config (if the router has a password, you'd be prompted for it.)
* `config` to enter config mode
  * `router rip` to enter RIP
    * Set V2 with `version 2`
    * Add network with `network <ID>`
    * Exit with just `exit`
  * `exit` to exit (and save!)
* `show ip route` shows information about routing settings (seems to include RIP and/or static)

## Setting IP adresses/networks

Go into `config`,
* `interface <device name here>`
* `ip address <ip> <mask>`
* `no shutdown`

## VLANs

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

## Virtual Interfaces

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

## Static Routing
```
switch# configure terminal
switch(config)#
switch(config)# ip route 192.0.2.0/8 ethernet 1/2 192.0.2.4
switch(config)# show ip static-route
switch(config)# copy running-config startup-config # save config for next reboot
```

## Using interface ranges (for VLAN assignment, mostly)
```
switch# configure terminal
switch(config)# interface range FastEthernet 0/x-y
switch(config)# switchport access vlan x
```

## Change a port to trunk mode
```
switch# configure terminal
switch(config)# interface FastEthernet 0/x
switch(config)# switchport trunk
```

## Using ip helper-address
This is for DHCP across subnets/interfaces
```
router(config)# interface vlan <id_here> # or a fa or ge interface
router(config)# ip helper-address <dhcp_server_addr_here>
```

## Static NAT
Define where's inside and where's outside
```
R1(config)# interface <type> <number> # e.x. fa 0/0
R1(config)# ip nat inside
R1(config)# exit
R1(config)# interface <type> <number> # e.x. serial 0/0/0
R1(config)# ip nat outside
R1(config)# exit
```

Then you can add a static mapping like:
```
R1(config)# ip nat inside source static <LAN IP of machine> <IP in WAN range for router>
# in our case:
R1(config)# ip nat inside source static 10.0.0.2 50.0.0.1
```

## PAT
```
# Create a "pool" with the public IP (only 1 in this case)
R1(config)#ip nat pool test 30.0.0.120 30.0.0.120 netmask 255.0.0.0
# Allow the 192.168.1.X clients to use said pool
R1(config)#access-list 1 permit 192.168.0.0 0.0.0.255
# Connect pool and ACL for going from inside to outside
# overload allows up to 64k clients
R1(config)#ip nat inside source list 1 pool test overload
```

## Setting up OSPF
Firstly, ensure that each router has it's interface IP addresses configured. Then, on each router:
```
router ospf 1
network <network IP> <network mask> area 0
# repeat the above line for each network that's directly connected to this router
```

The `1` after `router ospf` is a PID number, for complex routing setups where the router will have multiple executibles of the OSPF process running. We are ignoring this
The `area 0` in each `network` command is to tell the router that the given network is in the backbone area. In a more complex setup, each layer going "down" would have a higher value here.