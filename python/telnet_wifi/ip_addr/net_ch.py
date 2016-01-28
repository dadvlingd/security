#!/usr/bin/python
#-*- coding UTF-8 -*-

import netaddr

with open("chinanet.txt", "r") as f:
    for line in f:
        ip = line.strip().split()
        prx = netaddr.IPRange(ip[0], ip[1]).cidrs()[0].prefixlen
        print(ip[0] + '/' + str(prx))
