---
layout: /src/layouts/MarkdownLayout.astro
---
# Lab 03 - Git + Linux
## Things I didn't really know
* I think the reason my `secure_ssh.sh` script creates users with just a `$` prompt is because I probably missed a flag for `useradd`. I should probably have read my own [CentOS Notes](../../../centos-commands.md) better.

## Things I did
* Since my techjournal repo is basically just the markdown pages that create this website, and I don't think I would necesarily need this particular SSH key or script, I put the `linux/{centos,public-key}` stuff into the Git repo made specifically for my Docker project, which you can find [here](https://git.goober.cloud/matt/forgejo-docker-stack)
* On the off-chance that I do ever decide to reuse the script, I used `curl` within it to grab the pubkey, rather than assume that the user has `git` and has pulled the whole repository. This also makes more sense in my mind because the user might not actually *want* all the Forgejo docker compose stuff. (Although, I do think it is pretty rad)