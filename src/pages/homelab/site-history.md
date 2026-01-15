---
layout: /src/layouts/MarkdownLayout.astro
title: "Portfolio Site History"
---

# Portfolio Website History
I've had numerous iterations of a portfolio website. The very first one, unfortunately, I believe is lost to time (and my very first server along with it)

## Site 1 - xhec.us
A static website created and hosted on my mom's old HP work PC tower that I had loaded with Ubuntu (I belive 16.04, and kept upgrading for a while)
(I wish I still had the origional repo of that, and/or any docs about how long that particular server lived. As I last knew, it lived on with my friend Ethan from HS, as a minecraft server)

## Site 2 - xhec.dev v1
A better static website that my friend Kris helped me build. I also stole the CSS for the very first Crystal Linux website (which was also on my mom's old work PC lol), which I can probably find a link to (`#TODO`).

## Site 3 - xhec.dev v2
I eventually decided that manually editing pure HTML with no framework at all was too much work, so I began looking for solutions. That's when I first encountered the idea of a static site generator. I had previously written web-apps and other things with scripting languages like Python, but I felt like having a live daemon would be overcomplicated for a site that was (and mostly still is!) just serving static content. So, when I saw that Jekyll would let you write Markdown files, and template files for appearence, and combine them in a programatic way so that I didn't have to, say, keep copying a navbar HTML snippet between files, that was a no-brainer.

I think at this point it was still (mostly?) hosted on my own infrastructure, though for a while it was also on GitHub pages.

## Site 4 - mattcompton.dev v1
During my first year at Champlain College, one of the professors, Devin, showed us (or rather, in my case, another professor linked to ) his portfolio site, using a different static site generator called Docusaurus. It's a Node.js framework that aims to be even less overhead than something like Jekyll, and was built by FB (Meta?) to allow their developers to have an easier time of documenting their projects (maybe only OSS ones?) without worrying about styling, browser compat, etc. 

Given that I was really tired of Jekyll tomfoolery (especailly as someone who had never (and still has not) used Ruby), it seemed like a cool thing to try. So I did!

This site was also on the old MD servers for a while (I need to setup a "history" section for my former homelab stuff, tbh), then on GitHub Pages, and then once I moved off-campus in Burlington, finally on my IBM servers in my apartment.

## Site 5 - mattcompton.dev v2
After having used Docusaurus for a while, I got the bug to do some fun custom stuff again, so I was poking around at other Node.js-esque static site options, and found Astro. It does very little hand-holding, especially given that I have only very basic JS knowledge, but it still lets me write most pages in Markdown, and even on the occasion that I have to write a `.astro` page, it's fairly straight forward.

The site *has* changed a bunch even in this current iteration, but it's mostly been related to making switchable themes, having auto-CI rebuilds to update things that then "appear" to be dynamic to the end user, like the tagline on the main page. 

## That's all folks.
I've been happy with Astro since (last fall, as of me writing this in fall 2025), so I doubt I'll be totally throwing it out anytime soon. Plus, with Mend Renovate's bot running on my GitLab, handling Node.js and Astro updates, maintenence on my end is basically non existent, except for me creating content obviously.