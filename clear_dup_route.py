#!/usr/bin/env python3

from netmiko import ConnectHandler
from getpass import getpass
import os
import subprocess
import paramiko

static_ip = input("Enter static ip of affected user: ")
emp_num = input("Enter employee number of affected user: ")
print("Login for asa firewall")
uusername = input("Username: ")
upassword = getpass()
secret = input("enable secret")

#find the ip route from the static ip input
def find_route():    
    #password = getpass()
    #secret = getpass("Enter secret: ")

    cisco1 = {
        "device_type": "cisco_asa",
        "host": "",
        "username": uusername,
        "password": upassword,
        "secret": secret,
    }

    # Show command that we execute.
    command = "show route {}".format(static_ip)

    with ConnectHandler(**cisco1) as net_connect:
        net_connect.enable()
        print("net_connect.find_prompt()")
        output = net_connect.send_command(command)
        print(output)

    # Automatically cleans-up the output so that only the show output is returned
    s = output.split()
    global route_ip1
    global route_ip2
    global mod_route_ip1
    global mod_route_ip2
    route_ip1 = s[33]
    route_ip2 = s[-14]
    print("")
    mod_route_ip1 = route_ip1.rstrip(route_ip1[-1])
    mod_route_ip2 = route_ip2.rstrip(route_ip2[-1])
    print("Route found via Route 1: {} Route2: {}".format(mod_route_ip1, mod_route_ip2))
    sel_route = input("Clear Route? Enter 1 or 2: or CTRL+C to quit")
    print("")

    global del_route
    del_route = ""

    if sel_route == "1":
        del_route = mod_route_ip1
    elif sel_route == "2":
        del_route = mod_route_ip2
    else:
        print("Invalid input")

    print(input("Press Enter to Proceed with session logoff if more than one route is found, or CTRL+C to quit"))

    net_connect.disconnect()

#END


#login to backup server and find the firewall the route exists on

def find_fw():
    # login to backup server where fw configs are kept
    host = ""
    port = 22
    username = uusername
    password = upassword

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    # Show command that we execute.
    grep_cmd = "grep {} * | grep address".format(del_route)
    stdin, stdout, stderr = ssh.exec_command('cd /opt/svc_fwauto_prod/fwbkp && {}'.format(grep_cmd))
    for i in stdout:
        print(i)
        g = i.split()
    gg = g[0]
    global fw_name
    fw_name = gg.rstrip(gg[-1])
    print(fw_name)

    ssh.close()

#END


#login to firewall, enable mode, execute vpn-session logoff command with employee number
def logoff_username():
    #password = getpass()
    #secret = getpass("Enter secret: ")
    cisco2 = {
        "device_type": "cisco_asa",
        "host": fw_name,
        "username": uusername,
        "password": upassword,
        "secret": secret,
    }

    # vpn-session command we execute to logoff user
    logoff = "vpn-sessiondb logoff name {}".format(emp_num)

    with ConnectHandler(**cisco2) as net_connect:
        net_connect.enable()
        print("net_connect.find_prompt()")
        output = net_connect.send_command(logoff)

    print("")
    print(output)
    print("")

    net_connect.disconnect()

#END

find_route()
find_fw()
logoff_username()
