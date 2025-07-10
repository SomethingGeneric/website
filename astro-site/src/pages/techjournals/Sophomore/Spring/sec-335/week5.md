---
layout: /src/layouts/MarkdownLayout.astro
---
# Week 5 (Class on 2/19/24)

## Password Cracking Bios - Notes

### Tool Notes
* CEWL was fairly straight forward. You simply point it at the target URL
    * I took it another step up and ran the pages per user like
    ```bash
    for man in frodo pippin bilbo samwise; do
        cewl http://10.0.5.21/bios/$MAN > $MAN.words.txt
    done
    ```
* rsmangler was also pretty straight forward, once I got a hint from fellow classmates that a couple specific words were imporant LOTR references.
    * As with cewl, I am lazy so I once-again used a for-loop to generate my mangled wordlists
    ```bash
    for man in frodo pippin bilbo samwise; do
        rsmangler --file $man.small.txt -x 12 -m 9  -l -s -e -i -p -u  -a --output $man.mangled.txt
    done
    ```
* Hydra was actually very easy to use for both HTTP post and SSH. The only thing that tripped me up was that I didn't realize the form was a GET, and I was breifly confused why my attempts to use the HTML form post module didn't work.

### Problems Encountered
* I don't know LOTR lore. I guess it's a good simulation of real-world, where you might not be able to identify what elements of someone's public facing profile could (or could not) be part(s) of their credentials. It made the brute-forcing more challenging, as I didn't know what keywords from the bio pages are hints.
* Hydra over SSH is stupid slow. Didn't end up mattering once I resolved the above issue, as it significantly shorted my password files.