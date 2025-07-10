---
layout: /src/layouts/MarkdownLayout.astro
---
# Week 7 (Class on 3/4/24)

## Exploiting Pippin (7.1) Notes
This lab was really interesting, but also I think (hope) a little unrealistic.
I've deployed `vsftpd` myself before, so I know just how many things you'd have to do wrong in order to have the problems that we saw with it in this lab.

Somehow, the vsftpd root directory was set to `/var/www/html`, which is also Apache's root directory. This allowed us to upload files of our choosing to `upload/` which was a directory that Apache would also happily serve back to us. I found a CMD web shell on the internet, which I put in that directory, and then Apache/PHP were happy to run any commands of my choosing as the Apache user.

To get into the `peregrin.took` user, I found the MediaWiki settings file in the `/var/www/html` directory, and found the SQL password by `grep 'password' LocalSettings.php` after downloading the file via FTP. It just so happened that the root SQL passwowrd was also the password for this account.

To get into the Pippin user on MediaWiki, after being able to SSH as `peregrin.took`, I used the SQL prompt with the above discovered password, and then dumped the hash of the user's password.

```sql
use mediawiki;
select * from users;
```

Cracking this hash with hashcat was actually fairly straight-forward thanks to the [fourm post](https://forum.hashkiller.io/index.php?threads/25-reward-need-help-in-formatting-modifying-mediawiki-pbkdf2-sha512-hashes.32787/). The only trick was to remove the `:64:` from the dumped hash, and then it "just worked" with my Nvidia GPU and the flags documented in the above fourm post. The link that lead me to removing that noted `:64:` was this [list](https://hashcat.net/wiki/doku.php?id=example_hashes) of hashcat's supported formats (specifically `PBKDF2-HMAC-SHA512`, in our case.)