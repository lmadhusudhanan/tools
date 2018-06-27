#!/usr/bin/python

VM_START_IP_PREFIX = "10.84.54"
VM_START_IP_ID = 25
VM_START_HOSTNAME_PREFIX = "scale_vm_"
VM_START_HOSTNAME_ID = 25
GW_IP = "10.84.55.254"
DHCP_FP = open("/tmp/dhcp_template_partial","a+")

def dec_to_hex(decimal_value):
    if decimal_value < 100:
	return decimal_value
    first_octet = decimal_value/10
    second_octet = decimal_value%10
    return str('{0:x}'.format(int(first_octet))).upper()+str(second_octet)

def add_dhcp_entry(hostname, addr_id, gw_ip):
    DHCP_FP.write("      host {}{{\n".format(hostname))
    if int(addr_id) < 10:
        DHCP_FP.write("      hardware ethernet            00:67:77:88:88:0{};\n".format(addr_id))
    if int(addr_id) > 159:
        DHCP_FP.write("      hardware ethernet            00:67:77:88:89:{};\n".format(dec_to_hex(addr_id-100)))
    else:
        DHCP_FP.write("      hardware ethernet            00:67:77:88:88:{};\n".format(dec_to_hex(addr_id)))
    DHCP_FP.write("      fixed-address                {}.{};\n".format(VM_START_IP_PREFIX, addr_id))
    DHCP_FP.write("      option domain-search         \"englab.juniper.net\", \"juniper.net\";\n")
    DHCP_FP.write("      option domain-name           \"englab.juniper.net\" ;\n")
    DHCP_FP.write("      #option ntp-servers          $next_server ;\n")
    DHCP_FP.write("      option host-name             \"{}\";\n".format(hostname))
    DHCP_FP.write("      option routers               {};\n".format(gw_ip))
    DHCP_FP.write("      option domain-name-servers   10.84.5.100, 8.8.8.8;\n")
    DHCP_FP.write("    }\n")
   
while (VM_START_HOSTNAME_ID < 226):
    add_dhcp_entry(VM_START_HOSTNAME_PREFIX+str(VM_START_HOSTNAME_ID), VM_START_IP_ID, GW_IP)
    VM_START_HOSTNAME_ID+=1
    VM_START_IP_ID = VM_START_HOSTNAME_ID
    
    

