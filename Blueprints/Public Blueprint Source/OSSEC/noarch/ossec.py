"""
ossec management extension to bpbroker.

This module's methods are accessible via the URL

	https://bpbroker:20443/ossec/

In order for this module to succcessfuly execute as part of an RPC it needs to be added to the config.json
as a top level key named "ossec".  Initial validation is done via this whitelist.

"""

import random
import string
import json


OSSEC_DIR = "/var/ossec"


#####################################################

print "Load"

def AddAgent(rh):
	"""Add agent to local ossec manager and return key."""

	print "in"
	global OSSEC_DIR

	# Make sure not already registered
	with open("%s/etc/client.keys") as f:  client_keys = f.read()
	print client_keys
	if re.search("\s%s\s" % rh.RequestingHost(),client_keys):
		rh.status = 500
		rh.status_message = "Unable to add requested host IP in use"

	else:
		# Find next agent

		# Generate key 
		key = ''.join(random.SystemRandom().choice(string.hexdigits) for _ in range(64))
		#rh.data = json.dumps(rh.qs)



