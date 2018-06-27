#!/usr/bin/python
import paramiko

def run_cmd_on_remote_server(cmd):

    last_octet = 25
    while(last_octet<30):
	print last_octet
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(
	    '10.84.54.{0}'.format(last_octet),
	    username="root",
	    password="c0ntrail123")
	stdin, stdout, stderr = client.exec_command(cmd.format(last_octet))
	for line in stdout:
	    print line.strip('\n')

	client.close()
	last_octet += 1


#run_cmd_on_remote_server("printf \"nameserver 172.29.131.60 \" >> /etc/resolv.conf")
#run_cmd_on_remote_server("printf \"\\n\" >> /etc/resolv.conf")
#run_cmd_on_remote_server("printf \"10.84.54.2 b1s2.contrail.juniper.net  b1s2 \" >> /etc/hosts")
#run_cmd_on_remote_server("printf \"\\n\" >> /etc/hosts")
run_cmd_on_remote_server("yes | ssh b1s2")
