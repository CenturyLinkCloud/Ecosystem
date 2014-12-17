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
	rh.send_response(200)
	rh.send_header('Content-Type','Application/json')
	rh.end_headers()

	data = None
	try:
		data = json.loads(rh.qs['data'])
	except:
		data = {'_str': rh.qs['data']}
	print data
	rh.wfile.write(json.dumps({'src': rh.RequestingHost(), 'data': data}))


