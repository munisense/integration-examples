import requests
import json
import struct

# Sample code to retrieve the model identifier (node name) from a node if you know the EUI64 address of the node.
# Verify that the web interface is enabled on the gateway (visit the web interface and go to configuration > general page)

ip = "172.22.20.144" # Fill in the IP address of your gateway here.

url = "http://" + ip + "/zgd/zcl/read"
DEFAULT_ENDPOINT_ID = 10
PROFILE_ID = 61696
BASIC_CLUSTER_ID = 0
MODEL_IDENTIFIER_ATTRIBUTE_ID = 5

# Take the eui64 address of the node and split it up into parts to create an array of integers.
# E.g. 000d:6f00:04bc:73ab -> ["0x00", "0x0d", "0x6f", "0x00", "0x04", "0xbc", "0x73", "0xab"] -> [0, 13, 111, 0, 4, 188, 115, 171]
eui64 = [0, 13, 111, 0, 4, 188, 115, 171]

data = {"addr": {"eui": eui64},
        "endpoint": DEFAULT_ENDPOINT_ID,
        "profile": PROFILE_ID,
        "cluster": BASIC_CLUSTER_ID,
        "attributes": [MODEL_IDENTIFIER_ATTRIBUTE_ID]
        }

r = requests.post(url, data=json.dumps(data))
result = json.loads(r.text)

# The results will be an array of integers, they need to be converted to ASCII
response_as_array = result["attributes"][0]["value"]

# Remove the first array item as this is a Form Feed character (decimal value 12)
response_as_array.pop(0)

# Convert the array items to ASCII and store the entire result
model_identifier_readable = "".join(str(unichr(val)) for val in response_as_array)

print "Model Identifier: " + model_identifier_readable
