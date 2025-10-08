---
layout: /src/layouts/MarkdownLayout.astro
---
 
# Milestone 5 - Automation Pt 1

This milestone was interesting.

Python has been my go-to language for years, but the py interfaces for vCenter/ESXi are kind've a pain in the ass IMO.

Everything is a nested class with properties, which makes debugging w/o something like iPython a bit of a pain.

For example, my function to search for all VMs that match a name:
```py
def get_vms(service_instance, vm_name=None):
    """
    Searches for VMs by name, returning all VMs if no name is provided.
    """
    content = service_instance.RetrieveContent()
    container = content.rootFolder
    view_type = [vim.VirtualMachine]
    recursive = True
    container_view = content.viewManager.CreateContainerView(container, view_type, recursive)

    vms = []
    for vm in container_view.view:
        if vm_name is None or vm_name.lower() in vm.name.lower():
            vms.append(vm)
    container_view.Destroy()
    return vms
```

Why do I need a new "container view" object???


Anyways, the main thing that I struggled with wasn't actually the [code implementation](https://github.com/SomethingGeneric/sys350), but rather in getting VM tools instaled on my pfSense box.

I knew of `open-vm-tools` already (and thank god, the vCenter/ESXi ones seem really old, which is weird, given that iirc we're on pretty-close to current versions of both??), but my pfSense box just wouldn't let me use `pkg`. 

Thankfully, when searching the internet for the `missing library` error I was encountering, I found [this reddit thread](https://www.reddit.com/r/PFSENSE/comments/18ll0la/cannot_pkg_update_it_says_ldelfso1_shared_object/), which then got `pkg` to work, and installing `pfSense-pkg-Open-VM-Tools` (apologies if I spelled this slightly wrong, just do `pkg search open-vm`, and you'll find it) went off just fine, and one reboot later, I had my last IP showing in my python program.
