#!/usr/local/bin/python3

import pexpect
import re
import time
import sys
import threading
from threading import Thread

hostname = "10.84.55."
username = "root"
password = "c0ntrail123"
threads = []

def exec_cmd_thread(y, master_last_octet):
    ssh_key_exists = False
    print("Creating new thread")
    local_data = threading.local()
    local_data.y = y
    local_data.master_last_octet = master_last_octet
    local_data.hostname_new = hostname + str(local_data.y)
    print(local_data.hostname_new)
    local_data.s = pexpect.spawn("ssh {0} -l {1}".format(local_data.hostname_new, username))
    x = local_data.s.expect([".*yes/no.*",".*assword:"])
    if x==1:
        local_data.s.sendline(password)
    if x==0:
        local_data.s.sendline("yes")
        local_data.s.expect("assword:")
        local_data.s.sendline(password)
    local_data.s.expect("#")
    local_data.s.logfile = open("/tmp/mylog", "wb+")
    print("Generating ssh keygen")
    local_data.s.sendline("ssh-keygen -t rsa ")
    local_data.s.expect(["#", ":"])
    local_data.s.sendline("\n")
    x = local_data.s.expect([":", "already exists"])
    if x==0:
        local_data.s.sendline("\n")
    if x==1:
        print("ddd")
        #ssh_key_exists = True
        #local_data.s.close()
        local_data.s.sendline("y")
        local_data.s.expect(":")
        local_data.s.sendline("\n")
    if not ssh_key_exists:
        local_data.s.expect(":")
        local_data.s.sendline("\n")
        local_data.s.expect("#")
        local_data.s.close()
    while(local_data.master_last_octet < 3):
        print("Re-connecting to VM")
        time.sleep(2)
        local_data.s = pexpect.spawn("ssh {0} -l {1}".format(local_data.hostname_new, username))
        local_data.s.logfile = open("/tmp/mylog2", "wb+")
        print(local_data.master_last_octet)
        print("ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.84.55.{0} -f".format(local_data.master_last_octet))
        local_data.s.sendline("ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.84.55.{0} -f".format(local_data.master_last_octet))
        x = local_data.s.expect([".*yes/no.*", '.*password:', ".*#"])
        if x==0:
            print("aa")
            local_data.s.sendline("yes")
            local_data.s.expect("word:")
            local_data.s.sendline(password)
            local_data.s.expect("#")
        if x==1:
            print("bb")
            local_data.s.sendline(password)
            local_data.s.expect("#")
        elif x==2:
            print("cc")
            local_data.s.sendline("\n")
            local_data.s.expect(".*")
        time.sleep(0.5)
        local_data.master_last_octet += 1
        local_data.s.close()

def pass_ssh_keys_to_nodes():

    master_last_octet = 2
    vm_last_octet=int(sys.argv[1])
    print(sys.argv)
    while(vm_last_octet<int(sys.argv[2])):
        print(vm_last_octet)
        threads.append(Thread(target=exec_cmd_thread ,args=(vm_last_octet, master_last_octet)))
        print(vm_last_octet)
        vm_last_octet += 1
    print("b")

print("a")
pass_ssh_keys_to_nodes()
print("Starting all threads")
for thread in threads:
   thread.start()

print("Waiting for all threads to finish")
for thread in threads:
    thread.join()
