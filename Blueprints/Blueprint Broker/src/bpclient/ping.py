"""
bp_client ping module.

Basic package to test end to end communication
"""


import json

import bpclient


#####################################################

def Ping(rh):
	"""Echo source host and querystring back in response.

	:param *: No params required
	:returns src: Requesting IP address
	:returns pong: Echoes entire provided querystring
	"""
	rh.send_response(200)
	rh.send_header('Content-Type','Application/json')
	rh.end_headers()

	rh.wfile.write(json.dumps({'src': rh.RequestingHost(), 'pong': rh.qs}))


