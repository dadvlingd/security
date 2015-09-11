#!/usr/bin/env python

import urllib2
import re
from urllib2 import HTTPError
import urllib
import os

mmurl = "http://jandan.net/ooxx/page-"
#mmurl = "http://www.mm8mm8.com/sexy/p"
ph = -1
temp = '''<img src="'''
ri = 0

def downImage(pic_url, name):
    localPath = "/home/hakits/Downloads/domm" + name + ".jpg"
    try:
        request = urllib2.Request(pic_url)
        request.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36")
        response = urllib2.urlopen(request, timeout = 4)
        f = file(localPath, "wb")
        f.write(response.read())
        f.close()
    except HTTPError:
        pass

def getImg(html):
    reg = r'(?<=src=")http://.*?.jpg'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html) #get every page url list
    for imgurl in imglist:
        print imgurl
        os.system("wget " + imgurl)
        
        #downImage(imgurl, imgurl.split('/')[-1])

        
if __name__ == '__main__':
    os.chdir("/home/hakits/Downloads/domm")
    os.system("rm -rf *")
    for i in range(1501, 1529):      #get every one url
        url  = mmurl + str(i) + '#comments'
        request = urllib2.Request(url)
        request.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36")
        response = urllib2.urlopen(request)
        cont = response.read()
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


