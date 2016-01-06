#!/usr/bin/python
#-*_ coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2, socket, time
import re, random

base_url = 'http://torrentba.com/s/'

user_agents = list()

class MagentAPI:
    def __init__(self):
        timeout = 40
        socket.setdefaulttimeout(timeout)

    def randomeSleep(self):
        sleeptime = random.randint(60, 120)
        time.sleep(sleeptime)

    def writetofile(self, result):
        magnet_url = "magnet:?xt=urn:btih:" + result + '\n'
        print result
        magnet_file = open('magnet.txt', 'a')
        magnet_file.write(magnet_url)
        magnet_file.close()
        time.sleep(1)

    def write_no_search(self, keyword):
        print 'no search %s' % keyword
        nofile = open('nosearch.txt', 'a')
        nofile.write(keyword)
        nofile.write('\n')
        nofile.close()
    

    def extractResults(self, html):
        if html != None:
            searchUrl = html.decode('utf-8')
            magRe = re.compile(r'(?<=href="http://torrentba.com/list/)\w*')
            magUrl = magRe.findall(searchUrl)
            print len(magUrl[0])
            return magUrl[0]

    #search magnet
    #@param keyword ->  key words for search
    #@param num -> number of search results to return
    def search(self, keyword, num):
        #search_results = list()
        query = urllib2.quote(keyword)  #解析搜索关键字
        url = '%s%s/' % (base_url, query)
        print url
        retry = 3
        while(retry > 0):
            try:
                request = urllib2.Request(url)
                length = len(user_agents)
                index = random.randint(0, length - 1)
                user_agent = user_agents[index]
                request.add_header('User-Agent', user_agent) 
                response = urllib2.urlopen(request)
                html = response.read()
                n = str(html).count(query)
                print n
                if n <= 8: #search no find result
                    self.write_no_search(query)
                    break;
                search_results = self.extractResults(html)
                if len(search_results):
                    self.writetofile(search_results)
                else:
                    break;
                break;
            except urllib2.URLError, e:
                print 'url error:', e
                self.randomeSleep()
                retry = retry - 1
                continue
            
            except Exception, e:
                print 'error:', e
                retry = retry -1
                self.randomeSleep()
                continue

def load_user_agent():
    fp = open('./user_agents', 'r')

    line = fp.readline().strip('\n')
    while(line):
        user_agents.append(line)
        line = fp.readline().strip('\n')
    fp.close()

def searcher():
    #清空保存结果的文件
    magnet_file = open('magnet.txt', 'w')
    magnet_file.close()
    #清空未搜到关键字的文件
    magnet_file = open('nosearch.txt', 'w')
    magnet_file.close()
    #Load use agent string form file
    load_user_agent()

    # Create a MagentAPI instance
    api = MagentAPI()

    #set expect search results to be searcher
    expect_num = 10
    #if no parameters, red query keywords form file
    if(len(sys.argv) < 2):
        keywords = open('./keywords', 'r')
        keyword = keywords.readline().strip('\n')
        while(keyword):
            results = api.search(keyword, num = expect_num)
            #for r in results:
            keyword = keywords.readline().strip('\n')
    else:
        keyword = sys.argv[1]
        results = api.search(keyword, num = expect_num)
        print 'have args'

if __name__ == '__main__':
    searcher()
