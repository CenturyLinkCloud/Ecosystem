"""
bp_broker ping module.

Basic package to test end to end communication
"""


import json

import bpbroker


#####################################################

def Ping(rh):
	"""Echo source host and querystring back in response.

	:param *: No params required
	:returns src: Requesting IP address
	:returns data: Echoes entire provided querystring
	"""

	data = None
	try:
		data = json.loads(rh.qs['data'])
	except:
		data = {'_str': rh.qs['data']}
	rh.data = json.dumps({'src': rh.RequestingHost(), 'data': data})


