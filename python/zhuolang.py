#-*-coding:utf8-*-
#!/usr/bin/python
# Python:      2.7.8
# Platform:    Windows
# Program:     Get Novels From Internet
# Author:      wucl
# Description: Get Novels
# Version:     1.0
# History:     2015.5.27  完成目录和url提取
#              2015.5.28  完成目录中正则提取第*章，提取出章节链接并下载。在逐浪测试下载无误。
 
from bs4 import BeautifulSoup
import urllib2,re
 
def get_menu(url):
    """Get chapter name and its url"""
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0"
    headers = {'User-Agent':user_agent}
    req = urllib2.Request(url,headers = headers)
    page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page)
    novel = soup.find_all('title')[0].text.split('_')[0]     # 提取小说名
    menu = []
    all_text = soup.find_all('a',target="_blank")   # 提取记载有小说章节名和链接地址的模块
    regex=re.compile(ur'\u7b2c.+\u7ae0')          # 中文正则匹配第..章，去除不必要的链接
    for title in all_text:
        if re.findall(regex,title.text):
            name = title.text
            x = [name,title['href']]
            menu.append(x)       # 把记载有小说章节名和链接地址的列表插入列表中                
    return menu,novel
 
def get_chapter(name,url):
    """Get every chapter in menu"""
    html=urllib2.urlopen(url).read()
    soup=BeautifulSoup(html)
    content=soup.find_all('p')     # 提取小说正文
    return content[0].text
     
     
     
 
if __name__=="__main__":
    url=raw_input("""Input the main page's url of the novel in ZhuLang\n        Then Press Enter to Continue\n""")
    if url:
        menu,title=get_menu(url)
        print title,str(len(menu))+'\n     Press Enter To Continue   \n'     # 输出获取到的小说名和章节数
        for i in menu:
            chapter=get_chapter(i[0],i[1])
            raw_input()
            print '\n'+i[0]+'\n'       
            print chapter
            print '\n'
