#!/usr/bin/python

import pexpect
import re
import time
import sys

def pass_ssh_keys_to_nodes():
    hostname = "10.84.54."
    username = "root"
    password = "c0ntrail123"
    
    last_octet = 25
    y=int(sys.argv[1])
    while(y<sys.argv[2]):
      try:
        hostname_new = hostname + str(y)
	print hostname_new
        s = pexpect.spawn("ssh {0} -l {1}".format(hostname_new, username))
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
        while(last_octet < 225):
	    print last_octet
	    print "ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.84.54.{0} -f".format(last_octet)
	    try:
                s.sendline("ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.84.54.{0} -f".format(last_octet))
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
		s = pexpect.spawn("ssh {0} -l {1}".format(hostname, username))
        	x = s.expect([".*yes/no.*",".*assword:"])
        	if x==1:
            	    s.sendline(password)
        	if x==0:
            	    s.sendline("yes")
                    s.expect("assword:")
            	    s.sendline(password)
        	s.expect("#")
		continue
            last_octet += 1
	    time.sleep(2)
	y += 1
        s.close()
	last_octet = 25
      except pexpect.TIMEOUT:
	print "pexpect timeout in outer loop. Re-trying"
	continue

pass_ssh_keys_to_nodes()
