
#######INVENTORY#####################
INVENTORY_API='http://<inventory_url>:5001/api/inventory'
INVENTORY_kernel_URL='http://clrv0000114061.ic.ing.net:5001/api/kernel_patch'
#####################################

####################################
#CURRENT_KERNEL="Linux-3.10.0-957.12.2.el7.x86_64-x86_64-with-redhat-7.6-Maipo"
TOLERATED_TIME_OF_NON_RESPONSE_FROM_INVENTORY_AGENT_TO_CONSIDER_DOWN=15 + 1*60  #if we didn't receive a signal from the VM for more than 1 minutes + 15 seconds extra time
####################################
