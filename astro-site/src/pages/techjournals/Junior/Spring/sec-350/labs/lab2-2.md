# Lab 2.2

## Including authpriv events in rsyslog
In your client config, ensure you add:
```
user.notice @172.16.50.5:514
# New (vv)
authpriv.* @172.16.50.5:514
```

## Drop-in config for log01
Instead of modifying `/etc/rsyslog.conf`, we created `/etc/rsyslog.d/03-sec350.conf`:
```
module(load="imudp")
input(type="imudp "port="514" ruleset="RemoteDevice)
template(name="DynFile" type="string"
    string="/var/log/remote-syslog/%HOSTNAME%/%$YEAR%.%$MONTH%.%$DAY%.%PROGRAMNAME%.log"
)
ruleset(name="RemoteDevice"){
    action(type="omfile" dynaFile="DynFile")
}
```

And, make sure to re-disable the base rsyslog listening on port 514 (in `/etc/rsyslog.conf`)

## VyOS syslog
(See the VyOS reference sheet at the top level of techjournals)