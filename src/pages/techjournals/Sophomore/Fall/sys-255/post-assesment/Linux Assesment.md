---
layout: /src/layouts/MarkdownLayout.astro
---
# Linux Assesment
Basically re-creating web01 and adding some kind of PHP based blog service
WordPress in my case

## Prereqs
1. Set up your IP, gateway, DNS in `nmtui`
2. Ensure hostname is `blog01-you`
3. I rebooted for good measure

## Steps

### Apache
```
yum install -y httpd
firewall-cmd --permanent --add-port=80/tcp
firewall-cmd --permanent --add-port=443/tcp
firewall-cmd --reload
systemctl enable --now httpd
```

### PHP 7 (wordpress requires, CentOS packages 5 by default)
```
yum install -y yum-utils epel-release
yum install -y http://rpms.remirepo.net/enterprise/remi-release-7.rpm
yum-config-manager ––enable remi–php73 # be careful with this line, as clipboard sometimes nukes the --
yum install php php-common php-opcache php-mcrypt php-cli php-gd php-curl php-mysql –y
```

### MySQL
```
yum install -y mariadb-server
systemctl enable --now mariadb
```

### Wordpress
```
yum install -y wget unzip nano
wget https://wordpress.org/latest.zip
unzip latest.zip
rm -r /var/www/html # im lazy
mv wordpress /var/www/html
# make mysql db
mysql -u root
# in SQL prompt:
CREATE DATABASE <something>;
GRANT ALL ON <something>.* to 'username'@localhost identified by 'apassword';
FLUSH PRIVILEGES;
exit;
# END SQL
setenforce 0 # SELinux can suck my nuts
chown -R apache:apache /var/www/html
cp /var/www/wp-config-sample.php /var/www/wp-config.php
nano /var/www/html/wp-config.php
# fill in SQL details (db name, user name, password)
systemctl restart httpd
# browse to http://your_ip and set up wordpress!
# not sure what else Joe might want from us
```

### AD join
```
yum install -y realmd samba samba-common oddjob oddjob-mkhomedir sssd
realm join --user=your-domain-admin-username@yourdomain.local yourdomain.local
# show proof:
realm list
```