#!/usr/bin/python
import pexpect
import sys

def generate_etc_hosts():
	last_octet = int(sys.argv[1])
	fp = open("/etc/hosts", "a+")
	username = "root"
	password = "c0ntrail123"
	hostname = "10.84.54"

	while(last_octet<=int(sys.argv[2])):
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
	    x=25
	    while(x<225):
		print "c"
        	s.sendline("printf \"10.84.54.{0} k8s-scale-test-vm{1}.contrail.juniper.net k8s-scale-test-vm{2} \" >> /etc/hosts".format(x,x,x))
		s.expect("#")
        	s.sendline("printf \"\\n\" >> /etc/hosts")
		s.expect("#")
		x+=1
	    last_octet += 1
	    s.close()
	    print "d"
		

generate_etc_hosts()
