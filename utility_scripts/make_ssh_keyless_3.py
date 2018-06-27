#!/usr/bin/python

import pexpect
import re
import time

def pass_ssh_keys_to_nodes():
    hostname = "10.84.54.2"
    username = "root"
    password = "c0ntrail123"
    
    last_octet = 25
    while(last_octet < 31):
        s = pexpect.spawn("ssh {0} -l {1}".format(hostname, username))
        x = s.expect([".*yes/no.*",".*assword:", "#"])
        if x==1:
            s.sendline(password)
        if x==0:
            s.sendline("yes")
            s.expect("assword:")
            s.sendline(password)
	else:
	    s.sendline("\n")
        s.expect("#")
        s.logfile = open("/tmp/mylog", "w+")
        #s.sendline("ssh-keygen -t rsa")
        #s.expect(":")
        #s.sendline("\n")
        #x = s.expect([":", "(y/n)?"])
        #if x==0:
        #    s.sendline("\n")
        #if x==1:
     	
	#    s.sendline("y")
    	#    s.expect(":")
    	#    s.sendline("\n")
        #s.expect(":")
        #s.sendline("\n")
        #s.expect("#")
	print last_octet
	#import pdb;pdb.set_trace()
	print "ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.84.54.{0}".format(last_octet)
        s.sendline("ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.84.54.{0}".format(last_octet))
	print s.before
	print "ddd"
	print s.after
        x = s.expect(["Are you sure you want to continue connectin", "#", 'password:'])
        if x==0:
	    print "a"
            s.sendline("yes")
            s.expect("word:")
            s.sendline(password)
            s.expect("#")
	if x==2:
	    print "b"
            s.sendline(password)
            s.expect("#")
	else:
	    print "c"
	    s.sendline("\n")
	    s.expect("#")
    	last_octet += 1
        time.sleep(2)
        s.close()

pass_ssh_keys_to_nodes()
