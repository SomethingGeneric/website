---
layout: /src/layouts/MarkdownLayout.astro
---
# Lab 3.2 - Wazuh

## Setting up Wazuh
Installing Wazuh is very easy, as there's a bash install script:
```
curl -sO https://packages.wazuh.com/4.3/wazuh-install.sh # for this lab,  I used 4.7, which meant simply modifying the version in the URL
# inspect the installer if you'd like
sudo bash ./wazuh-install.sh -a -i # where "-a" means combined install (all Wazuh components on the same box), and "-i" is to ignore system requirements, as our class VMs are a little too light on RAM in Wazuh's opinion
```

## Installing Agents
Installing agents is easy on supported platforms, as the "Deploy new agents" screen, which you can get to easily from the main dashboard by clicking "agents" and then the plus icon, will generate install scripts for every supported platform.

## Where's Wazuh stuff?
Wazuh's files live in `/var/ossec` on both the agents and the manager