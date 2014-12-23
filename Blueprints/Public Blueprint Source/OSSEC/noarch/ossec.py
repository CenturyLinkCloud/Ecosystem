"""
ossec management extension to bpbroker.

This module's methods are accessible via the URL

	https://bpbroker:20443/ossec/

In order for this module to succcessfuly execute as part of an RPC it needs to be added to the config.json
as a top level key named "ossec".  Initial validation is done via this whitelist.

The module has access to all methods within the request handler passed along as the variable rh.
By default the following values are set - change them as needed.  This is the content tht's returned
to the requesting client:

	rh.error = 200
	rh.error_message = ''
	rh.content_type = "Application/json"
	rh.data = ''

"""

import random
import string
import json


#####################################################


def AddAgent(rh):
	"""Add agent to local ossec manager and return key."""

	# Generate key 
	key = ''.join(random.SystemRandom().choice(string.hexdigits) for _ in range(64))
	#rh.data = json.dumps(rh.qs)

	# Where you to choose an errored response you may set the following:
	#rh.status = 500
	#rh.status_message = "End client visible message text explaining 500 error"

print AddAgent(object)

