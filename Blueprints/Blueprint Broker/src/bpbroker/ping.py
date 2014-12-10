"""
bp_broker ping module.

Basic package to test end to end communication
"""


import json

import bpbroker


#####################################################

def Ping(rh):
	rh.send_response(200)
	rh.send_header('Content-Type','Application/json')
	rh.end_headers()

	rh.wfile.write(json.dumps({'from': rh.address_string(), 'pong': rh.qs}))


