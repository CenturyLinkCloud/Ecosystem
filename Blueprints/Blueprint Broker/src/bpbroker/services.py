"""
bp_broker service broker bundle.

Service registration, listing, and object querying
"""


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

	# Replace entry

	# 
	rh.send_response(200)
	rh.send_header('Content-Type','Application/json')
	rh.end_headers()

	with bpbroker.config.rlock:
		bpbroker.config.data['services']['']
	rh.wfile.write(json.dumps({'from': rh.RequestingHost(), 'pong': rh.qs}))


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


def Get(rh)
	"""Return data associated with given key.

	Returns all data associated with key unless specific fields are provided.

	:param name: Unique registration name.  Often a name and a unique key.
	:returns success: bool success
	:returns data: query result for key 'name'
	"""


def List(rh):
	"""Alias for Get."""
	Get(rh)


