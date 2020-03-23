from inventory import *
from config import *
from flask import Flask, render_template, send_from_directory, jsonify, redirect
from flask import request, make_response, Response, url_for
import os
import requests
from app import app
from functools import wraps
import subprocess
import time
from json import dumps
from operator import itemgetter


#@app.before_request
#def before_request():
#    if not request.is_secure and app.env != "development":
#        url = request.url.replace("http://", "https://", 1)
#        code = 301
#        return redirect(url, code=code)


@app.route('/')
def index():
      print("1")
#      inventory()
      return redirect(url_for('inventory',_scheme="https",_external=True))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')






@app.route('/inventory/<string:machine_name>/delete_from_inventory', methods=['GET'])
def delete_from_inventory(machine_name):
   requests.delete(INVENTORY_API+machine_name)
   url="/inventory"
#   return redirect(url, code=302)
   return render_template("inventory.html",Secops_Link=Secops_Link, Icinga_Link=Icinga_Link)

@app.route('/inventory/<string:kernel_patch>', methods=['POST'])
def kernel_patch(kernel_patch):
      if request.form['submit'] == 'update patch':
          new_patch=request.form['new_patch']
          payload = {'patch': new_patch}
          headers = {'content-type': 'application/json'}
          r = requests.post(INVENTORY_kernel_URL, json=payload, headers=headers)
      return redirect(url_for('inventory',_scheme="https",_external=True))



@app.route('/inventory/<string:machine_name>', methods=['GET'])
def inventory_detail(machine_name):
      guests=''
      json_data = requests.get(INVENTORY_API).json()
      json_patch= requests.get(INVENTORY_kernel_URL).json()[0].get('patch')
      json_data=sorted(json_data, key=itemgetter('vm_inventory_name'))
      #print(type(json_data))
      #print(sorted(json_data,key="vm_inventory_name",reverse=True))
      #print(sort(json_data, sort_keys=True)
      VMs=get_VMs(json_data)
      env=get_env(json_data)
      types=get_type(json_data)
      ms=get_ms(json_data)
      inv_names=get_inv_name(json_data)
      patched=get_patched(json_data,json_patch)
      number_of_servers=len(VMs)
      # IPs=get_IPs(json_data)
      states=get_state(json_data)
      dcs=get_DCs(json_data)
      images=get_os(json_data)
      VM_image=get_VM(json_data,machine_name).get('os_version')
      if get_VM(json_data,machine_name).get('RAM_size_MB'):
           if int(get_VM(json_data,machine_name).get('RAM_size_MB'))<1024:
               VM_RAM=str(int(get_VM(json_data,machine_name).get('RAM_size_MB')))+' MB'
           else:
               VM_RAM=str(int(round(float(get_VM(json_data,machine_name).get('RAM_size_MB')/1024))))+' GB'
      else:
        VM_RAM='-'
      if get_VM(json_data,machine_name).get('number_of_cores'):
        VM_cpu=get_VM(json_data,machine_name).get('number_of_cores')
      else:
        VM_cpu='-'
      VM_kernel=get_VM(json_data,machine_name).get('kernel_version')
      VM_env=get_VM(json_data,machine_name).get('environment')
      VM_type=get_VM(json_data,machine_name).get('vmtype')
      VM_inv_name=get_VM(json_data,machine_name).get('vm_inventory_name')
      VM_inv_last_run=get_VM(json_data,machine_name).get('last_alive_signal')
      VM_dc=get_VM(json_data,machine_name).get('vm_dc_name')
      VM_microservices=str(get_VM(json_data,machine_name).get('microservices'))
      VM_free_disk=get_VM(json_data,machine_name).get('Disk_MB')[2]/1024/1024/1024
      VM_cpu_load_prcnt=get_VM(json_data,machine_name).get('cpu_load_prcnt')
      VM_free_ram=get_VM(json_data,machine_name).get('RAM_free_MB')
      # VM_IP=get_VM(json_data,machine_name).get('Internal_IP')

      mode=1
      return render_template("inventory.html",mode=mode,VMs=VMs,ms=ms,
      VM_type=VM_type,env=env, VM_free_ram=VM_free_ram,VM_cpu_load_prcnt=VM_cpu_load_prcnt,
      VM_free_disk=VM_free_disk,types=types,patched=patched,inv_names=inv_names,
      states=states,images=images,number_of_servers=number_of_servers,VM_image=VM_image,
      machine_name=machine_name,VM_env=VM_env,VM_kernel=VM_kernel,VM_cpu=VM_cpu,
      VM_RAM=VM_RAM,VM_inv_last_run=VM_inv_last_run,VM_microservices=VM_microservices,
      Secops_Link=Secops_Link,json_patch=json_patch, Icinga_Link=Icinga_Link,
      VM_dc=VM_dc, dcs=dcs )



@app.route('/inventory')
def inventory():
      json_patch= requests.get(INVENTORY_kernel_URL).json()[0].get('patch')
      json_data = requests.get(INVENTORY_API).json()
      json_data=sorted(json_data, key=itemgetter('vm_inventory_name'))
      VMs=get_VMs(json_data)
      types=get_type(json_data)
      inv_names=get_inv_name(json_data)
      dcs=get_DCs(json_data)
      ms=get_ms(json_data)
      patched=get_patched(json_data,json_patch)
      env=get_env(json_data)
      # IPs=get_IPs(json_data)
      states=get_state(json_data)
      images=get_os(json_data)
      number_of_servers=len(VMs)
      mode=0
      return render_template("inventory.html",mode=mode,VMs=VMs,ms=ms,env=env,states=states,
      images=images,types=types,patched=patched,inv_names=inv_names, dcs=dcs,
      number_of_servers=number_of_servers,Secops_Link=Secops_Link,json_patch=json_patch, Icinga_Link=Icinga_Link )
