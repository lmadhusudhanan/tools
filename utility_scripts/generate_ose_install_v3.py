#!/usr/local/bin/python3

import pexpect

def generate_etc_hosts():
    fp = open("/tmp/gen_hosts.txt", "w+")
    for i in range(25,53):
        fp.write("10.84.55.{0} openshift_hostname=k8s-scale-test-vm{1}".format(i,i))
        fp.write("\n")


generate_etc_hosts()
