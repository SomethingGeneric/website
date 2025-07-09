# Lab 02: AD and DNS

## Pre-Setup:
The `ad01` preconfigured machine didn't boot, so I followed the regedit instructions in this guide: https://woshub.com/windows-install-error-computer-restarted-unexpectedly/
And afterwards it booted.

## IP Setup for ad01
![IP Config windows for ad01](/lab02_image.png)

And the details that were set:
```
IP Address:  10.0.5.5
Netmask: 255.255.255.0
Gateway 10.0.5.2 (Make sure fw01 is running).
DNS 10.0.5.2
```

Final config:
![Finished ad01 ipv4](/lab02_image-1.png)

## Date & TZ & Machine Name
* Timezone already read UTC-5 in the server manager, so I left it alone.
* Clicking on the computer name box in the server manager opened a dialog box to change the hostname, so I did, and then rebooted.

## Verifying system settings & network connectivity
![powershell command output](/lab02_image-2.png)

## Installing ADDS Role
There are screens to bypass where the defaults are ok.
The box that must be selected is "Active Directory Domain Services"
Make sure to allow the installer to grab dependencies as well.
Then you can skip all the way to performing install.

## Seting AD Deployment Config
You'll see the following message
![ad error after install](/lab02_image-3.png)

Click on it, and then change the "deployment operation" to "add a new forest", and enter "yourname.local" as the root domain name.

And then.... after one long install and reboot

## Setting up local DNS for fw01
DNS manager clicks
![i hate the windows clicky-things](/lab02_image-4.png)

## Reverse PTR Zone
Here's the menu
![hate windows](/lab02_image-5.png)
Then you do a new zone with mostly defaults

![uejfiefsef](/lab02_image-6.png)
It works!!

## Making Accounts
Management is under `Tools/Active Directory Users and Computers` from the Server Manager

Right-click on users and select new
![add user flow](/lab02_image-7.png)

After creating, you can delegate groups by:
![set group menu](/lab02_image-8.png)

Both are similar to the Control Panel flow with local users.

## Prepping wks01 for AD
Make sure that DNS for wks01 is ad01
![Adapter settings for wks01](/lab02_image-9.png)

Changing AD:
![whoopie](/lab02_image-10.png)

## Deliverable 1
![it's here!](/lab02_image-11.png)

## Deliverable 2
![AD accounts](/lab02_image-13.png)

## Deliverable 3
![powershell command output](/lab02_image-12.png)