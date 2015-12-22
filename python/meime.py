#/usr/bin/python3
#-*- coding: UTF-8 -*-

import urllib.request
import urllib.error
from http import server, client #方便后面能够捕获到此类相关的异常
import os, re

#伪装成浏览器
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}

def urlOpen(url):
    global header
    req = urllib.request.Request(url, None, header)
    return urllib.request.urlopen(req).read()

def tryToGet(url):
    errorTimes = 0 #记录出错次数，超过5次则放弃访问该页面
    while errorTimes != 5:
        try: #尝试访问该页面
            errorTimes += 1
            return urlOpen(url)
        except: #若出现异常则忽略，重新访问
            pass

    return None #超过5次访问失败，返回空值

#get picture numbers
def getPicnum(url):
    pic_num = tryToGet(url)
    if pic_num != None:
        pic_html = pic_num.decode('utf-8')
        ppp = re.compile(r'(?<=<h1>).*(?=P]<\/h1>)')
        list_num = ppp.findall(pic_html)
        str_num = str(list_num) #转换成字符串，方便切片

        girl_num = int((str_num.split("[")[2].split("'")[0]))
        title_name = str_num.split("[")[1].split("'")[1] # get 标题名字
        os.mkdir(title_name) #make new dir
        os.chdir(title_name)

        return girl_num
    else:
        print('********cant not get ipic num')
        return list()

#get every person url
def getPersonurl(url):
    p_response = tryToGet(url)
    if p_response != None:
        p_html = p_response.decode('utf-8')
        pp = re.compile(r'<a href="/(.*\.html)" target="_blank">')
        return pp.findall(p_html)
    else:
        print('*********can not get personal url')
        return list()

#获取子页面
def getSubpage(url):
    response = tryToGet(url)
    if response != None:
        html = response.decode('utf-8')
        #用于获取标题栏中子页面url的正则表达式
        p = re.compile(r'<a href="/(.*\.html)" class="tag-font-size-14">')
        return p.findall(html)
    else:
        print('**********当前页面获取失败')
        return list()

imgCount = 1#图片计数器
def saveImgInPage(url, num):
    #global imgCount
    #print('**********正在获取页面' + url)
    response = tryToGet(url)
    if response != None:
        html = response.decode('utf-8')
        #获取图片url的正则表达式
        p = re.compile(r'<img .* src="(.*\.jpg)"')
        imgList = p.findall(html)

        for each in imgList:
            #print ("\n%s" % imgList)
            response = tryToGet(each)
            if response != None:
                #保存图片
                with open(str(num) + '.jpg', 'wb') as f:
                    f.write(response)
                #print('**********目前已成功获取%d张图片!' % imgCount)
                #imgCount += 1

    else:
        print('**********当前页面获取失败!')

def work():
    if not os.path.isdir('Girl'):
        os.mkdir('Girl')
    os.chdir('Girl')
    
    PWD = os.getcwd()

    url = 'http://www.chunmm.com/'
    subpageList = getSubpage(url)#获取子页面
    subpageList.insert(0, '')#加入首页

    for each in subpageList:  #爬取每个页面上的图片
        Person_urlList = getPersonurl(url + each)
        for i in range(0, len(Person_urlList), 2):  #每个页面中有两个有效url故只能保留一个
            personurl = url + Person_urlList[i]
            os.chdir(PWD) #change to 主目录
            gir_num = getPicnum(personurl)  #get sum of everygirl's pic 
            #print (gir_num)
            for num in range(1, gir_num + 1): 
                girurl = personurl.split("-")[0] + "-" + str(num) + ".html" #get every pic's url
                #print (girurl)
                #print (personurl.split("-")[-1])
                #print (personurl)
                saveImgInPage(girurl, num)  #downlaod image
    

if __name__ == '__main__':
    work()
