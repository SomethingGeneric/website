---
layout: /src/layouts/MarkdownLayout.astro
---
# Lab 05: ADDS

## Step 1:
In "AD Users and Computers" (from Server Manager), right click on domain and "new" -> "OU", make one called `SYS255`

## Step 2:
In the OU made above, add `Accounts`, `Groups`, `Computers`

## Step 3:
In the new `SYS255\Accounts` OU, make users `Alice`, `Bob`, `Charlie`

Note: typically, enabling the tickbox for "change password on next login" is important, but we can skip it here.

## Step 4:
Move the `wks01` box from the default `Computers` OU to the `SYS255\Computers` OU that you just made (this is literally just a drag-n-drop)

## Step 5:
Create a group `custom-desktop` under `SYS255\Groups`, and ensure the defaults are still `global group` and the group type is `security`

## Step 6:
Add the new `Bob` and `Alice` accounts to the group via right-click, properties. (Don't add Charlie!)

## Step 7:
Launch Group Policy from Server Manager, click drop-downs to find your `SYS255` OU.

Make a new GPO by right-clicking on the `SYS255` entry, and name it `sys255-desktop`

## Step 8:
In the new object's window, under security filtering, add the `custom-desktop` group from the `SYS255\Groups` OU that was made earlier.

Remove the `authenticated users` item from the filter.

## Step 9:
Add `YOURDOMAIN\Domain Computers` to the filter as before.

## Step 10:
Go to delegation tab, advanced settings.

Select the `Domain Computers` object, untick it's `Apply Group Policy` allow, and set deny.

## Step 11:
Right click on `sys255-desktop`, and hit edit. This spawns a new window.

In the Policy Editor, drop down `User Configuration\Policies\Administrative Templates\Desktop` to find the `Remove Recycle Bin icon from desktop` item.

## Deliverable 1:
A screenshot of logged-in desktop as `alice@yourname.local` on `wks01` with NO recycle bin icon.

## Step 12:
As in step 7, make a new GPO called `DisableLastLogin`, and add `YOURDOMAIN\Domain Computers` to the filter

## Step 13:
Right-click and edit `DisableLastLogin`, so you can drop-down `Computer Configuration\Policies\Windows Settings\Security Settings\Local Policies\Security Options`, and then scroll to `Interactive logon: Don't display last signed-in`, and enable it.

## Step 14:
Sign in to `wks01` as your domain admin account, and then:
```ps
gpupdate /force
gpresult /scope computer /r 
```

## Deliverable 2
Screenshot of the second command above.

## Deliverable 3
Screenshot of the login screen where there are no longer any usernames visible

## Resources:
I goofed u pwhile adding an OU, enabling detailed view was required to follow these steps and fix the typo:
https://petri.com/delete-protected-ou-active-directory/#:~:text=The%20process%20to%20delete%20a,deletion%2C'%20then%20click%20OK.