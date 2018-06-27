#!/usr/local/bin/python3
import paramiko
from threading import Thread
import time

def exec_cmd_thread(cmd, last_octet):
    print ("Executing {0} on server {1}".format(cmd, last_octet))
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
	'10.84.55.{0}'.format(last_octet),
         username="root",
         password="c0ntrail123")
    stdin, stdout, stderr = client.exec_command(cmd)
    exit_status = stdout.channel.recv_exit_status()
    print("exit status is {}".format(exit_status))
    for line in stdout:
        print(line.strip('\n'))
    client.close()

def run_cmd_on_remote_server(cmd):

    lock = False
    last_octet = 25
    threads = []
    while(last_octet<30):
        time.sleep(1)
        print ("Creating new thread")
        print (last_octet)
        if not lock:
            print ("Acquiring lock...")
            lock = True
            try:
                threads.append(
		    Thread(
		        target=exec_cmd_thread ,
		        args=(cmd_new, last_octet)))
                cmd_new = ""
                lock = False
                print ("Releasing lock...")
            except Exception:
                print ("Exception: Retrying... ")
                lock = False
                cmd_new = ""
                continue
        else:
            print ("Waiting for lock to be release ... Retrying")
            continue
        last_octet += 1
    
    print ("Starting all threads")
    for thread in threads:
        thread.start()
        time.sleep(0.5)

    print ("Waiting for all threads to finish")
    for thread in threads:
        thread.join()
        time.sleep(0.5)


#run_cmd_on_remote_server("sudo pip install --upgrade pip && sudo pip install netaddr && yes y | sudo yum install NetworkManager && sudo systemctl start NetworkManager && systemctl enable NetworkManager ")
run_cmd_on_remote_server("sudo yum -y install docker &")
