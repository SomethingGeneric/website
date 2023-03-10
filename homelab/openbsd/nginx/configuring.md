# Configuring

Like on Linux, OpenBSD puts the config in `/etc/nginx` not some weird place like FreeBSD

They do not create a `sites-enabled` directory by default, so you have to `mkdir -p /etc/nginx/sites-enabled` and then add a code block to the http block of `nginx.conf`

```
include sites-enabled/*.conf;
```

They had a very nice pre-commented `nginx.conf`, which I would end up needing later, as EFF's certbot doesn't support auto-config deployment like on Linux.

However, copying from the default SSL config example that OpenBSD ships and adding the paths to files that Certbot so kindly spit out worked just fine.

I did also have to modify one final bit of the config:

```
server {
    listen       443; # change '443' to '443 ssl'
    server_name  localhost;
    root         /var/www/htdocs;
    
    ssl                  on; # remove this line
    ssl_certificate      /etc/ssl/server.crt;
    ssl_certificate_key  /etc/ssl/private/server.key;
    
    ssl_session_timeout  5m;
    ssl_session_cache    shared:SSL:1m;
    
    ssl_ciphers  HIGH:!aNULL:!MD5:!RC4;
    ssl_prefer_server_ciphers   on;
}
```

