#!/usr/local/bin/python3

import paramiko

def run_cmd_on_remote_server(cmd):

    last_octet = 99
    while(last_octet<101):
        print(last_octet)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
	    '10.84.54.{0}'.format(last_octet),
	    username="root",
	    password="c0ntrail123")
        stdin, stdout, stderr = client.exec_command(cmd.format(last_octet))
        for line in stdout:
            print(line.strip('\n'))

        client.close()
        last_octet += 1


#run_cmd_on_remote_server("printf \"nameserver 172.29.131.60 \" >> /etc/resolv.conf")
#run_cmd_on_remote_server("printf \"\\n\" >> /etc/resolv.conf")
#run_cmd_on_remote_server("printf \"10.84.54.22 b5s18.contrail.juniper.net  b5s18 \" >> /etc/hosts")
#run_cmd_on_remote_server("printf \"\\n\" >> /etc/hosts")
#run_cmd_on_remote_server("chattr -i /etc/resolv.conf")
#run_cmd_on_remote_server("printf \"search cluster.local englab.juniper.net juniper.net \\nnameserver 172.29.131.60 \\nnameserver 10.84.54.{0} \\n \" > /etc/resolv.conf")
#run_cmd_on_remote_server("chattr +i /etc/resolv.conf")
#run_cmd_on_remote_server("printf \"BOOTPROTO=dhcp\\nDEVICE=ens2\\nONBOOT=yes\\nTYPE=Ethernet\\nUSERCTL=no\\nNM_CONTROLLED=yes\\n\" > /etc/sysconfig/network-scripts/ifcfg-eth0")
#run_cmd_on_remote_server("mkdir /etc/origin; mkdir /etc/origin/node/; touch /etc/origin/node/resolv.conf")
#run_cmd_on_remote_server("yum install ansible vim git wget -y && wget -O /tmp/epel-release-latest-7.noarch.rpm https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && rpm -ivh /tmp/epel-release-latest-7.noarch.rpm && yum update -y")
#run_cmd_on_remote_server("sudo yum -y install python-pip && pip install --upgrade pip && sudo pip install netaddr && yes y | sudo yum install NetworkManager && sudo systemctl start NetworkManager && systemctl enable NetworkManager ")
run_cmd_on_remote_server("sudo yum remove -y ansible && pip install ansible")
