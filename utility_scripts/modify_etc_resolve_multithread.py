#!/usr/bin/python
import paramiko
from threading import Thread
import time

def exec_cmd_thread(last_octet):
    username = "root"
    password = "c0ntrail123"
    hostname = "10.84.54"    
    print "a"
    s = pexpect.spawn("ssh 10.84.54.{0} -l {1}".format(last_octet, username))
    x = s.expect([".*yes/no.*",".*assword:"])
    if x==1:
        s.sendline(password)
    if x==0:
        s.sendline("yes")
        s.expect("assword:")
        s.sendline(password)
    s.expect("#")
    print "b"
    s.logfile = open("/tmp/mylog", "w+")
    s.sendline("printf \"nameserver 172.29.131.60 \" >> /etc/resolv.conf")
    s.expect("#")
    s.sendline("printf \"\\n\" >> /etc/resolv.conf")
    s.expect("#")
    s.sendline("printf \"10.84.54.2 b1s2.contrail.juniper.net  b1s2 \" >> /etc/hosts")
    s.expect("#")
    s.sendline("printf \"\\n\" >> /etc/hosts")
    s.expect("#")
    x+=1
    last_octet += 1
    s.close()
    print "d"

def run_cmd_on_remote_server():

    lock = False
    last_octet = 25
    threads = []
    while(last_octet<31):
        time.sleep(1)
        print "Creating new thread"
        print last_octet
        if not lock:
            print "Acquiring lock..."
            lock = True
            try:
                    threads.append(
                        Thread(
                            target=exec_cmd_thread ,
                            args=(last_octet)))
                    cmd_new = ""
                    lock = False
                    print "Releasing lock..."
            except Exception,e:
                print "Exception: Retrying... "
                lock = False
                cmd_new = ""
                print str(e)
                continue
        else:
            print "Waiting for lock to be release ... Retrying"
            continue
        last_octet += 1
    
    print "Starting all threads"
    for thread in threads:
       thread.start()

    print "Waiting for all threads to finish"
    for thread in threads:
        thread.join()

run_cmd_on_remote_server()
