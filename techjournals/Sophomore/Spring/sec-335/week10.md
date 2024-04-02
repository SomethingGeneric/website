# Week 10 (Class on 4/1/24)

## Hunting SUID and publicly writeable files (class activity 10.1)

In my case, I just did `/` for `/<dir>` below.

To find all suid execs on the system (without root, so you can live off the land etc):
`find /<dir> -perm /u=s,g=s 2>/dev/null` (piping away errors not required, but nice since so many `/proc` and `/sys` matches etc)

To find files that are publicly writeable:
`find /<dir> -perm /o=w 2>/dev/null` (once again, recommend to get rid of errors, because of psuedofilesystems being silly)

## Nancurinir Reflection (10.2)
In terms of techniques and tools, this week's target was compromised using things we had seen before.

The unique thing about this target was that it only exposed the Apache server, which didn't have any *useful* CVE's for it.

However, using `dirb` revealed a phpmyadmin, who's credentials were the username made obvious by the main Apache page, and the password was, as hinted, within the text of the page itself.

In the phpmyadmin, I was able to grab the password hash for the MySQL root user, which when reversed on CrackStation, was obviously the password for the Linux user `gandalf`.

So, I then used a revshell thru the compromised phpmyadmin to log in as `www-data`, and then pivot to `gandalf`, and finally to `root`, as `gandalf` was a sudoer.
