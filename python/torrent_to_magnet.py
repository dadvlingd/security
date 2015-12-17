#!/usr/bin/python
#-*- coding: utf-8 -*-
#before run this script you should:
#git clone https://github.com/arvidn/libtorrent.git
#cd libtorrent Run: python setup.py build. As root, run: python setup.py install
#yum install rb_libtorrent-python

import os
import sys
import libtorrent as bt

reload(sys)
sys.setdefaultencoding('utf8') #解决 python的str默认是ascii编码，和unicode编码冲突

def Usage():
    print "Usage: %s dir" % sys.argv[0]

def get_file_name(rootdir):
    for lists in os.listdir(rootdir):
        t_file = os.path.join(rootdir, lists)
        if os.path.splitext(t_file)[1] == '.torrent': #make sure file is torrent
            torrent_to_magnet(t_file)
            if os.path.isdir(t_file):
                get_file_name(t_file)

def torrent_to_magnet(t_file):
    #print t_file
    info = bt.torrent_info(t_file)
    magnet_hash = info.info_hash()
    magnet_name = info.name()
    #print "magnet:?xt=urn:btih:" + str(btih) + "&dn=" + infos 
    #print "magnet:?xt=urn:btih:%s&dn=%s" % (info.info_hash(), info.name())
    magnet_link = "magnet:?xt=urn:btih:" + str(magnet_hash) + "&dn=" + magnet_name +'\n'
    print magnet_link
    magnet_file = open('magnet.txt', 'a')
    magnet_file.write(magnet_link)
    magnet_file.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        Usage()
        sys.exit(0)
    magnet_file = open('magnet.txt', 'w') #清空文件
    magnet_file.close()
    get_file_name(sys.argv[1])

