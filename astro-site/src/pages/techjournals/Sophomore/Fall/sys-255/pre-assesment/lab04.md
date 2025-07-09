# Lab 04: DHCP

## Some of the items in here involved editing my [CentOS Reference](/techjournals/centos-commands.md) page.

## Step 0: PuTTY
(Installing PuTTY just involves downloading the `.msi` file from their [website](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html))
(The only interesting part was using `matt.compton-adm` domain admin for the UAC prompt)

## Step 1: Installing dhcp
* Run `yum install dhcp` - Installs the dhcp daemon that we configure

## Step 2: Configure dhcpd
* Run either `nano /etc/dhcp/dhcpd.conf` as root, or prefix with `sudo`
* Type in contents like the below:
![contents of dhcpd.conf](/lab04_dhcpd_conf.PNG)

## Step 3: Start & Enable dhcpd
* Run `systemctl start dhcpd` (prefix with `sudo` if you're not logged in as root)
    * This command starts `dhcpd` in the background as a daemon
* Run `systemctl enable dhcpd` (again, prefix with `sudo` if needed.)
    * This command instructs the system to auto-start the service when the system boots.

## Step 4: Allow dhcpd through firewall
* Run `firewall-cmd --add-service=dhcp --permanent`
    * The firewall's rule sets know that dhcp is UDP port 67, so we don't have to explicitly say it.
* Run `firewall-cmd --reload` to make the change active.

## Step 5: Reconfigure Workstation to use the new DHCP server
Like in Lab 1, we're editing the adapter options. Only this time, we're setting both back to automatic
* Control Panel -> Network and Internet -> Network Connections
* `Ethernet0` properties -> IPv4 Properties
* Tick `Obtain an IP address automatically`
* Tick `Obtain DNS server address automatically`

## Deliverable 1
Proving that DHCP works correctly with a screenshot of `ipconfig /all`
![results of ipconfig command](/lab04_deliverable1.PNG)

## Deliverable 2
Log entries on `dhcp01-matt` of the DHCP request from `wks01-matt`
Command used: `sudo cat /var/log/messages | grep wks01-matt`
![results of command](/lab04_deliverable2.PNG)

## Deliverable 3
Wireshark outputs from DHCP transaction.
![wireshark capture](/lab04_deliverable3.PNG)

## Deliverable 4
To change the lease time, I consulted [an online man page for dhcpd](https://linux.die.net/man/8/dhcpd), and edited the file `/etc/dhcp/dhcpd.conf`

Contents of the file:
![updated configuration](/lab04_deliverable4_pt1.PNG)

Proof of updated lease time
![ipconfig new output](/lab04_deliverable4_pt2.PNG)