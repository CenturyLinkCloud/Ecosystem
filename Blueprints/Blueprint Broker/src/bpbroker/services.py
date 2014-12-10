"""
bp_broker ping module.

Basic package to test end to end communication
"""


import json

import bpbroker


#####################################################

def Register(rh):
	"""Registers new service to service broker.

	Registers a new entry or overwrites and existing on if entry already exists for name.
	Recommend using a name + key to mitigate misplaced overwrites

	:param name: Unique registration name.  Often a name and a unique key.
	:param *:
	:returns :
	rh.send_response(200)
	rh.send_header('Content-Type','Application/json')
	rh.end_headers()

	with bpbroker.config.rlock:
		bpbroker.config.data['services']['
	rh.wfile.write(json.dumps({'from': rh.RequestingHost(), 'pong': rh.qs}))


