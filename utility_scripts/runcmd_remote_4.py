#!/usr/bin/python
import paramiko

def run_cmd_on_remote_server(cmd):

    last_octet = 25
    while(last_octet<27):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(
	    '10.84.54.{0}'.format(last_octet),
	    username="root",
	    password="c0ntrail123")
	stdin, stdout, stderr = client.exec_command(cmd)
	for line in stdout:
	    print line.strip('\n')

	client.close()


run_cmd_on_remote_server("yum install ansible vim git wget -y && wget -O /tmp/epel-release-latest-7.noarch.rpm https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && rpm -ivh /tmp/epel-release-latest-7.noarch.rpm && yum update -y")	
