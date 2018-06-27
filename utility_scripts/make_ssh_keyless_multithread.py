#!/usr/bin/python

import pexpect
import re
import time
import sys
import threading
from threading import Thread

hostname = "10.84.54."
username = "root"
password = "c0ntrail123"
threads = []

def exec_cmd_thread(y, last_octet):
	print "Creating new thread"
	local_data = threading.local()
	local_data.y = y
	local_data.last_octet = last_octet
        local_data.hostname_new = hostname + str(local_data.y)
        print local_data.hostname_new
        s = pexpect.spawn("ssh {0} -l {1}".format(local_data.hostname_new, username))
        x = s.expect([".*yes/no.*",".*assword:"])
        if x==1:
            s.sendline(password)
        if x==0:
            s.sendline("yes")
            s.expect("assword:")
            s.sendline(password)
        s.expect("#")
   #     s.logfile = open("/tmp/mylog", "w+")
        s.sendline("ssh-keygen -t rsa ")
        s.expect(["#", ":"])
        s.sendline("\n")
        x = s.expect([":", "(y/n)?"])
        if x==0:
            s.sendline("\n")
        if x==1:
            s.sendline("y")
            s.expect(":")
            s.sendline("\n")
        s.expect(":")
        s.sendline("\n")
        s.expect(":")
        while(local_data.last_octet < 225):
            print local_data.last_octet
            print "ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.84.54.{0} -f".format(local_data.last_octet)
            try:
                s.sendline("ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.84.54.{0} -f".format(local_data.last_octet))
                x = s.expect([".*yes/no.*", "#", 'password:'])
                if x==0:
                    s.sendline("yes")
                    s.expect("word:")
                    s.sendline(password)
		    s.expect("#")
                if x==2:
                    s.sendline(password)
                    s.expect("#")
                else:
                    s.sendline("\n")
                    s.expect(".*")
                time.sleep(0.5)
            except pexpect.TIMEOUT:
                print "pexpect timeout. Re-trying"
                s.close()
                s = pexpect.spawn("ssh {0} -l {1}".format(local_data.hostname_new, username))
                x = s.expect([".*yes/no.*",".*assword:"])
                if x==1:
                    s.sendline(password)
                if x==0:
                    s.sendline("yes")
		    s.expect("assword:")
                    s.sendline(password)
                s.expect("#")
                continue
            local_data.last_octet += 1
            time.sleep(2)
        s.close()

def pass_ssh_keys_to_nodes():
    
    last_octet = 25
    y=int(sys.argv[1])
    print sys.argv
    while(y<int(sys.argv[2])):
	print y
	threads.append(Thread(target=exec_cmd_thread ,args=(y, last_octet)))
	print y
        y += 1
    print "b"

print "a"
pass_ssh_keys_to_nodes()
print "Starting all threads"
for thread in threads:
   thread.start()

print "Waiting for all threads to finish"
for thread in threads:
    thread.join()
