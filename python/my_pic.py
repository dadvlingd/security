#!/usr/bin/env python

import urllib2

mmurl = "http://www.mm8mm8.com/xiurenmote/list_"
i = 1
ph = -1
temp = '''<img src="'''
while i <= 1:
    url  = mmurl + str(i) + ".html"
    i += 1
    #print url
    up = urllib2.urlopen(url)
    cont = up.read()
    #print cont
    head = "<img src="
    tail = ".jpg"
    ph = cont.find(head)
    pj = cont.find(tail, ph + 1)
    #print cont[ph + len(temp) : pj + len(tail)]
    ahref = '''<li><a href="'''
    target = "target"
    pa = cont.find(ahref)
    pt = cont.find(target, pa)
    #print cont[pa + len(ahref) : pt - 2]
    moduleurl = cont[pa + len(ahref) : pt - 2]
    mup = urllib2.urlopen(moduleurl)
    mcont = mup.read()
    print mcont


