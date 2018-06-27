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

def exec_cmd_thread(vm_last_octet, master_last_octet):
    print("Creating new thread")
    local_data = threading.local()
    local_data.vm_last_octet = vm_last_octet
    local_data.master_last_octet = master_last_octet
    local_data.hostname_new = hostname + str(local_data.vm_last_octet)
    print(local_data.hostname_new)
    s = pexpect.spawn("ssh {0} -l {1}".format(local_data.hostname_new, username))
    s.delaybeforesend = None
    x = s.expect([".*yes/no.*",".*assword:"])
    if x==1:
        s.sendline(password)
    if x==0:
        s.sendline("yes")
        s.expect("assword:")
        s.sendline(password)
    s.expect("#")
    #s.logfile = open("/tmp/mylog", "w+")
   # s.sendline("ssh-keygen -t rsa ")
   # s.expect(["#", ":"])
   # s.sendline("\n")
   # x = s.expect([":", "(y/n)?"])
   # if x==0:
   #     s.sendline("\n")
   # if x==1:
   #     s.sendline("y")
   #     s.expect(":")
   #     s.sendline("\n")
   # s.expect(":")
   # s.sendline("\n")
   # s.expect(":")
    while(local_data.master_last_octet <= 2):
        print(local_data.master_last_octet)
        print(vm_last_octet)
        print("sudo ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.84.55.{0} -f".format(local_data.master_last_octet))
        try:
            s.sendline("rm -rf /root/.ssh/known_hosts")
            s.expect("#")
            s.sendline("sudo ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.84.55.{0} -f".format(local_data.master_last_octet))
            x = s.expect(["Are you sure you want to continue", "#", 'password:'])
            if x==0:
                print("a")
                s.sendline("yes")
                print ("a12")
                print (s.before)
                print (s.after)
                m=s.expect(["#", "password:"])
                if m==1:
                    print("a33")
                    s.sendline(password)
                    s.expect("#")
                s.sendline('\n')
                s.expect('#')
                print("a3")
            if x==2:
                print("b")
                s.sendline(password)
                s.expect("#")
            elif x==1:
                print("c")
                s.sendline("\n")
                s.expect(".*")
            time.sleep(0.5)
        except pexpect.TIMEOUT:
            print("pexpect timeout. Re-trying")
            s.close()
            s = pexpect.spawn("ssh {0} -l {1}".format(local_data.hostname_new, username))
            x = s.expect(["Are you sure you want to continue","assword:"])
            if x==1:
                s.sendline(password)
            if x==0:
                s.sendline("yes")
                s.expect("assword:")
                s.sendline(password)
            s.expect("#")
            continue
        local_data.master_last_octet += 1
        time.sleep(2)
    s.close()

def pass_ssh_keys_to_nodes():

    master_last_octet = 2
    vm_last_octet=int(sys.argv[1])
    print(sys.argv)
    while(vm_last_octet<int(sys.argv[2])):
        print(vm_last_octet)
    #    threads.append(Thread(target=exec_cmd_thread ,args=(vm_last_octet, master_last_octet)))
        exec_cmd_thread(vm_last_octet, master_last_octet)
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
