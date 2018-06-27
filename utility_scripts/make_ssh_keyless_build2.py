#!/usr/bin/python

import pexpect
import re
import time

def pass_ssh_keys_to_nodes():
    hostname = "10.84.5.31"
    username = "lmadhusudhan"
    password = "Dreamliner_1"
    username2 = "root"
    password2 = "c0ntrail123"
    s = pexpect.spawn("ssh {0} -l {1}".format(hostname, username))
    x = s.expect(["yes/no",".*assword:"])
    if x==1:
        s.sendline(password)
    if x==0:
        s.sendline("yes")
        s.expect("assword:")
        s.sendline(password)
    s.expect("$")
    print "sss"
    s.logfile = open("/tmp/mylog", "w+")
    s.sendline("ssh-keygen -t rsa")
    s.expect(":")
    print "sdddsss"
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
    s.expect("$")
    
    last_octet = 46
    while(last_octet < 225):
	print last_octet
	#import pdb;pdb.set_trace()
        s.sendline("ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.84.54.{0}".format(last_octet))
        x = s.expect(["yes/no", "$", ':'])
        if x==0:
            s.sendline("yes")
            s.expect("word:")
            s.sendline(password2)
            s.expect("$")
	if x==2:
            s.sendline(password2)
            s.expect("$")
	else:
	    s.sendline("\n")
	    s.expect("$")
    	last_octet += 1
        time.sleep(2)
    s.close()

pass_ssh_keys_to_nodes()
