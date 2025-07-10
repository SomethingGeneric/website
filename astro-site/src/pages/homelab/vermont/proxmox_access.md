---
layout: /src/layouts/MarkdownLayout.astro
title: "Proxmox Access"
---
# Accessing Proxmox

URL: https://pve.mattcompton.dev/

Username and password should be sent

![pve credentials page](/public/images/pve_login.png)

Make sure to change the `Realm` to `Proxmox VE auth server`.

Your VM is probably under `pve2`, and you likely have to click dropdowns to get to it.

You *should* have full access to make any changes to the node.

The interface for your VM should look like this

![pve vm view](/public/images/pve_vm_view.png)