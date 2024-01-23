# IO Lab

(Not the whole doc, but the command used in the lab)

```
24  sudo apt install iotop htop -y
25  sudo iotop
26  cat /proc/ioports
27  clear
28  cat /proc/ioports
29  sudo apt install sysstat -y
30  iostat
31  clear
32  sudo apt install ioping -y
33  sudo apt autoremove -y
34  clear
35  ioping -c 12 .
36  clear
37  sudo apt install sysbench -y
38  sysbench --test=memory --memory-block-size=1M --memory-total-size=10G run
```
