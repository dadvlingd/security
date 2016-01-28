#!/usr/bin/python
#-*- coding:UTF-8 -*-

file = open("ip_addr/chinanet.txt", "r")
while True:
    line = file.readline()
    if line:
        line = line.split()
        print line[0]
        print line[1]
    else:
        break
file.close()
