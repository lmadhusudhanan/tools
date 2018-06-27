from fabric.api import env
import os

#host1 = 'root@10.204.217.31'
#host2 = 'root@10.204.217.32'

k8s_scale_test_host = '10.84.25.1'

ext_routers = [('hooper','10.204.217.240')]                                                                                                                                                             
router_asn = 64512                                                                                                                                                                                        
public_vn_rtgt = 2225                                                                                                                                              
public_vn_subnet = '10.204.221.160/28'
host_build = 'stack@10.204.216.49'

#{env_roledefs}
#env.roledefs = {
#    'all': [host1,host2,host3,host4,host5,host6],
#    'cfgm': [host1, host2],
#    'webui': [host1],
#    'openstack': [host1],
#    'control': [host2, host3],
#    'collector': [host1],
#    'database': [host1, host2, host3],
#    'compute': [host4, host5, host6],
#    'build': [host_build]
#}

env.physical_routers={
'hooper'     : {       'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : 'hooper',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.217.240',
             }
}

env.hostnames = {
    'all': ['k8s_scale_test_vm1', 'k8s_scale_test_vm2']
}

env.ostypes = {
    host1:'centos',
    host2:'centos'
}

env.openstack_admin_password = 'contrail123'
env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host_build: 'stack@123',
}

reimage_param = os.getenv('REIMAGE_PARAM', 'centos-7.4-copy.qcow2')

vm_node_details = {
    'default': {
                'image_dest' : '/mnt/disk1/images/',
                'ram' : '16384',
                'server': k8s_scale_test_host,
                'vcpus' : '2',
                'disk_format' : 'qcow2',
                'image_source' : 'http://10.84.5.120/images/node_vm_images/%s.gz' % (reimage_param),
                },
    host1 : {  
                'name' : 'k8s_scale_test_vm1',
                'network' : [{'bridge' : 'br0', 'mac':'52:53:58:11:00:01'}
                            ],
            },
    host2 : {  
                'name' : 'k8s_scale_test_vm2',
                'network' : [{'bridge' : 'br0', 'mac':'52:53:58:11:00:02'}
                            ],
            }
}

env.ha = {
    'internal_vip' : '10.204.217.229'
}
ha_setup = True

minimum_diskGB=32
env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}
env.test_repo_dir='/home/stack/multi_interface_parallel/centos65/icehouse/contrail-test'
env.mail_from='contrail-build@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
multi_tenancy=True
env.interface_rename = True
env.enable_lbaas = True
enable_ceilometer = True
ceilometer_polling_interval = 60
env.encap_priority =  "'VXLAN','MPLSoUDP','MPLSoGRE'"
env.log_scenario='Multi-Node Virtual Testbed Sanity[mgmt, ctrl=data]'
env.ntp_server = '10.204.217.158'
