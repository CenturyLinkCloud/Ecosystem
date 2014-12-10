"""
bp_broker ping module.

Basic package to test end to end communication
"""


import json

import bpbroker


#####################################################

def Ping(var):
	ro = bpbroker.api.Response()
	ro.status = 200
	ro.response = json.dumps({'pong': var})
	
	return(ro)


