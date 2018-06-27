#!/usr/local/bin/python3

import yaml
import pdb
import sys
import paramiko

###################
# Arg1 - remote server IP
# Arg2 - username
# Arg3 - password
# Arg4 - pods-per-core value
##################


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(
    sys.argv[1],
    username=sys.argv[2],
    password=sys.argv[3])
sftp_client = client.open_sftp()
 
fp = sftp_client.open("/etc/origin/node/node-config.yaml", "r")
data = yaml.load(fp)
fp.close()

#modifications
try:
    data["kubeletArguments"]["pods-per-core"] = int(sys.argv[4])
except TypeError:
    print ("Remote file is empty. Aborting script !!")
    sys.exit(1)

fp = sftp_client.open("/etc/origin/node/node-config.yaml", "w")
yaml.dump(data, fp)
fp.close()
