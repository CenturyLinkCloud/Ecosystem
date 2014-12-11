"""
bp_broker service broker bundle.

Service registration, listing, and object querying
"""


import re
import time
import json

import bpbroker


#####################################################

def Register(rh):
	"""Registers new service to service broker.

	Registers a new entry if none exists or returns error if entry already exists.
	Recommend using a name + key to mitigate misplaced overwrites

	:param name: Unique registration name.  Often a name and a unique key.
	:param data: json object containing all data to associated with name
	:returns success: bool success
	:returns data: query result for key 'name'
	"""

	# Validate parameters
	error = False
	data = []
	try:
		data = json.loads(rh.qs['data'])
	except:
		error = "Unable to parse data json format"
	if 'name' not in rh.qs:  error = "Missing name parameter"
	elif 'data' not in rh.qs:  error = "Missing data parameter"
	elif 'last_write_ip' in data:  error = "Used reserved data name last_write_ip"
	elif 'last_write_ts' in data:  error = "Used reserved data name last_write_ts"

	# Set data
	elif data:  
		with bpbroker.config.rlock:
			if rh.qs['name'] in bpbroker.config.data['services']:  error = "Entry exists, cannot register"
			else:  
				bpbroker.config.data['services'][rh.qs['name']] = \
					dict(data.items() + {'last_write_ip': rh.RequestingHost(), 'last_write_ts': int(time.time())}.items())

	# return results
	if error:  rh.send_error(400, error)
	else:  Get(rh)


def Replace(rh):
	"""Replacing existing content (if any).

	:param name: Unique registration name.  Often a name and a unique key.
	:param data: json object containing all data to associated with name
	:returns success: bool success
	:returns data: query result for key 'name'
	"""
	Delete(rh)
	Register(rh)


def Delete(rh):
	"""Remove keyed entry.

	:param name: Unique registration name.  Often a name and a unique key.
	:returns success: bool success
	"""


def Update(rh):
	"""Update existing entry.

	If no entry exists insert it.  If entry already exists for given key then merge data together with
	new data taking precedence.

	:param name: Unique registration name.  Often a name and a unique key.
	:param data: json object containing all data to associated with name
	:returns success: bool success
	:returns data: query result for key 'name'
	"""


def Get(rh):
	"""Return data associated with given key.

	Returns all data associated with key unless specific fields are provided.

	:param name: Unique registration name.  Often a name and a unique key.
	:returns success: bool success
	:returns data: query result for key 'name'
	"""


def List(rh):
	"""Alias for Get."""
	Get(rh)


