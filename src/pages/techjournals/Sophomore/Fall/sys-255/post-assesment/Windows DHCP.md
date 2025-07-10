---
layout: /src/layouts/MarkdownLayout.astro
---
# Setting up Windows DHCP Server
* In the Server manager, add DHCP as a role for your preferred server
* If the machine for the DHCP server is a minimal setup (no GUI), add the "feature" for "Remote Server Administration" -> "DHCP Server Tools"
* Connect to the target machine in the DHCP tools window
* Create a scope
* Set options

## Or if you're feeling brave:
You can use Powershell on the target machine following this guide: https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/quickstart-install-configure-dhcp-server?tabs=powershell

I couldn't fidnd a good reference for the `-OptionId` fields, so I gave up and used the GUI to set the default gateway of my scope.