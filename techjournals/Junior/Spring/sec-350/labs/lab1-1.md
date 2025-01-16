# Lab 1.1

IP Assignment Sheet: https://docs.google.com/spreadsheets/d/1QfUMFhFyiDqfvJU24Fav5s71LYY_LKGA/edit?gid=2000835468#gid=2000835468

## rw01-matt
* Changed `champuser` password
* Added `sudo` user `matt`
* Set IP with `nmtui` (netplan makes me sad)
* Set hostname with `hostnamectl set-hostname`

## fw01-matt

### Changing user password
```
configure
set system login user vyos authentication plaintext-password PasswordGoesHere
commit
exit
```
https://support.vyos.io/support/solutions/articles/103000096301-set-change-the-password-of-a-user

### Changing hostname
```
configure
set system host-name fw01-matt
commit
save
exit 
```

# TODO: make github repo and dump vyos config

## web01-matt

* Changed root password
* Made `matt` sudo user, set password
* Set IP address, DNS, etc
* IP on DMZ: `172.16.50.3`

## log01-matt

* Same steps as web01-matt
* IP on DMZ: `172.16.50.5`