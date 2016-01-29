#!/usr/bin/python
#-*- coding=UTF-8 -*-

#将所有IP段合并为一个文件
#awk '{print $1,$2}' *.txt | sort | uniq > ip.txt

import netaddr

with open("chinanet.txt", "r") as f:
    for line in f:
        ip = line.strip().split()
        prx = netaddr.IPRange(ip[0], ip[1]).cidrs()[0].prefixlen
        print(ip[0] + '/' + str(prx))
