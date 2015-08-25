#!/usr/bin/env python

import urllib2
import re
from urllib2 import HTTPError

mmurl = "http://www.mm8mm8.com/xiurenmote/list_"
i = 1
ph = -1
temp = '''<img src="'''

def downImage(pic_url):
    localPath = "/home/hang/Downloads/" + str(imgurl) + ".jpg"
    try:
        request = urllib2.Request(imglist[imgurl + 1])
        request.add_header("User-Agent", "fake-client")
        response = urllib2.urlopen(request)
        f = file(localPath, "wb")
        f.write(response.read())
        f.close()
    except HTTPError:
        pass

def getImg(html):
    reg = r'(?<=href=")http://.*?(?=" targe)'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html) #get every page url list
    for imgurl in range(0, len(imglist), 2):
        print imglist[imgurl + 1]
        gir_url = urllib2.urlopen(imglist[imgurl + 1])
        context = gir_url.read()
        print context

        
while i <= 1:      #get every one url
    url  = mmurl + str(i) + ".html"
    i += 1
    print url
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


