from fabric.api import env 
import os 

host173 = 'root@10.84.54.95' 
host174 = 'root@10.84.54.96' 
host175 = 'root@10.84.54.97' 
host176 = 'root@10.84.54.98' 
host177 = 'root@10.84.54.99' 
host178 = 'root@10.84.54.100' 
host179 = 'root@10.84.54.101' 
host180 = 'root@10.84.54.102' 
host181 = 'root@10.84.54.103' 
host182 = 'root@10.84.54.104' 
host183 = 'root@10.84.54.105' 
host184 = 'root@10.84.54.106' 
host185 = 'root@10.84.54.107' 
host186 = 'root@10.84.54.108' 

k8s_scale_test_host = '10.84.54.10' 

ext_routers = [('hooper','10.204.217.240')] 
router_asn = 64512 
public_vn_rtgt = 2225 
public_vn_subnet = '10.204.221.160/28' 
host_build = 'stack@10.204.216.49' 
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
     'all': ['k8s_scale_test_vm95',
	'k8s_scale_test_vm96',
	'k8s_scale_test_vm97',
	'k8s_scale_test_vm98',
	'k8s_scale_test_vm99',
	'k8s_scale_test_vm100',
	'k8s_scale_test_vm101',
	'k8s_scale_test_vm102',
	'k8s_scale_test_vm103',
	'k8s_scale_test_vm104',
	'k8s_scale_test_vm105',
	'k8s_scale_test_vm106',
	'k8s_scale_test_vm107',
	'k8s_scale_test_vm108'
	] 
 } 
env.ostypes = { 
     host173:'centos', 
     host174:'centos', 
     host175:'centos', 
     host176:'centos', 
     host177:'centos', 
     host178:'centos', 
     host179:'centos', 
     host180:'centos', 
     host181:'centos', 
     host182:'centos', 
     host183:'centos', 
     host184:'centos',
     host185:'centos',
     host186:'centos'
 } 
env.openstack_admin_password = 'contrail123' 
env.password = 'c0ntrail123' 
env.passwords = { 
     host173: 'c0ntrail123', 
     host174: 'c0ntrail123', 
     host175: 'c0ntrail123', 
     host176: 'c0ntrail123', 
     host177: 'c0ntrail123', 
     host178: 'c0ntrail123', 
     host179: 'c0ntrail123', 
     host180: 'c0ntrail123', 
     host181: 'c0ntrail123', 
     host182: 'c0ntrail123', 
     host183: 'c0ntrail123', 
     host184: 'c0ntrail123', 
     host185: 'c0ntrail123', 
     host186: 'c0ntrail123',
     host_build: 'stack@123', 
 }         

reimage_param = os.getenv('REIMAGE_PARAM', 'centos-7.4.qcow2') 

vm_node_details = { 
    'default': { 
                'image_dest' : '/mnt/disk1/images/', 
                'ram' : '16384', 
                'server': k8s_scale_test_host, 
                'vcpus' : '2', 
                'disk_format' : 'qcow2', 
                'image_source' : 'http://10.84.5.120/images/node_vm_images/%s.gz' % (reimage_param), 
                }, 
    host173 : { 
        'name' : 'k8s_scale_test_vm95', 
        'server': '10.84.54.10', 
         'network' : [{'bridge' : 'br0', 'mac':'00:66:77:88:88:95'} 
                     ], 
     }, 
    host174 : { 
        'name' : 'k8s_scale_test_vm96', 
        'server': '10.84.54.10', 
         'network' : [{'bridge' : 'br0', 'mac':'00:66:77:88:88:96'} 
                     ], 
     }, 
    host175 : { 
        'name' : 'k8s_scale_test_vm97', 
        'server': '10.84.54.10', 
         'network' : [{'bridge' : 'br0', 'mac':'00:66:77:88:88:97'} 
                     ], 
     }, 
    host176 : { 
        'name' : 'k8s_scale_test_vm98', 
        'server': '10.84.54.10', 
         'network' : [{'bridge' : 'br0', 'mac':'00:66:77:88:88:98'} 
                     ], 
     }, 
    host177 : { 
        'name' : 'k8s_scale_test_vm99', 
        'server': '10.84.54.10', 
         'network' : [{'bridge' : 'br0', 'mac':'00:66:77:88:88:99'} 
                     ], 
     }, 
    host178 : { 
        'name' : 'k8s_scale_test_vm100', 
        'server': '10.84.54.10', 
         'network' : [{'bridge' : 'br0', 'mac':'00:66:77:88:88:9A'} 
                     ], 
     }, 
    host179 : { 
        'name' : 'k8s_scale_test_vm101', 
        'server': '10.84.54.10', 
         'network' : [{'bridge' : 'br0', 'mac':'00:66:77:88:88:9B'} 
                     ], 
     }, 
    host180 : { 
        'name' : 'k8s_scale_test_vm102', 
        'server': '10.84.54.10', 
         'network' : [{'bridge' : 'br0', 'mac':'00:66:77:88:88:9C'} 
                     ], 
     }, 
    host181 : { 
        'name' : 'k8s_scale_test_vm103', 
        'server': '10.84.54.10', 
         'network' : [{'bridge' : 'br0', 'mac':'00:66:77:88:88:9D'} 
                     ], 
     }, 
    host182 : { 
        'name' : 'k8s_scale_test_vm104', 
        'server': '10.84.54.10', 
         'network' : [{'bridge' : 'br0', 'mac':'00:66:77:88:88:9E'} 
                     ], 
     }, 
    host183 : { 
        'name' : 'k8s_scale_test_vm105', 
        'server': '10.84.54.10', 
         'network' : [{'bridge' : 'br0', 'mac':'00:66:77:88:88:9F'} 
                     ], 
     }, 
    host184 : { 
        'name' : 'k8s_scale_test_vm106', 
        'server': '10.84.54.10', 
         'network' : [{'bridge' : 'br0', 'mac':'00:66:77:88:88:A0'} 
                     ], 
     }, 
    host185 : { 
        'name' : 'k8s_scale_test_vm107', 
        'server': '10.84.54.10', 
         'network' : [{'bridge' : 'br0', 'mac':'00:66:77:88:88:A1'} 
                     ], 
     }, 
    host186 : { 
        'name' : 'k8s_scale_test_vm108', 
        'server': '10.84.54.10', 
         'network' : [{'bridge' : 'br0', 'mac':'00:66:77:88:88:A2'} 
                     ], 
     }, 
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
