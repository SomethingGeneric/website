---
layout: /src/layouts/MarkdownLayout.astro
---
 
# Milestone 7 - HyperV Linked Clones and Automation

Compared to PyVmomi, Hyper V + Powershell was a world better.

Which is a weird thing for me to say, given that I almost always default to Python when picking a language. 

Pyvmomi is just such an awful API.

Given that Hyper-V is a MS product, and so is PowerShell, I suppose it shouldn't suprise me that the PS extensions for it are easy to use, and mostly self-explanatory.

For example, if I want to stop a VM, I simply run `Stop-VM 'vmNameGoesHere'` it's glorious!

So thus, even for a "hard" task like making a linked clone (which is only really hard since it's not natively supported), my PowerShell script is only 31 lines.

Script: https://github.com/SomethingGeneric/sys350/blob/main/hyperv/linkedclone.ps1

To make this script, I just ran one-off commands in the PowerShell session, wheras with pyvmomi I just wrote the code and prayed, because setting up a temporary session in something like ipython seemed like way too much work.