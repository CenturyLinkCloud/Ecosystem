"""
bp_client discovery module.

Package to initiate UDP broadcast to local networks searching for existing BP Broker servers.
"""


import requests

import bpclient


#####################################################

def Discovery(name):
	"""Broadcast BP Broker discovery traffic to local networks, returing BP Broker that resonds.

	Broadcasts UDP packet to all local networks containing a BP Broker discovery query.
	If BP Broker is on one of these networks and contains the specified "name" in the service
	registry then it will respond.

	:param name: Services key to search to broadcast to bp broker servers
	:returns bpboker: Returns IP address of responding BP Broker or False if no response
	"""

	method_match = re.match("(.*)\.(.*)",method)

	r = requests.post("https://%s/%s/%s/" % (bpclient.BPBROKER,method_match.group(1),method_match.group(2)),params={'data': data},verify=False)
	return(r.text)


