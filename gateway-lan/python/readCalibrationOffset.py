import requests
import json
import struct

# Sample code to retrieve the current calibration value from a node.
# Verify that the web interface is enabled on the gateway (visit the web interface and go to configuration > general page)

ip = "172.22.20.144" # Fill in the IP address of your gateway here.

url = "http://" + ip + "/zgd/zcl/read"
DEFAULT_ENDPOINT_ID = 10
PROFILE_ID = 61696
SOUND_CLUSTER_ID = 37888
CALIBRATION_OFFSET_ATTRIBUTE_ID = 5

# Take the eui64 address of the node and split it up into parts to create an array of integers.
# E.g. 000d:6f00:04bc:73ab -> ["0x00", "0x0d", "0x6f", "0x00", "0x04", "0xbc", "0x73", "0xab"] -> [0, 13, 111, 0, 4, 188, 115, 171]
eui64 = [0, 13, 111, 0, 4, 188, 115, 171]

data = {"addr": {"eui": eui64},
        "endpoint": DEFAULT_ENDPOINT_ID,
        "profile": PROFILE_ID,
        "cluster": SOUND_CLUSTER_ID,
        "attributes": [CALIBRATION_OFFSET_ATTRIBUTE_ID]
        }

r = requests.post(url, data=json.dumps(data))
result = json.loads(r.text)

value = result["attributes"][0]["value"]

# Pack the two values together.
buffer = struct.pack("BB", value[0], value[1])
# Unpack the buffer as one value and apply scale.
calibration_output = struct.unpack("h", buffer)[0] / 10.0

print "Calibration: {} dB(A)".format(calibration_output)
