import sys, os
import resource
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import time

device = "/dev/ttyAMA0"

options = ZWaveOption(device, config_path = "../python-openzwave/openzwave/config", user_path = ".", cmd_line = "")
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(True)
options.set_save_log_level("Debug")
options.set_logging(False)
options.lock()

print ("Memory use : {} Mo".format((resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0)))

network = ZWaveNetwork(options, log=None)

time_started = 0

print ("------------------------------")
print ("Waiting for network awaked : ")
print ("------------------------------")

for i in range(0,300):
  if network.state >= network.STATE_AWAKED:
    print (" done")
    print ("Memory use : {} Mo".format((resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0)))
    break
  else:
    sys.stdout.write(".")
    sys.stdout.flush()
    time_started += 1
    time.sleep(1.0)

if network.state < network.STATE_AWAKED:
  print (".")
  print ("Network is not awake but continue anyway")


print ("------------------------------")
print ("Use openzwave library : {}".format(network.controller.ozw_library_version))
print("Use python library : {}".format(network.controller.python_library_version))
print("Use ZWave library : {}".format(network.controller.library_description))
print("Network home id : {}".format(network.home_id_str))
print("Controller node id : {}".format(network.controller.node.node_id))
print("Controller node version : {}".format(network.controller.node.version))
print("Nodes in network : {}".format(network.nodes_count))

print("------------------------------------------------------------")
print("Waiting for network ready : ")
print("------------------------------------------------------------")
for i in range(0,300):
    if network.state>=network.STATE_READY:
        print(" done in {} seconds".format(time_started))
        break
    else:
        sys.stdout.write(".")
        time_started += 1
        #sys.stdout.write(network.state_str)
        #sys.stdout.write("(")
        #sys.stdout.write(str(network.nodes_count))
        #sys.stdout.write(")")
        #sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)


print("Memory use : {} Mo".format( (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0)))
if not network.is_ready:
    print(".")
    print("Network is not ready but continue anyway")

print("------------------------------------------------------------")
print("Controller capabilities : {}".format(network.controller.capabilities))
print("Controller node capabilities : {}".format(network.controller.node.capabilities))
print("Nodes in network : {}".format(network.nodes_count))
print("Driver statistics : {}".format(network.controller.stats))
print("------------------------------------------------------------")

for node in network.nodes:
  for val in network.nodes[node].get_switches():
    print ("Activate switch")
    network.nodes[node].set_switch(val, True)
    time.sleep(10.0)
    print ("Deactivate switch")
    network.nodes[node].set_switch(val, False)

    '''
    print("------------------------------------------------------------")
    print("{} - Name : {}".format(network.nodes[node].node_id,network.nodes[node].name))
    #print("{} - Manufacturer name / id : {} / {}".format(network.nodes[node].node_id,network.nodes[node].manufacturer_name, network.nodes[node].manufacturer_id))
    #print("{} - Product name / id / type : {} / {} / {}".format(network.nodes[node].node_id,network.nodes[node].product_name, network.nodes[node].product_id, network.nodes[node].product_type))
    #print("{} - Version : {}".format(network.nodes[node].node_id, network.nodes[node].version))
    print("{} - Command classes : {}".format(network.nodes[node].node_id,network.nodes[node].command_classes_as_string))
    #print("{} - Capabilities : {}".format(network.nodes[node].node_id,network.nodes[node].capabilities))
    #print("{} - Neigbors : {}".format(network.nodes[node].node_id,network.nodes[node].neighbors))
    #print("{} - Can sleep : {}".format(network.nodes[node].node_id,network.nodes[node].can_wake_up()))

    for cmd in network.nodes[node].command_classes:
        print("   ---------   ")
        #print("cmd = {}".format(cmd))
        values = {}
        for val in network.nodes[node].get_values_for_command_class(cmd) :
            values[network.nodes[node].values[val].object_id] = {
                'label':network.nodes[node].values[val].label,
                'help':network.nodes[node].values[val].help,
                'max':network.nodes[node].values[val].max,
                'min':network.nodes[node].values[val].min,
                'units':network.nodes[node].values[val].units,
                'data':network.nodes[node].values[val].data,
                'data_str':network.nodes[node].values[val].data_as_string,
                'genre':network.nodes[node].values[val].genre,
                'type':network.nodes[node].values[val].type,
                'ispolled':network.nodes[node].values[val].is_polled,
                'readonly':network.nodes[node].values[val].is_read_only,
                'writeonly':network.nodes[node].values[val].is_write_only,
                }
        print("{} - Values for command class : {} : {}".format(network.nodes[node].node_id,
                                    network.nodes[node].get_command_class_as_string(cmd),
                                    values))
    print("------------------------------------------------------------")
    '''

network.stop()

print ("Hello, World")
