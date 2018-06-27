#!/usr/local/bin/python3

import paramiko

def run_cmd_on_remote_server():

    last_octet_master = 22 
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        '10.84.54.{0}'.format(last_octet_master),
	username="root",
	password="c0ntrail123")
    last_octet=25
    while(last_octet<225):
        print(last_octet)
        stdin, stdout, stderr = client.exec_command("printf \"10.84.54.{0} k8s-scale-test-vm{1}.contrail.juniper.net k8s-scale-test-vm{2}\\n\"".format(
            last_octet, last_octet, last_octet) + " >> /etc/hosts" )
#        for line in stdout:
#            print(line.strip('\n'))
        last_octet += 1

    client.close()


#run_cmd_on_remote_server("printf \"nameserver 172.29.131.60 \" >> /etc/resolv.conf")
#run_cmd_on_remote_server("printf \"\\n\" >> /etc/resolv.conf")
#run_cmd_on_remote_server("printf \"10.84.54.22 b5s18.contrail.juniper.net  b5s18 \" >> /etc/hosts")
#run_cmd_on_remote_server("printf \"\\n\" >> /etc/hosts")
#run_cmd_on_remote_server("chattr -i /etc/resolv.conf")
#run_cmd_on_remote_server("printf \"search cluster.local englab.juniper.net juniper.net \\nnameserver 172.29.131.60 \\nnameserver 10.84.54.{0} \\n \" > /etc/resolv.conf")
#run_cmd_on_remote_server("chattr +i /etc/resolv.conf")
run_cmd_on_remote_server()
#run_cmd_on_remote_server("printf \"NM_CONTROLLED=yes \\n\" >> /etc/sysconfig/network-scripts/ifcfg-eth0")
#run_cmd_on_remote_server("mkdir /etc/origin/node/; touch /etc/origin/node/resolv.conf")
