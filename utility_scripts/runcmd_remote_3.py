#!/usr/local/bin/python3
import paramiko

def run_cmd_on_remote_server(cmd):

    last_octet = 25
    while(last_octet<53):
        print('10.84.55.{0}'.format(last_octet))
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            '10.84.55.{0}'.format(last_octet),
            username="root",
            password="c0ntrail123")
        cmd_new = cmd+str(last_octet)
        stdin, stdout, stderr = client.exec_command(cmd_new)
        for line in stdout:
            print(line.strip('\n'))
        client.close()
        last_octet += 1
        cmd_new = cmd

run_cmd_on_remote_server("hostnamectl set-hostname  k8s-scale-test-55-vm")
