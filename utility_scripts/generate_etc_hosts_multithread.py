#!/usr/local/bin/python3
import paramiko
from threading import Thread
import time
import pexpect

def exec_cmd_thread(last_octet):
    username = "root"
    password = "c0ntrail123"
    hostname = "10.84.55"    
    print ("a")
    s = pexpect.spawn("ssh 10.84.55.{0} -l {1}".format(last_octet, username))
    x = s.expect([".*yes/no.*",".*assword:"])
    if x==1:
        s.sendline(password)
    if x==0:
        s.sendline("yes")
        s.expect("assword:")
        s.sendline(password)
    s.expect("#")
    print ("b")
    s.logfile = open("/tmp/mylog", "wb+")
    x=25
    while(x<53):
        print ("c")
        s.sendline("printf \"10.84.55.{0} k8s-scale-test-55-vm{1}.contrail.juniper.net k8s-scale-test-55-vm{2} \" >> /etc/hosts".format(x,x,x))
        s.expect("#")
        s.sendline("printf \"\\n\" >> /etc/hosts")
        s.expect("#")
        x+=1
    last_octet += 1
    s.close()
    print ("d")

def run_cmd_on_remote_server():

    lock = False
    last_octet = 25
    threads = []
    while(last_octet<53):
        time.sleep(1)
        print ("Creating new thread")
        print (last_octet)
        if not lock:
            print ("Acquiring lock...")
            lock = True
            try:
                    threads.append(
                        Thread(
                            target=exec_cmd_thread ,
                            args=(last_octet,)))
                    cmd_new = ""
                    lock = False
                    print ("Releasing lock...")
            except Exception:
                print ("Exception: Retrying... ")
                lock = False
                cmd_new = ""
                continue
        else:
            print ("Waiting for lock to be release ... Retrying")
            continue
        last_octet += 1
    
    print ("Starting all threads")
    for thread in threads:
       thread.start()

    print ("Waiting for all threads to finish")
    for thread in threads:
        thread.join()

run_cmd_on_remote_server()
