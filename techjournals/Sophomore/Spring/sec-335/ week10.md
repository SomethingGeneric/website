# Week 10 (Class on 4/1/24)

## Hunting SUID and publicly writeable files (class activity 10.1)

In my case, I just did `/` for `/<dir>` below.

To find all suid execs on the system (without root, so you can live off the land etc):
`find /<dir> -perm /u=s,g=s 2>/dev/null` (piping away errors not required, but nice since so many `/proc` and `/sys` matches etc)

To find files that are publicly writeable:
`find /<dir> -perm /o=w 2>/dev/null` (once again, recommend to get rid of errors, because of psuedofilesystems being silly)