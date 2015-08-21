#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2015-2016 Shen Cloud, Inc.
#

import os
import socket
import select
import time
import threading
import logging
import logging.handlers
import socket
from multiprocessing import Process
from multiprocessing.connection import Listener
from subprocess import Popen, PIPE, CalledProcessError, call
try:
    from subprocess import check_output
except ImportError:
    def func(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = Popen(stdout=PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise CalledProcessError(retcode, cmd)
        return output
    check_output = func

DNS_FILE = '/etc/resolv.conf'
UPS_CONF = "/etc/ups.conf"
DEFAULT_PORT = 12345
LISTEN_PORT = 8012
POWEROFF_DELAY = 200
SHUTDOWN_ALL_VMS = "kill -12 `ps aux | grep '/usr/bin/python /usr/share/vdsm/vdsm' | grep -v grep | awk '{print $2}'`"
PRE_POWEROFF = '''
sleep %s
killall qemu-kvm''' % POWEROFF_DELAY  # shutdown host after 210 seconds
POWEROFF = '''
sleep 5
service vdsmd stop
#service supervdsmd stop
sleep 5
poweroff'''
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10M
LOG_BAK_COUNT = 5

log_dir = '/var/log/sycos/'
def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    else:
        return False
mkdir(log_dir)
format_ = '%(asctime)s  %(filename)s[line:%(lineno)d] \n\t[%(levelname)s] %(message)s'
file_name = 'ups.log'
log_file_name = os.path.join(log_dir, file_name)

def init_log(file_level=logging.DEBUG):
    '''initialize log.
    '''

    global format_, log_file_name
    log = logging.getLogger(__name__)
    logging.basicConfig(level=file_level,
                        format=format_,
                        filename=log_file_name,
                        filemode='w')
    handler = logging.handlers.RotatingFileHandler(log_file_name,
                                                   maxBytes=MAX_LOG_SIZE,
                                                   backupCount=LOG_BAK_COUNT)
    log.addHandler(handler)

    return log

log = init_log()

class MyTimer(object):
    '''custom circle timer

    note: plz do not use stop -> start at the same instance,
          you should create a new instance to start after stopped.
    '''

    def __init__(self, interval, function, args=[], kwargs={}):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.stop_flag = True

    def start(self):
        self.stop_flag = False
        self._timer = threading.Timer(self.interval, self._run)
        self._timer.setDaemon(True)
        self._timer.start()

    def stop(self):
        self.stop_flag = True
        if self.__dict__.has_key("_timer"):
            self._timer.cancel()
            del self._timer

    def _restart(self):
        self.stop()
        self.start()

    def _run(self):
        try:
            ret = self.function(*self.args, **self.kwargs)
        except:
            ret = True
        if ret:
            if self.stop_flag:
                pass
            else:
                self._restart()
        else:
            self.stop()

def ups_conn(host, port):
    server = (host, port)
    #print server
    timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(3.0)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(server)
        log.info('Connect to ups server successful!!!')
    except Exception, err:
        return False
    poller = select.poll()
    poller.register(sock.fileno(), select.POLLIN)

    def send_msg():
        #print 'send ping package'
        sock.sendall('ping')
        return True

    send_msg()
    t = MyTimer(10, send_msg)
    t.start()

    alarm = False
    while True:
        events = poller.poll()
        for _, event in events:
            if event & select.POLLIN:
                data = sock.recv(1024)
                if data.strip() == 'pang':
                    #print 'recv pang package'
                    pass
                elif data.strip() == 'alarm':
                    alarm = True
                    log.info('recv alarm package and goto shutdown.')
                    shutdown_vms_and_host()
                    break
                else:
                    log.error("unrecognize response:[%s] from ups server.", data)
                    pass
        if alarm:
            alarm = False
            break

    t.stop()
    socket.setdefaulttimeout(timeout)
    sock.close()
    return True

def poweroff_info():
    time_left = POWEROFF_DELAY + 10
    for i in range(time_left)[::-1]:
        print 'Server is shutting down now, pelease wait ...', i+1
        time.sleep(1)

def shutdown_vms_and_host():
    call(SHUTDOWN_ALL_VMS, shell=True)
    threading.Thread(target=poweroff_info).start()
    call(''.join([PRE_POWEROFF, POWEROFF]), shell=True)

    return "Shutdown all successful!"

def ping_test(ip):
    ret = call('ping -c 2 -w 10 %s > /dev/null 2>&1' % ip, shell=True)
    if not ret:
        # print 'ping %s success.' % ip
        return True
    else:
        # print 'ping %s failed!' % ip
        return False

def usage():
    print "Usage: upsdaemo.py"

def get_ups_addr():
    if os.path.exists(UPS_CONF):
        with open(UPS_CONF) as ups:
            info = ups.read().strip()
            server = info.split(':')
            host = server[0]
            if len(server) < 2:
                port = DEFAULT_PORT
            else:
                port = int(server[1])
            if host:
                return host, port
            else:
                log.error("/etc/ups.conf file is empty.")
    else:
        log.error("/etc/ups.conf is not exist.")
    return None, None

def check_ip(ipaddr):
    """Is it a ip string format"""

    addr_list = ipaddr.strip().split('.')  # 切割IP地址为一个列表
    if len(addr_list) != 4:  # 切割后列表必须有4个参数
        return False

    for addr in addr_list:
        try:
            addr = int(addr)  # 每个参数必须为数字，否则校验失败
        except:
            return False

        if addr > 255 or addr < 0:  # 每个参数值必须在0-255之间
            return False

    return True

def check_port(port):
    if port >= 0 and port <= 65535:
        return True
    else:
        return False

def powerkey():
    evt_file = open("/dev/input/event1", "rb")
    while True:
        #print "loop----"
        evt = evt_file.read(16) # Read the event
        evt_file.read(16)       # Discard the debounce event
        code = ord(evt[10])
        if code == 0:
            shutdown_vms_and_host()
            break

def listen_powerkey():
    threading.Thread(target=powerkey).start()

def pre_poweroff_host():
    threading.Thread(target=poweroff_info).start()
    call(PRE_POWEROFF, shell=True)
    return "poweroff host successful!"

def poweroff_host():
    call(POWEROFF, shell=True)

def get_dns1():
    for line in open(DNS_FILE):
        if line.startswith('nameserver'):
            dns = line.split()[1].split('#')[0]
            return dns
    return None

def detect_ad(ad_ip, port):
    ad_port = port
    cmd = ['telnet', ad_ip, str(ad_port)]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    #output = check_output(['ls', '-l'], shell=True)
    output, err = p.communicate("echo -e '\n'")
    info = 'Connected to %s.' % ad_ip
    if info in output:
        # print 'telnet %s %s Sucessful!' % (ad_ip, ad_port)
        return True
    # print 'telnet %s %s Failed!' % (ad_ip, ad_port)
    return False

def check_ad(ad_ports=[135, 389, 636, 3268, 3269, 53, 88, 445]):
    ad_ip = get_dns1()
    while 1:
        if ad_ip and ping_test(ad_ip):
            for port in ad_ports:
                while True:
                    if detect_ad(ad_ip, port):
                        break
                    time.sleep(1)
                    if get_dns1() != ad_ip:
                        return check_ad()
                if get_dns1() != ad_ip:
                    return check_ad()
            else:
                #print 'ad is started already.'
                break
        time.sleep(1)
        if get_dns1() != ad_ip:
            return check_ad()

    return True

def server_listener():
    address = ('localhost', LISTEN_PORT)     # family is deduced to be 'AF_INET'
    listener = Listener(address, authkey='sycos local conn')
    while 1:
        conn = listener.accept()
        threading.Thread(target=proc_sycos, args=(conn,)).start()

def proc_sycos(conn):
    shutdown_flag = False

    while 1:
        try:
            data = conn.recv_bytes()
            #print data
        except EOFError:
            print 'close by remote.'
            break
        except:
            log.error('recv from sycos failed.')
            return
        if data == 'poweroff_host':
            resp = pre_poweroff_host()
            conn.send_bytes(resp)
            print 'stopped vdsmd successful!'
            shutdown_flag = True
            break
        elif data == 'waiting_ad':
            check_ad()
            conn.send_bytes('ad started successful!')
            break
        else:
            print 'recv msg is error! msg: %s' % data

    conn.close()
    if shutdown_flag:
        poweroff_host()

def run_listener():
    '''create a process to listen to sycos to stop vdsmd and shutdown host'''

    Process(target=server_listener).start()

def ups_server():
    while True:
        host, port = get_ups_addr()
        if host:
            if check_ip(host) and check_port(port):
                if ping_test(host):
                    if ups_conn(host, port):
                        #print host, port
                        break
                    else:
                        log.error('connect to ups server failed.')
                else:
                    log.error('ping ups ip:%s failed.', host)
            else:
                log.error('ups ip or port error at /etc/ups.conf, %s:%s', host, port)

        time.sleep(1)

def main():
    #run_listener()
    #listen_powerkey()
    ups_server()

if __name__ == '__main__':
    main()
