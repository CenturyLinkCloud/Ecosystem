"""
bp_client ping module.

Basic package to test end to end communication
"""


import requests
import json

import bpclient


#####################################################

def Ping(data):
	"""Echo to BP Broker host adn recieve back echoed response.

	:param data: Data to be sent/echoed
	:returns pong: Original data in returned
	"""
	r = requests.post("https://%s/Ping/Ping/" % bpclient.BPBROKER,params={'data': data},verify=False)
	#print "%s: %s" % (bpclient.BPBROKER,data)


