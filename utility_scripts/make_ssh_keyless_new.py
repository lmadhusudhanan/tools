#!/usr/local/bin/python3

import pexpect
import re
import time
import sys
import threading
from threading import Thread

hostname = "10.84.55."
master_ip = "10.84.55.2"
username = "root"
password = "c0ntrail123"
threads = []


vm_last_octet = int(sys.argv[1])
vm_last_octet_limit = int(sys.argv[2])

print("a")
s = pexpect.spawn("ssh {0} -l {1}".format(master_ip, username))
s.logfile = open("/tmp/mylog2", "wb+")
response = s.expect([".*yes/no.*",".*assword:"])
if response==1:
    s.sendline(password)
if response==0:
    s.sendline("yes")
    s.expect(".*assword:")
    s.sendline(password)

time.sleep(1)
print("b")
s.sendline("ssh-keygen -t rsa ")
s.expect(":")
s.sendline("\n")
response = s.expect(["Overwrite (y/n)?",":"])
if response == 0:
    s.sendline('y')
    s.expect(':')
    s.sendline('\n')
elif response == 1:
    s.sendline("\n")
s.expect(":")
s.sendline("\n")
s.expect(":")
s.sendline("\n")
s.expect("#")


time.sleep(1)
print("c")

while(vm_last_octet <= vm_last_octet_limit):
    print (vm_last_octet)
#    s = pexpect.spawn("ssh {0} -l {1}".format(master_ip, username))
    s.delaybeforesend = None
    response = s.expect([".*yes/no.*",".*assword:"])
    print("first response is {}".format(response))
    if response==1:
        s.sendline(password)
    if response==0:
        s.sendline("yes")
        s.expect(".*assword:")
        s.sendline(password)
    time.sleep(5)
    print("ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.84.55.{0} -f".format(vm_last_octet))
    s.sendline("ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.84.55.{0} -f".format(vm_last_octet))
    response = s.expect([".*Are you sure.*", ".*password"])
    print("second response is {}".format(response))
    if response == 0:
        s.sendline("yes")
        s.expect(".*password:")
        s.sendline(password)
        s.expect("#")
    elif response == 1:
        s.sendline(password)
        s.expect("#")
    time.sleep(1)
    vm_last_octet += 1
    time.sleep(1)
    s.flush()
    s.close()
