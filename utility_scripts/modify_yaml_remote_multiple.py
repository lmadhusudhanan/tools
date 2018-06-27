#!/usr/local/bin/python3

import yaml
import pdb
import sys
import paramiko

###################
# Arg1 - remote server IP (not used in this script. just fill some dummy value)
# Arg2 - username
# Arg3 - password
# Arg4 - pods-per-core value
##################

last_octet = 25
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
while (last_octet<27):

    client.connect(
        '10.84.54.{0}'.format(last_octet),
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

    with sftp_client.open("/etc/origin/node/node-config.yaml", "w") as fp:
        import pdb;pdb.set_trace()
        yaml.dump(data, fp, default_flow_style=False)
        fp.flush()
        fp.close()
    
    client.close()
    last_octet+=1
