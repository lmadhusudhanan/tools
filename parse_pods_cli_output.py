#!/usr/local/bin/python3

import paramiko
import re
import subprocess

#stdin, stdout, stderr = client.exec_command("oc get pods -n ctest-ns1-98045229 -o wide")
command = "oc get pods -n ctest-ns1-98045229 -o wide"
#command = ["oc get pods", "-n", "ctest-ns1-98045229", "-o", "wide"]

p = subprocess.Popen(command, universal_newlines=True, 
shell=True, stdout=subprocess.PIPE, 
stderr=subprocess.PIPE)
text = p.stdout.read()
retcode = p.wait()
#import pdb;pdb.set_trace()
#print text
total=0

pattern = "^ctest.*\s+\d+\/\d+\s+(ContainerCreating|Pending|Running)\s+\d+\s+\d+h\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(k8s-scale-test-vm\d+).*$"
node_count = {}
#print p.stdout
for line in text.split("\n"):
    #print line
    if re.match(pattern, line):
        #print "match"
        node = re.match(pattern, line).group(3)
        if node in node_count.keys():
            node_count[node] += 1
        else:
            node_count[node] = 1

for k,v in node_count.iteritems():
    print (str(k) + "  : "+str(v))
    total = total + int(v)
    print ("total is : "+str(total))
