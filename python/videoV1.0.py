#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(c.yingxian)s
"""
import sys
type_ = sys.getfilesystemencoding()

import urllib,urllib2
import time
import re
from random import choice
from multiprocessing.dummy import Pool
import os
import socket

# 用于抽取主页中的视频部分
extractPart=re.compile('<div class="nag cf">([\s\S]*?)<div class="loop-nav-inner">')
#抽取视频内容页url
extractVideoUrl=re.compile('<a class="clip-link".*?href="(.*?)">')
#用于抽取内容页的视频连下载链接
extractVideo=re.compile('m4v:"(.*?mp4)"')

#获得所有的带页码的主页url
def parse_home_url(init_url,v_type,start,end):
  url='%s%s/page/'%(init_url,v_type)
  home_url_list=[]
  for i in xrange(start,end+1):
    urls=url+str(i)
    home_url_list.append(urls)
  return home_url_list

#获得主页url内容的视频部分
def parse_video_part(url):
  global contents,headers
  req=urllib2.Request(url,headers=headers)
  res=urllib2.urlopen(req)
  content=res.read()
  res.close()
  content=extractPart.findall(content)
  contents=contents.join(content)

#获得视频内容页url
def parse_vdeo_url(contents):
  video_list=extractVideoUrl.findall(contents)
  return video_list

#从contents获得视频下载连接
def direct_video_url(video_url):
  global headers,video_direct_list
  try:
    req=urllib2.Request(video_url,headers=headers)
    res=urllib2.urlopen(req)
    content=res.read()
    res.close()
    v_list=extractVideo.findall(content)
    video_direct_list.extend(v_list)
  except:
    print '%s parse failed'%video_url

#下载下载下载
def download(v_d_url):
  global save_path,count
  filename=save_path+v_d_url.split('/')[-1]
  try:
    urllib.urlretrieve(v_d_url,filename=filename)
    count+=1
  except:
    print 'video:%s download failed'%filename

if __name__=='__main__':
  print '###########################\n\
writted by C.yingxian\n\
any question mailto cyx2012scut@163.com\n\
###########################'
  
  hlist=['Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',\
       'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',\
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",\
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7'
        ]
  user_agent=choice(hlist)
  #global variable
  headers = {'User-Agent':user_agent}
  typeList={1:'meizi',2:'rewu',3:'fuli',4:'gaoxiao',5:'chuangyi'}
  hosturl='http://www.9db.cc/'
  contents=''
  video_direct_list=[]
  save_path='d:/videos/'
  count=0
  #设置超时值
  socket.setdefaulttimeout(60)
  #设置代理
  i='是否使用代理？是-->请输入代理地址，例如：192.168.0.0:22；否-->请输入no\n-->'
  proxy_i=raw_input(i.decode('utf-8').encode(type_))
  if proxy_i!='no':
    #设置使用代理
    proxy = {'http':proxy_i}
    proxy_support = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
  #选择下载类型
  info='选择下载类型：\n\
1：微拍妹子 2：微拍热舞 3：微拍福利 4：搞笑短片 5：创意视频\n-->'
  v_num=input(info.decode('utf-8').encode(type_))
  v_type=typeList[v_num]
  #设置保存位置
  info='你想把下载内容存在哪里？输入yes则默认保存在D:/pictures目录；\n\
或者输入一个目录地址，例如：D:/videos/，但是别忘了最后面的斜杠/\n\
[yes/目录地址]-->'
  save_path=raw_input(info.decode("utf-8").encode(type_))
  if save_path=='yes':
    save_path='d:/videos/'
    if not os.path.exists(save_path):
      os.mkdir(save_path)
  else:
    if not os.path.exists(save_path):
      os.mkdir(save_path)
  #选择从第几页开始
  start=input('从第几页开始下载？-->'.decode('utf-8').encode(type_))
  #到第几页结束
  end=input('到第几页结束？-->'.decode('utf-8').encode(type_))
  #线程数&设置线程
  thread_num=input('最大线程数？-->'.decode('utf-8').encode(type_))
  pool=Pool(thread_num)
  #开始时间
  st0=time.time()
  #step 1:
  home_list=parse_home_url(hosturl,v_type,start,end)
  st1=time.time()
  print '第一步完成时间：%ss'.decode('utf-8').encode(type_)%(st1-st0)
  #step 2:
  pool.map(parse_video_part,home_list)
  st2=time.time()
  print '第二步完成时间：%ss'.decode('utf-8').encode(type_)%(st2-st1)
  #step 3:
  video_list=parse_vdeo_url(contents)
  st3=time.time()
  print '第三步完成时间：%ss'.decode('utf-8').encode(type_)%(st3-st2)
  #step 4:
  pool.map(direct_video_url,video_list)
  st4=time.time()
  print '第四步完成时间：%ss'.decode('utf-8').encode(type_)%(st4-st3)
  #step 5:
  pool.map(download,video_direct_list)
  st5=time.time()
  print '第五步完成时间：%ss'.decode('utf-8').encode(type_)%(st5-st4)
  #结束进程
  pool.close()
  pool.join()
  #ptint infomation
  print '视频下载完毕！\n一个下载了%s部视频'.decode('utf-8').encode(type_)%count
  print '视频保存在%s'.decode('utf-8').encode(type_)%save_path
  time.sleep(5)

    

