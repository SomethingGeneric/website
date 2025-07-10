---
layout: /src/layouts/MarkdownLayout.astro
---
# Lab 02 - Docker
## Things I didn't already know / suffered with
* The documentation for [Netplan](https://netplan.readthedocs.io/en/stable/examples/#how-to-configure-a-static-ip-address-on-an-interface) is pretty good, but I had a couple of specific pain points:
    * They deprecated `gateway4`, so you have to use a `routes` block like
        ```yaml
            routes:
                - to: default
                  via: <gateway_ip>
        ```
* Adding a `sudo` user was only different because the group is called `sudo` instead of `wheel`
    * This means `usermod -aG sudo <your_user>` instead of `usermod -aG wheel <your_user>`
    * You should maybe still also be in `wheel` too, since I believe it's eval'd for `su`

## Docker commands
* `docker run` - create a container based on a template (imo not as useful as compose stacks)
* `docker compose <up,down,build>` - create or destroy a stack based on a `docker-compose.yml`
    * NOTE THE SPACE `docker compose` vs `docker-compose`. The latter is a deprecated version that would require a seperate package install.
* `docker pull` - pull an image from dockerhub (premade containers/containerized apps)
