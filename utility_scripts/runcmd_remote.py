#!/usr/bin/python
import paramiko
import sys
import thread

def exec_cmd(server_ip, cmd):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(
	    server_ip,
	    username="root",
	    password="c0ntrail123")
	chan = client.get_transport().open_session()
	print "running '%s'" % cmd
	stdin, stdout, stderr = client.exec_command(cmd)
	print "exit status: %s" % chan.recv_exit_status()
	#for line in stdout:
	#    print line.strip('\n')

	client.close()


def run_cmd_on_remote_server(cmd):

    last_octet = int(sys.argv[1])
    print sys.argv
    while(last_octet<int(sys.argv[2])):
	print "starting new thread"
	thread.start_new_thread(exec_cmd, ("10.84.54.{0}".format(last_octet), cmd))
	last_octet+=1


run_cmd_on_remote_server("yum install ansible vim git wget -y && wget -O /tmp/epel-release-latest-7.noarch.rpm https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && rpm -ivh /tmp/epel-release-latest-7.noarch.rpm && yum update -y")	
