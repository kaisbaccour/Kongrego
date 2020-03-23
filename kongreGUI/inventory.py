#!/opt/python3/bin/python3.4
import requests
import json
from datetime import datetime
from config import *
import time

def get_VMs(json_data):
      VMs=[]
      for i in range(len(json_data)):
          if ('vmname' in json_data[i] ) :
             VMs.append(json_data[i]['vmname'])
          else:
             VMs.append("")
      return VMs

def get_VM(json_data,machine_name):
      for i in range(len(json_data)):
          if ( json_data[i].get('vmname')==machine_name ):
             return json_data[i]

      return json_data[0]


def get_inv_name(json_data):
      env=[]
      for i in range(len(json_data)):
          if ('vm_inventory_name' in json_data[i] ) :
             env.append(json_data[i]['vm_inventory_name'])
          else:
             env.append("")
      return env
def get_DCs(json_data):
      dcs=[]
      for i in range(len(json_data)):
          if ('vm_dc_name' in json_data[i] ) :
             dcs.append(json_data[i]['vm_dc_name'])
          else:
             dcs.append("")
      return dcs

def get_type(json_data):
      types=[]
      for i in range(len(json_data)):
          if ('vmtype' in json_data[i] ) :
             types.append(json_data[i]['vmtype'])
          else:
             types.append("")
      return types

def get_env(json_data):
      env=[]
      for i in range(len(json_data)):
          if ('environment' in json_data[i] ) :
             env.append(json_data[i]['environment'])
          else:
             env.append("")
      return env

def get_os(json_data):
      os=[]
      for i in range(len(json_data)):
          if ('os_version' in json_data[i] ) :
             os.append(json_data[i]['os_version'])
          else:
             os.append("")
      return os

def get_ms(json_data):
      ms=[]
      for i in range(len(json_data)):
          if ('microservices' in json_data[i] ) :
             ms.append(json_data[i]['microservices'])
          else:
             ms.append("")
      return ms

#def get_patched(json_data,json_patch):
#      patched=[]
#      for i in range(len(json_data)):
#          if ('kernel_version' in json_data[i] ) :
#             env.append(json_data[i]['vmtype'])
#          else:
#             env.append("")
#      return env


#def get_patched(json_data,json_patch):
#      patched=[]
#      for i in range(len(json_data)):
#          if ('kernel_version' in json_data[i] ) :
#             kernel_version=json_data[i]['kernel_version']
#
#             if (kernel_version == CURRENT_KERNEL) :
#                 patched.append(1)
#             else:
#                 patched.append(0)
#          else:
#             patched.append(2)
#
#      return patched

def get_patched(json_data,json_patch):
      patched=[]
      for i in range(len(json_data)):
          if ('kernel_version' in json_data[i] ) :
             kernel_version=json_data[i]['kernel_version']

             if (kernel_version == json_patch) :
                 patched.append(1)
             else:
                 patched.append(0)
          else:
             patched.append(2)

      return patched

def get_state(json_data):
      states=[]
      for i in range(len(json_data)):
          if ('last_alive_signal' in json_data[i] ) :
             last_seen=json_data[i]['last_alive_signal']
             last_seen=datetime.strptime(last_seen, '%Y/%m/%d %H:%M:%S')
             current_time=datetime.now()
             FMT = '%H:%M:%S'
             tdelta = current_time - last_seen
#because of time sync problem between inventory machine and this application we added the 86400 condition to be removed
             if (tdelta.seconds < TOLERATED_TIME_OF_NON_RESPONSE_FROM_INVENTORY_AGENT_TO_CONSIDER_DOWN) :  #if we didn't receive a signal from the VM for more than 5 minutes + 30 seconds extra time
                 states.append(1)
             else:
                 states.append(0)
          else:
             states.append(2)

      return states
