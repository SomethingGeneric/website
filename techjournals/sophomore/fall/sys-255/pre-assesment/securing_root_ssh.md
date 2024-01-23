# Securing SSHD
To prevent root access

The SSHD (ssh-daemon) config file is typically located at `/etc/ssh/sshd_config` on most linux systems (like the CentOS boxes used for this class!)

There are many options in the file, but only one we're interested in right now:
``` title="/etc/ssh/sshd_config"
...
# PermitRootLogin yes
...
```

To ensure that it is completely impossible to log in as root, simply change it to:
``` title="Modified /etc/ssh/sshd_config"
...
PermitRootLogin no
...
```

Then, we need to restart the SSHD service. On CentOS, this is as easy as `sudo systemctl restart sshd`