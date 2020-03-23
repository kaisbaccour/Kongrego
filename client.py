#from __future__ import print_function
import requests



import os
import sys
import socket
import netifaces
import json
import psutil
import platform
import multiprocessing
from psutil import virtual_memory
import datetime
import subprocess


inventory_services_file = '/etc/kongrego/services'
inventory_env_file = '/etc/kongrego/env'
url = sys.argv[1]
mem = virtual_memory()

# Define the result dict
results = {}

# Fuction for retrieving interfaces and IP addresses
def get_interfaces():
    interfaces = {}
    for interface in netifaces.interfaces():
        ip_addresses = netifaces.ifaddresses(interface)
        try:
            interfaces[interface] = ip_addresses[netifaces.AF_INET]
        except:
            pass
    return interfaces

# Function for getting open IP port combinations
def get_connections(ip_ver):
    ip_ports = set()
    for conn in psutil.net_connections(kind=ip_ver):
        ip = conn[3][0]
        port = conn[3][1]
        s = ":"
        ip_port = s.join((ip, str(port)))
        ip_ports.add(ip_port)
    return(list(ip_ports))

# Function for sending the result to the api
def send_result(url, data):
    payload = data
#    payload = data.encode('utf8')
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json=payload, headers=headers)
    print (r)

# Function for getting the hostname hostname
def get_inventory_hostname():
    if os.path.isfile(inventory_hostname_file):
        f = open(inventory_hostname_file, 'r')
        hostname = f.read()
        hostname = hostname.rstrip()
        return hostname
    else:
        return ''

# Function for getting if the machine should be monitored
def get_inventory_monitoring():
    if os.path.isfile(inventory_monitor_file):
        f = open(inventory_monitor_file, 'r')
        monitor = f.read()
        monitor = monitor.rstrip()
        return monitor
    else:
        return ''

# Function for getting the environment of the machine
def get_inventory_env():
    if os.path.isfile(inventory_env_file):
        f = open(inventory_env_file, 'r')
        env = f.read()
        env = env.rstrip()
        return env
    else:
        return ''

# Function for getting if the machine should be backed-up
def get_inventory_backup():
    if os.path.isfile(inventory_backup_file):
        f = open(inventory_backup_file, 'r')
        backup = f.read()
        backup = backup.rstrip()
        return backup
    else:
        return ''

#Function for getting the kernel version
def get_kernel_version():
    return platform.platform()

# Function for getting the os version
def get_os_version():
    os_version_file = None
    # For CentOS and Red Hat
    if os.path.isfile('/etc/redhat-release'):
        os_version_file = '/etc/redhat-release'
        f = open(os_version_file, 'r')
        os_version = f.read()
        os_version = os_version.rstrip()
        return os_version

    else:
        return ''


###########################################################################
#                               Main                                     ##
###########################################################################

results["vmname"] = socket.gethostname()
results["environment"] = get_inventory_env()
results["number_of_cores"] = multiprocessing.cpu_count()
results["RAM_size_MB"] = mem.total/(1024.**2)
results["os_version"] = get_os_version()
results["kernel_version"] = get_kernel_version()
results["interfaces"] = get_interfaces()
results=json.dumps(results)
results=json.loads(results)
print (type(results))
send_result(url, results)
