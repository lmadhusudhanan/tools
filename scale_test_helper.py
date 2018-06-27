#!/usr/local/bin/python3

import re
import pdb
import paramiko
import time
import shlex
import subprocess

from ansible.vars.manager import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager

class ScaleTestHelper(object):
    ''' Helper class for scale testing checks '''

    def __init__(self):
        self.loader = DataLoader()

    def _load_inventory(self):
        
        self.inventory = InventoryManager(
            loader=self.loader,
            sources=self.ose_install_path)

    def _read_variables(self):
        variables = VariableManager(
            loader=self.loader,
            inventory=self.inventory)
        self.variables_dict = variables.get_vars()

    def read_testbed_data(self, ose_install_path):
        ''' Using OSE install file, we read the testbed details '''

        self.ose_install_path = ose_install_path
        self._load_inventory()
        self._read_variables()

    def _ping_check(self, master_ip, ip_list, master_username="root", master_password="c0ntrail123"):
        ''' Returns True if ping is successful '''
            
        #create paramiko object to master
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                master_ip,
                username=master_username,
                password=master_password)
        except Exception:
            print("ERROR: Error connecting to Master {} ".format(master_ip))
            return False
        for ip in ip_list:
            try:
                print("INFO: Pinging from {} to {}".format(master_ip, ip))
                client.exec_command("ping -c 1 {}".format(ip), timeout=2)
            except Exception:
                print("ERROR: PING Connectivity Issue with slave {} from master {}".format(ip, master_ip))
                return False
            print("DEBUG: Ping was successful")
        client.close()
        return True

    def _ssh_check(self, master_ip, ip_list, master_username="root", master_password="c0ntrail123"):
        ''' Returns True if SSH is successful '''
        
        #create paramiko object to master
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                master_ip,
                username=master_username,
                password=master_password)
        except Exception:
            print("ERROR: Error connecting to Master {} ".format(master_ip))
            return False
        for ip in ip_list:
            try:
                print("INFO: Trying from {} to {}".format(master_ip, ip))
                client.exec_command("ssh {}".format(ip), timeout=2)
            except Exception:
                print("ERROR: SSH Connectivity Issue with slave {} from master {}".format(ip, master_ip))
                return False
            print("DEBUG: SSH was successful")
            time.sleep(0.1)

        client.close()
        return True

    def _system_pods_check(self, master_ip, master_username="root", master_password="c0ntrail123"):
        cmd = "oc get pods -n kube-system -o wide"
        failed = False
        pattern = "^(.*contrail.*?)\s+\d+\/\d+\s+(Error|CrashLoopBackOff|ContainerCreating|Pending|Running)\s+\d+\s+\d+[h|m|s]\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(.*).*$"
        node_info = {}
        #create paramiko object to master
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                master_ip,
                username=master_username,
                password=master_password)
        except Exception:
            print("ERROR: Error connecting to Master {} ".format(master_ip))
            return False
        try:
            print("INFO: Checking system pods on master {}".format(master_ip))
            stdin, stdout, stderr = client.exec_command(cmd)
            for line in stdout:
                if "No resources found" in line:
                    print ("No system PODS are up !!")
                    return False
                if re.match(pattern, line):
                    match_obj = re.match(pattern, line)
                    node = match_obj.group(1)
                    ip_address = match_obj.group(3)
                    state = match_obj.group(2)
                    hostname = match_obj.group(4)
                    node_info[node] = {'state': state, 'hostname': hostname, 'ip_address': ip_address}
            for k in node_info.keys():
                if "Running" not in node_info[k]["state"]:
                    print(str(k) + " : " + ">>>>>>>>>> ERROR")
                    print(node_info[k])
                    failed = True
                else:
                    continue
                    #print(str(k) + " : " + str(node_info[k]))
        except Exception as e:
            print("Exception while trying to check system pods on master {}".format(master_ip))
            print(str(e))
            return False
        client.close()
        if failed:
            return False
        return True

    def _user_pods_check(self, master_ip, master_username="root", master_password="c0ntrail123"):
        cmd = "oc get namespace"
        failed = False
        pattern = "(ctest.*)\s+Active\s+\d+[h|m|s]"
        namespace_list = []
        #create paramiko object to master
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(
                master_ip,
                username=master_username,
                password=master_password)
        except Exception:
            print("ERROR: Error connecting to Master {} ".format(master_ip))
            return False
        try:
            print("INFO: Checking user pods on master {}".format(master_ip))
            stdin, stdout, stderr = client.exec_command(cmd)
            print("INFO: Get all active user namespace")
            for line in stdout:
                if re.match(pattern, line):
                    match_obj = re.match(pattern, line)
                    namespace_list.append( match_obj.group(1))

            for namespace in namespace_list:
                print("DEBUG: Below Pods are not in running state in namespace {}".format(namespace))
                print("*********************************************************************************")
                stdin, stdout, stderr = client.exec_command("oc get pods -n {} -o wide  | grep -v Running".format(namespace))
                for line in stdout:
                    failed = True
                    print (line)
                print("*********************************************************************************")
        except Exception as e:
            print("Exception while trying to check system pods on master {}".format(master_ip))
            print(str(e))
            return False
        client.close()
        if failed:
            return False
        return True

    def slave_hosts_ping_check(self):
        ''' Checks if ping is successful from master nodes '''
        for master in self.variables_dict['groups']['masters']:
            return self._ping_check(
                master_ip=master,
                ip_list=self.variables_dict['groups']['nodes'])

    def slave_hosts_ssh_check(self):
        ''' Checks if SSH is successful from master nodes to slave nodes '''
        for master in self.variables_dict['groups']['masters']:
            return self._ssh_check(
                master_ip=master,
                ip_list=self.variables_dict['groups']['nodes'])

    def system_pod_status_check(self):
        ''' Checks if system pods are up and running fine '''
        for master in self.variables_dict['groups']['masters']:
            return self._system_pods_check(master_ip=master)

    def user_pod_status_check(self):
        ''' Checks if user pods are up and running fine '''
        for master in self.variables_dict['groups']['masters']:
            return self._user_pods_check(master_ip=master)
