#!/usr/local/bin/python3

import pexpect
import re
import time

def pass_ssh_keys_to_nodes():
    hostname = "10.84.55.2"
    username = "root"
    password = "c0ntrail123"
    
    last_octet = 25
    while(last_octet <= 52):
        s = pexpect.spawn("ssh -l {1} 10.84.55.{0}".format(last_octet, username))
        x = s.expect([".*yes/no.*",".*assword:", "#"])
        if x==1:
            s.sendline(password)
        if x==0:
            s.sendline("yes")
            s.expect("assword:")
            s.sendline(password)
        if x==2:
            s.sendline("")
        s.expect("#")
        s.logfile = open("/tmp/mylog", "wb+")
        s.sendline("ssh-keygen -t rsa")
        s.expect("Enter file in which to save the key")
        print("Enter file in which to save the key")
        s.sendline("")
        time.sleep(0.5)
        print(s.before)
        print(s.after)
        x = s.expect(["Enter passphrase \(empty for no passphrase\)", "Overwrite"])
        print(s.before)
        print(s.after)
        if x==0:
            print("Enter passphrase (empty for no passphrase)")
            s.sendline("")
        if x==1:
            time.sleep(0.5)
            print("Overwrite (y/n)?")
            s.sendline("y")
            print(s.before)
            print(s.after)
            s.expect(".*empty for no passphrase.*")
            print("Enter passphrase (empty for no passphrase)")
            s.sendline("")
        s.expect(".*Enter same passphrase again.*")
        print("Enter same passphrase again")
        time.sleep(0.5)
        s.sendline("")
        s.expect(".*")
        print (last_octet)
	#import pdb;pdb.set_trace()
        print ("ssh-copy-id -i ~/.ssh/id_rsa.pub root@{0} -f".format(hostname))
        s.sendline("ssh-copy-id -i ~/.ssh/id_rsa.pub root@{0} -f".format(hostname))
        x = s.expect(["password", ".*Are you sure you want to continue connecting.*"])
        print(s.before)
        print(s.after)
        if x==1:
            print("Are you sure you want to continue connecting")
            s.sendline("yes")
            s.expect(".*word:.*")
            s.sendline(password)
            s.expect("#")
        if x==0:
            print("password")
            s.sendline(password)
            s.expect("#")
        else:
            print("#")
            s.sendline("\n")
            s.expect(["#", "$"])
        last_octet += 1
        time.sleep(0.5)
        s.close()

pass_ssh_keys_to_nodes()
