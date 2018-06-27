#!/usr/bin/python

''' Generates testbed.py to generate multiple VMs '''

testbed_fp = open(
    "/tmp/testbed.py","w+")
EXT_ROUTERS = '[(\'hooper\',\'10.204.217.240\')]'
ROUTER_ASN = '64512'
PUBLIC_VN_RTGT = '2225'
PUBLIC_VN_SUBNET = '\'10.204.221.160/28\''
HOST_BUILD = '\'stack@10.204.216.49\''
VM_HOSTNAME_PREFIX = 'k8s_scale_test'
VM_IMAGE_DEFAULT = 'centos-7.4.qcow2'

def dec_to_hex(decimal_value):
    if decimal_value < 100:
        return decimal_value
    first_octet = decimal_value/10
    second_octet = decimal_value%10
    return str('{0:x}'.format(int(first_octet))).upper()+str(second_octet)

def construct_testbed_py(bm_vm_mapping):
    testbed_fp.write("from fabric.api import env \n")
    testbed_fp.write("import os \n")
    testbed_fp.write("\n")
    print "Defining host IPs"
    
    initial_count = 0
    last_octet = 25
    for bm in bm_vm_mapping:
        while(initial_count<200):
            testbed_fp.write("host{} = \'root@{}.{}\' \n".format(
	        initial_count+1, bm_vm_mapping[bm]["vm_ip_prefix"], last_octet))
            initial_count+=1
	    last_octet+=1
    testbed_fp.write("\n")

    print "Defining bare metal IP"
    for bm in bm_vm_mapping:
        testbed_fp.write("k8s_scale_test_host = \'{}\' \n".format(bm))

    testbed_fp.write("\n")
    testbed_fp.write("ext_routers = {} \n".format(EXT_ROUTERS))
    testbed_fp.write("router_asn = {} \n".format(ROUTER_ASN))
    testbed_fp.write("public_vn_rtgt = {} \n".format(PUBLIC_VN_RTGT))
    testbed_fp.write("public_vn_subnet = {} \n".format(PUBLIC_VN_SUBNET))
    testbed_fp.write("host_build = {} \n".format(HOST_BUILD))
    
    testbed_fp.write("env.physical_routers={ \n")
    testbed_fp.write("\'hooper\'     : {       \'vendor\': \'juniper\', \n")
    testbed_fp.write("                     \'model\' : \'mx\', \n")
    testbed_fp.write("                      \'asn\'   : \'64512\', \n")
    testbed_fp.write("                      \'name\'  : \'hooper\', \n")
    testbed_fp.write("                      \'ssh_username\' : \'root\', \n")
    testbed_fp.write("                      \'ssh_password\' : \'c0ntrail123\', \n")
    testbed_fp.write("                      \'mgmt_ip\'  : \'10.204.217.240\', \n")
    testbed_fp.write("              } \n")
    testbed_fp.write(" } \n")
     
    testbed_fp.write("env.hostnames = { \n")
    testbed_fp.write("     \'all\': [\'k8s_scale_test_vm1\', \'k8s_scale_test_vm2\'] \n")
    testbed_fp.write(" } \n")
     
    testbed_fp.write("env.ostypes = { \n")
    testbed_fp.write("     host1:\'centos\', \n")
    testbed_fp.write("     host2:\'centos\' \n")
    testbed_fp.write(" } \n")
     
    testbed_fp.write("env.openstack_admin_password = \'contrail123\' \n")
    testbed_fp.write("env.password = \'c0ntrail123\' \n")
    testbed_fp.write("env.passwords = { \n")
    testbed_fp.write("     host1: \'c0ntrail123\', \n")
    testbed_fp.write("     host_build: \'stack@123\', \n")
    testbed_fp.write(" }         \n")
   
    testbed_fp.write("\n")
    testbed_fp.write("reimage_param = os.getenv(\'REIMAGE_PARAM\', \'{}\') \n".format(VM_IMAGE_DEFAULT)) 
    testbed_fp.write("\n")

    testbed_fp.write("vm_node_details = { \n")
    testbed_fp.write("    \'default\': { \n")
    testbed_fp.write("                \'image_dest\' : \'/mnt/disk1/images/\', \n")
    testbed_fp.write("                \'ram\' : \'16384\', \n")
    testbed_fp.write("                \'server\': k8s_scale_test_host, \n")
    testbed_fp.write("                \'vcpus\' : \'2\', \n")
    testbed_fp.write("                \'disk_format\' : \'qcow2\', \n")
    testbed_fp.write("                \'image_source\' : \'http://10.84.5.120/images/node_vm_images/%s.gz\' % (reimage_param), \n")
    testbed_fp.write("                }, \n")

    host_count=1
    for bm in bm_vm_mapping:
        initial_count = 0
        while(initial_count<bm_vm_mapping[bm]["vm_count"]):
            testbed_fp.write("    host{} : {{ \n".format(host_count))
            testbed_fp.write("        \'name\' : \'{}_vm{}\', \n".format(VM_HOSTNAME_PREFIX, bm_vm_mapping[bm]["start_id"]+initial_count))
     	    testbed_fp.write("        \'server\': \'{}\', \n".format(bm))
            if bm_vm_mapping[bm]["start_id"]+initial_count < 10:
                testbed_fp.write("         \'network\' : [{{\'bridge\' : \'br0\', \'mac\':\'00:67:77:88:88:0{}\'}} \n".format(bm_vm_mapping[bm]["start_id"]+initial_count))
	    elif bm_vm_mapping[bm]["start_id"]+initial_count > 159:
		testbed_fp.write("         \'network\' : [{{\'bridge\' : \'br0\', \'mac\':\'00:67:77:88:89:{}\'}} \n".format(dec_to_hex(bm_vm_mapping[bm]["start_id"]+initial_count-100)))
            else:
                testbed_fp.write("         \'network\' : [{{\'bridge\' : \'br0\', \'mac\':\'00:67:77:88:88:{}\'}} \n".format(dec_to_hex(bm_vm_mapping[bm]["start_id"]+initial_count)))
            testbed_fp.write("                     ], \n")
 	    if initial_count==bm_vm_mapping[bm]["vm_count"]:
                testbed_fp.write("     } \n")
	    else:
                testbed_fp.write("     }, \n")
            initial_count+=1
	    host_count+=1
    testbed_fp.write("}\n")
    testbed_fp.write("\n")

    
    testbed_fp.write("env.ha = { \n")
    testbed_fp.write("    \'internal_vip\' : \'10.204.217.229\' \n")
    testbed_fp.write("} \n")
    testbed_fp.write("ha_setup = True \n")
    testbed_fp.write("\n")

    testbed_fp.write("minimum_diskGB=32 \n")
    testbed_fp.write("env.rsyslog_params = {\'port\':19876, \'proto\':\'tcp\', \'collector\':\'dynamic\', \'status\':\'enable\'} \n")
    testbed_fp.write("env.test_repo_dir=\'/home/stack/multi_interface_parallel/centos65/icehouse/contrail-test\' \n")
    testbed_fp.write("env.mail_from=\'contrail-build@juniper.net\' \n")
    testbed_fp.write("env.mail_to=\'dl-contrail-sw@juniper.net\' \n")
    testbed_fp.write("multi_tenancy=True \n")
    testbed_fp.write("env.interface_rename = True \n")
    testbed_fp.write("env.enable_lbaas = True \n")
    testbed_fp.write("enable_ceilometer = True \n")
    testbed_fp.write("ceilometer_polling_interval = 60 \n")
    testbed_fp.write("env.encap_priority =  \"\'VXLAN\',\'MPLSoUDP\',\'MPLSoGRE\'\" \n")
    testbed_fp.write("env.log_scenario=\'Multi-Node Virtual Testbed Sanity[mgmt, ctrl=data]\' \n")

    testbed_fp.write("env.ntp_server = \'10.204.217.158\' \n")
 

bm_vm_mapping_test = {
        "10.84.54.1": {"vm_count":2, "vm_ip_prefix":"10.84.54", "start_id":25, "vm_image":'centos-7.4.qcow2'}
}
bm_vm_mapping_test2 = {
        "10.84.54.1": {"vm_count":2, "vm_ip_prefix":"10.84.54", "start_id":25, "vm_image":'centos-7.4.qcow2'},
        "10.84.54.2": {"vm_count":2, "vm_ip_prefix":"10.84.54", "start_id":27, "vm_image":'centos-7.4.qcow2'}
}
bm_vm_mapping = {
        "10.84.55.12": {"vm_count":14, "vm_ip_prefix":"10.84.55", "start_id":25, "vm_image":'centos-7.4.qcow2'},
        "10.84.55.13": {"vm_count":14, "vm_ip_prefix":"10.84.55", "start_id":39, "vm_image":'centos-7.4.qcow2'}
}
construct_testbed_py(bm_vm_mapping) 
