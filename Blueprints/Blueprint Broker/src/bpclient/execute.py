"""
bp_client ping module.

Basic package to test end to end communication
"""


import requests

import bpclient


#####################################################

def Execute(method,data):
	"""Execute custom RPC on BP Broker server passing along data payload.

	

	:param data: Data to be sent/echoed
	:returns : Sends returns all output to stdout
	"""
	r = requests.post("https://%s/ping/Ping/" % bpclient.BPBROKER,params={'data': data},verify=False)
	return(r.json())


