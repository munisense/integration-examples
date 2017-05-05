import requests
import json
import struct
import sys

# Sample code to set the calibration value of a node.
# Verify that the web interface is enabled on the gateway (visit the web interface and go to configuration > general page)
# Note: The calibration value has a scale of 0.1
#
# Input: 10 -> calibration will be 1.0 dB
# Input: 1 -> calibration will be 0.1 dB
# Input: -10 -> calibration will be -1.0 dB
# Input: -1 -> calibration will be -0.1 dB

ip = "127.0.0.1" # Fill in the IP address of your gateway here.

url = "http://" + ip + "/zgd/zcl"
DEFAULT_ENDPOINT_ID = 10
PROFILE_ID = 61696
SOUND_CLUSTER_ID = 37888
CALIBRATION_OFFSET_ATTRIBUTE_ID = 5
COMMAND_ID = 2
DATATYPE_ID = 41

# Take the eui64 address of the node and split it up into parts to create an array of integers.
# E.g. 000d:6f00:04bc:73ab -> ["0x00", "0x0d", "0x6f", "0x00", "0x04", "0xbc", "0x73", "0xab"] -> [0, 13, 111, 0, 4, 188, 115, 171]
eui64 = [0, 13, 111, 0, 4, 188, 115, 171]

if (len(sys.argv) < 2):
    print "Please supply a calibration value"
    sys.exit()

# Get the calibration value to use from the first argument given to this script.
calibration_value = int(sys.argv[1])

data_payload = struct.pack("=HBh", CALIBRATION_OFFSET_ATTRIBUTE_ID, DATATYPE_ID, calibration_value)
data_payload = map(ord, data_payload)

data = {"addr": {"eui": eui64},
        "endpoint": DEFAULT_ENDPOINT_ID,
        "profile": PROFILE_ID,
        "cluster": SOUND_CLUSTER_ID,
        "command": COMMAND_ID,
        "global": True,
        "payload": data_payload
        }

r = requests.post(url, data=json.dumps(data))

result = json.loads(r.text)["payload"][0]
if (result == 0):
    print "Done"
else:
    print "Could not set value"
