---
layout: /src/layouts/MarkdownLayout.astro
---
# Lab ??? - Ansible
## Pain Points
* The webmin role by semuadmin didn't work. I used a playbook I manually pieced together instead. You can see it [here](https://git.goober.cloud/matt/sys265-ansible/src/branch/main/webmin.yml)
* I found a working role for the lovely web landing page [Dashy](https://github.com/Lissy93/dashy), but it didn't pull in it's own NodeJS role, and all the ones I tried from Galaxy didn't work. So, I manually installed NodeJS 16.x using NodeSource, like:
```
curl -fsSL https://rpm.nodesource.com/setup_16.x | bash -
yum install -y nodejs
```
And then ran [this playbook](https://git.goober.cloud/matt/sys265-ansible/src/branch/main/dashy.yml)
* Getting Windows SSH server to work was a pain point for the whole class, just like the webmin role, but it worked flawlessly with Ansible once jeastman discovered we couldn't use `Add-WindowsCapability` because the Windows Update service was off *facepalm*.