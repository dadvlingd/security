#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
from urllib2 import HTTPError
import urllib
import time
import os

def downImage(pic_url, name):
    localPath = "/home/hakits/Downloads/path_pic/" + str(name)
    try:
        request = urllib2.Request(pic_url)
        request.add_header("User-Agent", "fake-client")
        response = urllib2.urlopen(request, timeout = 4)
        f = file(localPath, "wb")
        f.write(response.read())
        f.close()
    except HTTPError:
        pass


http://www.meinvsushe.com/
http://meizi.us/
https://www.leonax.net/res/
mmurl = "http://t1.mm8mm8.com/mm8/tupai/20"

x = range(12, 16) #year y
a = ['%02d' % i for i in range(1, 13)] #month m
b = ['%03d' % i for i in range(1, 120)] #pic directory  day
c = range(1, 16) #pic number n

def getUrl():
    for y in x:
        for m in a:
            for d in b:
                for n in c:
                    #print mmurl + str(y) + m + '/' + d + '/' + str(n) + ".jpg"
                    real_url =  mmurl + str(y) + m + '/' + d + '/' + str(n) + ".jpg"
                    pic_name =  str(y) + m + d + str(n) + ".jpg "
                    #print real_url, pic_name
                    wget_url = "wget -O " + pic_name + real_url 
                    #downImage(real_url, pic_name) 
                    print wget_url
                    os.system(wget_url)
                    time.sleep(0.5)

if __name__ == '__main__':
    getUrl() 
    #downImage(real_url, pic_name) 
