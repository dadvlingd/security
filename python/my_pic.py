#!/usr/bin/env python

import urllib2
import re
from urllib2 import HTTPError
import urllib

mmurl = "http://www.mm8mm8.com/sexy/p"
i = 1
j = 4
ph = -1
temp = '''<img src="'''
ri = 0

def downImage(pic_url, name):
    localPath = "/home/hakits/Downloads/" + str(name) + ".jpg"
    try:
        request = urllib2.Request(pic_url)
        request.add_header("User-Agent", "fake-client")
        response = urllib2.urlopen(request, timeout = 4)
        f = file(localPath, "wb")
        f.write(response.read())
        f.close()
    except HTTPError:
        pass

def getImg(html):
    reg = r'(?<=href=")http://.*?(?=" targe)'
    i = 0
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html) #get every page url list
    for imgurl in range(0, len(imglist), 2):
        #print imglist[imgurl + 1]
        gir_url = urllib2.urlopen(imglist[imgurl + 1])
        context = gir_url.read() #this include all pic link
        gir_reg = r'(?<=src=").*(?=\d{1,2}.jpg)'
        gir_com = re.compile(gir_reg)
        gir_pic_list = re.findall(gir_com, context)
        for gir_pic in gir_pic_list:
            print gir_pic
            '''for i in range(1, 16):
                global ri
                #urllib.urlretrieve(gir_pic + str(i) + ".jpg",  str(ri) + ".jpg")
                downImage(gir_pic + str(i) + ".jpg", ri)
                ri += 1'''
        #print context

        
while j <= 8:      #get every one url
    url  = mmurl + str(j) + ".html"
    j += 1
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


