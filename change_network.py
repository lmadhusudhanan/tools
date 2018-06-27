#!/usr/local/bin/python3

import pexpect
import re
import time

def change_network_interface(bm_ip, interface_name="ens2", old_interface_name="eth0"):
    try:
        hostname = bm_ip
        username = "root"
        password = "c0ntrail123"
        #import pdb;pdb.set_trace()
        s = pexpect.spawn("ssh {0} -l {1}".format(hostname, username))
        x = s.expect([".*yes/no.*",".*assword:"])
        if x==1:
            s.sendline(password)
        if x==0:
            s.sendline("yes")
            s.expect("assword:")
            s.sendline(password)
        s.expect("#")
        s.logfile = open("/tmp/mylog", "wb+")
        s.sendline("virsh list")   # run a command
        s.expect("#")
        for line in open("/tmp/mylog", "rb"):
            line = line.decode('utf-8')
            if re.match(".*\s+(k8s_scale_test_vm.*)\s+running", line):
                vm_name = re.match(".*\s+(k8s_scale_test_vm.*)\s+running", line).group(1)
                print(vm_name)
                s.sendline("virsh console {0}".format(vm_name))
                s.expect("character")
                s.sendline("\n")
                x = s.expect(["login:", "#"])
                if x==0:    
                    s.sendline("root")
                    s.expect("assword:")
                    s.sendline("c0ntrail123")
                    s.expect("#")
                else:
                    s.expect("#")
                s.sendline("ifconfig -a")
                s.expect("#")
                s.sendline("sudo printf \"BOOTPROTO=dhcp\nDEVICE=ens2\nONBOOT=yes\nTYPE=Ethernet\nUSERCTL=no\" > /etc/sysconfig/network-scripts/ifcfg-eth0")
                s.expect("#")
                s.sendline("dhclient ens2")
                s.expect("#")
                s.sendcontrol("]")
                s.expect("#")
                print("done")
                time.sleep(0.3)
    
    except Exception as e:
        print("pxssh failed on login.")
        print(e)


start_ip_octet = 13
while (start_ip_octet<=13):
    print ("10.84.55.{0}".format(start_ip_octet))
    change_network_interface("10.84.55.{0}".format(start_ip_octet))
    start_ip_octet+=1

