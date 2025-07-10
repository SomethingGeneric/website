---
layout: /src/layouts/MarkdownLayout.astro
---
# Assignment: Linux File Permissions

## This assignment involved editing my [CentOS Reference](/techjournals/centos-commands.md)

## Requirements
* Make users:
    * bob
    * alice
    * fred
* Make groups:
    * management
    * marketing
* Add users to groups:
    * alice -> management
    * fred -> marketing
    * bob -> marketing
* Make directories
    * `/marketing`
    * `/management`
* Ensure that only `management` can access `/management`
* Ensure that only `management` can view/edit `/management/bobreview.txt`
* Ensure that fred can edit `/marketing/newproducts.txt`, and bob can view it.

## Making users
Fundamentally, adding users is just `useradd <name>`, but I'm lazy, so I did:
```bash
for u in bob alice fred; do
    useradd $u
done
```

## Making groups
Like before, the fundamental command is `groupadd <name>`, but I'm ✨special✨ so I did:
```bash
for g in management marketing; do
    groupadd $d
done
```

## Adding users to their groups
To add a user to a group you can `usermod -aG <group> <user>`
So, for this lab:
```bash
usermod -aG management alice
for u in bob fred; do
    usermod -aG marketing $u
done
```

## Making directories
This part is simple. 
```bash
mkdir /marketing
mkdir /management
# i guess there is a limit to when I'll use a one-line for loop
```

## Permissions for Management directory
I made the sample review file `/management/bobreview.txt` per lab instructions, then:
```
chown alice:management /management/bobreview.txt
chmod -R 770 /management
```

This sets the directory (and items under it) as read+write+execute for alice (as the owner), and members of management (as the owning group), and no perms for others. (Permission ints make my head hurt, you can always use a calculator [like this one](https://chmod-calculator.com/), or use the symbolic modes [reference](https://docs.oracle.com/cd/E19683-01/816-4883/6mb2joat8/index.html))

## Permissions for Marketing directory
Marketing was fairly simple, as the lab is ok with alice and other users having view permissions of the dir
My solution was (after doing `touch /marketing/newproducts.txt` as root):
```
chown fred:marketing /marketing/newproducts.txt
```
The file already had owner+group rw, so it remained after ownership transfered.

## Deliverable 1
![outputs](/public/images/permslab_deliverable1.png)