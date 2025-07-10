---
layout: /src/layouts/MarkdownLayout.astro
---
# Server Core / Remote Admin Lab

## In `sconfig` on fs01
* Set admin password
* Set network adapter settings:
    ![fs network](/public/images/nconfig.png)
* Set hostname & reboot
* Go back to sconfig, join domain, reboot again

## Deliverable 1
(screenshot of `sconfig` after domain join. Omitted for brevity.)

## On AD
* Add `File Server Resource Manager Tools`, and install
![Add feature wizard](/public/images/roles-feats.png)
* Add fs01 to the management window by right-clicking on `All Servers`, and adding it. Then, type in `fs` to find it by name.
 
## Deliverable 2
![Screenshot of both servers in the admin panel](/public/images/rsat-del2.png)

## On AD (in AD Users & Groups tool)
* Create OU's: `SYS-255/{Users,Computers,Groups}`
* Create Global Security Group `Sales-Users` in `SYS-255/Groups/`
* Add users `Bob` and `Alice` in `SYS-255/Users`
* Add `Alice` to `Sales-Users`
* Add `File Server Resource Manager` to fs01 through the add features and roles from server manager
    ![Tree view of features added](/public/images/rsat-arfw.png)

## On FS01
* Run the following command to open the firewall for remot e file server management: `netsh advfirewall firewall set rule group=”Remote File Server Resource Manager Management” new enable=yes`

## Deliverable 3
Screenshot of File Server Resource Manager on ad connected to fs01

## On AD01
* Through server manager -> File and Storage Services, create a quick share on fs01 called `Sales`, leaving the options alone, and noting the local and remote paths.
* Edit permissions by right clicking on Sales share, clicking permissions, and then "customize permissions"
* Remove "everyone has acces"
* Add Sales-Users OU as having full control.

## Deliverable 4
* PT #1 is showing that alice can use the share
* PT #2 is showing that bob cannot
(screenshots omitted)

## Deliverable 5:
Researching, and implementing, a GPO to map the network share to `S:\` on a machine if a user in `Sales-Users` signs in.
(Screenshots omitted.)
Resource used: https://activedirectorypro.com/map-network-drives-with-group-policy/
