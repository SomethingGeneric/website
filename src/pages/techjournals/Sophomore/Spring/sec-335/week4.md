---
layout: /src/layouts/MarkdownLayout.astro
---
# Week 4 (Class on 2/12/24)

## Exploiting Cupcake - Notes
1. How you determined the versions of the two services exposed by cupcake

    Luckily, the version of services running on cupcake were found simply by the nmap scan.

2. How you dealt with parsing nmap result with nmaptocsv

    nmaptocsv worked just fine as documented.

3. The techniques you used to invoke remote code execution

    Invoking RCE on cupcake was using the `/status` page which is a CGI script hosted by apache.
    I used `nmap` syntax and a `--script` argument, or `curl` syntax like the below, rather than the code listed on the CVE's [exploitdb](https://www.exploit-db.com/exploits/34900) page.

    ```bash
    RUN_ON_HOST="cat /etc/issue"
    curl -H "User-Agent: () { : ; }; echo; $RUN_HOST" http://10.0.5.23/cgi-bin/status
    ```

4. The generation of a list of passwords and subsequent ssh bruteforce

    The creation of a wordlist and usage of hydra worked fine as in the documentation.

5. Transfer of files using python and wget or any other mechanism you chose

    I mostly used `scp` once I had the SSH password. I managed to not need to move files to the host with the CGI rce.

6. Compiling and running a privilege escalation exploit (It can be different than the demo!)

    The instructions in the [Dirty Cow](https://www.exploit-db.com/exploits/40839) exploit worked just as described.

## Exploiting Cupcake - Reflection
The big learning experience for me is that a user which doesn't have that many permissions could still see `/etc/passwd`, and thus you can easily get valid usernames, even with a fairly well-sandboxed service.

Of course, in the real world, we wouldn't be able to guess that the password to a found account would be in the default `rockyou` without any permutation.

Overall, the tools used in this activity were mostly ones I had used before, but I wouldn't have considered the overall path that took us from 0 - pwn.