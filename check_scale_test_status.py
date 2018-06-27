#!/usr/local/bin/python3

import pdb

from scale_test_helper import ScaleTestHelper


#create helper object
class ScaleTestCheck(ScaleTestHelper):
    def __init__(self):
        super().__init__()

    def scale_test_health_check(self, skip_ping_check=False, skip_ssh_check=False, skip_system_pod_check=False, skip_user_pod_check=False):
        #Ping check
        if not skip_ping_check:
            if self.slave_hosts_ping_check():
                print("INFO: PING check was successful")
            else:
                print("ERROR: PING check was not successul")

        #SSH Check
        if not skip_ssh_check:
            if self.slave_hosts_ssh_check():
                print("INFO: SSH check was successful")
            else:
                print("ERROR: SSH check was unsuccessful")

        #DNS Check on nodes

        #

        #System Pods Status Check
        if not skip_system_pod_check:
            if self.system_pod_status_check():
                print("INFO : System PODS are up and running fine !")
            else:
                print("ERROR: System PODS failure !")
            
        
        #User Pods Status Check
        if not skip_user_pod_check:
            if self.user_pod_status_check():
                print("INFO : User PODS are up and running fine !")
            else:
                print("ERROR: User PODS failure !")

obj = ScaleTestCheck()
obj.read_testbed_data(ose_install_path="/Users/lmadhusudhan/Downloads/testbeds/ose-install.txt")
obj.scale_test_health_check(
    skip_ping_check=True,
    skip_ssh_check=True,
    skip_system_pod_check=False,
    skip_user_pod_check=True)

