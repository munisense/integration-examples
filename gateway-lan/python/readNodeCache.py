import requests
import json
import struct

# Sample code to retrieve the node cache from the gateway. Every node cache entry consists of the following format:
# capability - see 2.3.2.3.6 MAC Capability Flags Field from the ZigBee Specification
# addr
#   nwkAddr - 16-bit NWK address of the node
#   eui - 64-bit IEEE address of the node
# Verify that the web interface is enabled on the gateway (visit the web interface and go to configuration > general page)

ip = "172.22.20.144" # Fill in the IP address of your gateway here.

url = "http://" + ip + "/zgd/nodes"

r = requests.get(url)
result = json.loads(r.text)

# Get list from dict

for key, value in result.items():
       for node in value:
            print json.dumps(node)
