"""
ossec management extension to bpbroker.

This module's methods are accessible via the URL

	https://bpbroker:20443/ossec/

In order for this module to succcessfuly execute as part of an RPC it needs to be added to the config.json
as a top level key named "ossec".  Initial validation is done via this whitelist.

"""

import subprocess
import random
import string
import json
import re

import bpbroker

OSSEC_DIR = "/var/ossec"


#####################################################


def AddAgent(rh):
	"""Add agent to local ossec manager and return key."""

	global OSSEC_DIR

	# Make sure not already registered
	with open("%s/etc/client.keys" % OSSEC_DIR) as f:  client_keys = f.readlines()

	if 'data' not in rh.qs or re.search("^a-z0-9\-",rh.qs['data'].lower()):
		rh.status = 500
		rh.status_message = "Invalid source host name content"
	elif re.search("\s%s\s" % rh.RequestingHost(),''.join(client_keys)):
		rh.status = 500
		rh.status_message = "Unable to add requested host IP in use"

	else:
		# Find next agent
		try:
			id = str(int(re.sub("\s.*","",sorted(client_keys)[-1]))+1).zfill(3)
		except IndexError:
			id = "001"

		# Generate key 
		key = ''.join(random.SystemRandom().choice(string.hexdigits) for _ in range(64))

		# Append to client_keys file
		with bpbroker.config.rlock:
			with open("%s/etc/client.keys" % OSSEC_DIR,"aw") as f:
				f.write("%s %s %s %s\n" % (id,rh.qs['data'],rh.RequestingHost(),key))
			subprocess.Popen(["%s/bin/ossec-control" % OSSEC_DIR, "restart"], stdout=subprocess.PIPE).communicate()

		# Export encoded key
		rh.data = "%s %s %s %s" % (id,rh.qs['data'],rh.RequestingHost(),key)


def RemoveAgent(rh):
	rh.status = 501
	rh.status_message = "Not implemented"


