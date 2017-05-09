import requests
import json
import struct
import sys

# Sample code to recommission a node to a new pan id.
# WARNING:  If you are implementing this script and you sent a wrong command, you may end up with a node set to an
#           unknown pan id. If that happens you need to perform a hard reset of the node which will set it back to its
#           standard extended pan id: F113.
#           The node you are trying to recommission must be connected to the gateway that is sending these commands.
#           Otherwise it can not reach the node of course.
# Changing the extended pan id of the node is only the first part of creating a 'set' of a gateway + node. There must be a
# gateway with its extended pan id set to the same extended pan id as the node as well. Before recommissioning nodes and
# gateways it is recommended to draw a map of your network on a piece of paper and create a plan. Chaning the extended
# pan id of a gateway is done by going to the web interface and going to the Configuration -> ZigBee -> Settings page.
#
# Verify that the web interface is enabled on the gateway (visit the web interface and go to the Configuration > General page)
#
# The recommissioning process consists of two steps:
# 1) Set the attribute that stores the extended pan id to a new value.
# 2) Send the `Restart Device Command` to force the node to search for a new network to join, using the value from the
#    attribute that was set in step 1.

# ============================= Change these parameters to your need ==============================
# The IP address of the gateway that the node is currently connected with.
ip = "127.0.0.1"

# Take the eui64 address of the node and split it up into parts to create an array of integers.
# E.g. 000d:6f00:04bc:73ab -> ["0x00", "0x0d", "0x6f", "0x00", "0x04", "0xbc", "0x73", "0xab"] -> [0, 13, 111, 0, 4, 188, 115, 171]
eui64 = [0, 13, 111, 0, 4, 188, 115, 171]

# The extended pan id that the node is going to be recommissioned to. This example is F112. Remember that an extended pan
# id is a 64-bit value. Be sure to enter 8 values in this array.
new_extended_pan_id = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf1, 0x12]
# =================================================================================================

# Constants used by the rest of this script.
url = "http://" + ip + "/zgd/zcl"
DEFAULT_ENDPOINT_ID = 10
MUNISENSE_PROFILE_ID = 61696
COMMISSIONING_CLUSTER_ID = 21
EXTENDED_PAN_ID_ATTRIBUTE_ID = 1
IEEE_ADDRESS_DATATYPE_ID = 240
RESTART_DEVICE_COMMAND_ID = 0 # See Table 3.127 `Commands Received by the Commissioning Cluster Server` of the ZigBee Cluster Library.
WRITE_ATTRIBUTES_COMMAND_ID = 2 # See Table 2.9 `ZCL Command Frames` of the ZigBee Cluster Library.

# Set the extended pan id attribute on a node.
#
# :param eui64: The eui64 address of the node to send the command to. Must be an array with integer values for every
#               byte of the address. E.g. [0, 1, 2, 3, 4, 5, 6, 7]
# :param extended_pan_id: The new extended pan id. E.g. [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf1, 0x13] for F113.
def set_extended_pan_id_attribute(eui64, extended_pan_id):
    # Use the *-operator to unpack the new extended pan id array to separate positional arguments.
    data_payload = struct.pack("=HB8B", EXTENDED_PAN_ID_ATTRIBUTE_ID, IEEE_ADDRESS_DATATYPE_ID, *(extended_pan_id))
    data_payload = map(ord, data_payload)

    # Print the extended pan id for the user.
    print "Setting extended pan id to: " + "".join([format(byte, 'x') for byte in extended_pan_id])

    data = {"addr": {"eui": eui64},
            "endpoint": DEFAULT_ENDPOINT_ID,
            "profile": MUNISENSE_PROFILE_ID,
            "cluster": COMMISSIONING_CLUSTER_ID,
            "command": WRITE_ATTRIBUTES_COMMAND_ID,
            "global": True, # False to indicate the command acts across the entire profile, true to indicate the command is specific to a cluster
            "payload": data_payload
            }

    r = requests.post(url, data=json.dumps(data))

    # Print an error message if the response code is not 200.
    if(r.status_code != 200):
        print "Error! Response code not 200 after setting extended pan id attribute! Is the node joined to this gateway?"
        sys.exit(1)

    print "Done setting extended pan id."

    return

# Send the Restart Device Command to a node.
#
# :param eui64: The eui64 address of the node to send the command to. Must be an array with integer values for every
#               byte of the address. E.g. [0, 1, 2, 3, 4, 5, 6, 7]
def send_restart_device_command(eui64):
    # Create the payload for the Restart Device Command (options, delay, jitter)
    # See 3.15.2.3.1 `Restart Device Command` of the ZigBee Cluster Library.
    options = 0x00
    delay = 0x00
    jitter = 0x00
    data_payload = struct.pack("=bbb", options, delay, jitter)
    data_payload = map(ord, data_payload)

    print "Sending Restart Device Command"

    data = {"addr": {"eui": eui64},
            "endpoint": DEFAULT_ENDPOINT_ID,
            "profile": MUNISENSE_PROFILE_ID,
            "cluster": COMMISSIONING_CLUSTER_ID,
            "command": RESTART_DEVICE_COMMAND_ID,
            "global": False, # False to indicate the command acts across the entire profile, true to indicate the command is specific to a cluster
            "payload": data_payload
            }

    # Send the Restart Device Command to the gateway.
    r = requests.post(url, data=json.dumps(data))

    # Print an error message if the response code is not 200.
    if(r.status_code != 200):
        print "Error! Response code not 200 after sending Restart Device Command! "
        sys.exit(1)

    print "Done sending Restart Device Command"

    return

# Step 1
set_extended_pan_id_attribute(eui64, new_extended_pan_id)

# Step 2
send_restart_device_command(eui64)

print "Done"
