# Lab 2.1 - Standardizing rsyslog time

To edit rsyslog so that it will report full (and actually useful) timestamps, you simply need to edit `/etc/rsyslog.conf`.

On CentOS 7 and Xubuntu 22.04, you only need to comment out this line:
```
# Use default timestamp format
$ActionFileDefaultTemplate ...
```

Rocky Linux is slightly different, but also trivial. 
Comment out this line:
```
# Use default timestamp format
module(load="builtin:omfile" ...)
```

