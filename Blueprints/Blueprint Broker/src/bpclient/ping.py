"""
bp_client ping module.

Basic package to test end to end communication
"""


import requests
import json

import bpclient


#####################################################

def Ping(access_key,data):
	"""Echo to BP Broker host adn recieve back echoed response.

	With payload data=test, receives json object:
	{"src": "127.0.0.1", "pong": {"data": "test"}}

	:param data: Data to be sent/echoed
	:returns pong: Original data in returned
	"""
	r = requests.post("https://%s/ping/Ping/" % bpclient.BPBROKER,params={'data': data, 'access_key': access_key},verify=False)
	return(r.json())


