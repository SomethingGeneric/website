# Week 6 (Class on 2/26/24)

## Password Hash Cracking Notes (6.1)
* Grabbing hashes:
    * `cat /etc/shadow` (from root or with `sudo` or `doas`)
    * Or better: `cat /etc/shadow | grep -v '!\*'`
* Breakdown of `/etc/shadow` entries:
    * Example: `galadriel:$6$poPWvLT/CfA/sxS/$lHbu1oMqRV2aM18fkFPbJw25U2.POqhonSmaUpbzPIPVKl2IxS86Qq8q9v3fYu5Y6qlWwbmqekbL3g1vtPmlQ/:19143:0:99999:7:::`
    * Fields are seperated by `:`
    * First is username
    * Second is password hash, which has 3 sub-fields
        1. Hash algorithm. `$6` in this case
        2. Salt. `$poPWvLT/CfA/sxS/` in this case.
        3. Salt + Password: `$lHbu1oMqRV2aM18fkFPbJw25U2.POqhonSmaUpbzPIPVKl2IxS86Qq8q9v3fYu5Y6qlWwbmqekbL3g1vtPmlQ/`
    * And the ones after password we don't really need for this use-case
* Usage of `unshadow`
    * Unshadow turns a shadow file and passwd file into a combined file for tools like `hashcat` and `john`
    * Usage is very straight-forward: `unshadow passwd_file shadow_file > output_file`
* I gave up trying to use John because it didn't want to use my GPU
* Hashcat made life so easy.
    * It auto-detected my NVIDIA card when I ran `hashcat -I`
    * Cracking was very easy, with just:
        `hashcat -m 1800 -a 0 -o output_file_name unshadow_file_name path_to_wordlist_file`
* We're lucky that this old box has SHA-512, which I figured out from [this page](https://www.cyberciti.biz/faq/understanding-etcshadow-file/)

## Password Hash Cracking Reflection (6.1)
This assignment was really fun. Getting to use the tools that Kali has to grab other accounts from the bios box was super interesting to me.

The most challenging part was the amount of time I spent trying to get JtR to accept my NVIDIA GPU, which, I never was successful with. I also never bothered using hydra or john on the Kali VM, given the lack of output from running CPU-bound on my 16-core AMD Ryzen 7, I knew that vCenter would be hopeless.

Once I piped the magic arguments to hashcat, though, it took only about 5 minutes to get all three accounts that I didn't have previously.

I can totally understand the push for password managers, now, as I bet it would take ages (if it's even possible) to crack the 20+ character, randomized nonsense that are most of my personal passwords.