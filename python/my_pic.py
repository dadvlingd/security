#!/usr/bin/env python

import urllib2
import re

mmurl = "http://www.mm8mm8.com/xiurenmote/list_"
i = 1
ph = -1
temp = '''<img src="'''

def getImg(html):
    reg = r'(?<=href=")http://.*?(?=" targe)'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    for imgurl in range(0, len(imglist), 2):
        print imglist[imgurl + 1]

while i <= 1:
    url  = mmurl + str(i) + ".html"
    i += 1
    #print url
    up = urllib2.urlopen(url)
    cont = up.read()
    getImg(cont)
    '''
    #print cont
    head = "<img src="
    tail = ".jpg"
    ph = cont.find(head)
    pj = cont.find(tail, ph + 1)
    #print cont[ph + len(temp) : pj + len(tail)]
    ahref = <li><a href=" #there have three '
    target = "target"
    pa = cont.find(ahref)
    pt = cont.find(target, pa)
    #print cont[pa + len(ahref) : pt - 2]
    moduleurl = cont[pa + len(ahref) : pt - 2]
    mup = urllib2.urlopen(moduleurl)
    mcont = mup.read()
    print mcont
    '''


