"""
bp_broker service broker bundle.

Service registration, listing, and object querying
"""


import re
import time
import json
import requests

import bpclient


#####################################################

def Register(name,data):
	"""Registers new service to service broker.

	Registers a new entry if none exists or returns error if entry already exists.
	Recommend using a name + key to mitigate misplaced overwrites

	CLI:
	> ./bpclient.py  -f json -b 127.0.0.1:20443 service register --name test2 --data '{"a": 3, "b": "foo"}'
	{"message": "Success", "data": {"a": 3, "last_write_ts": 1418760026, "b": "foo", "last_write_ip": "127.0.0.1"}, "success": true}

	REPL:
	>>> bpclient.services.Register(name='test6',data='{"a": 1}')
	{"message": "Success", "data": {"a": 1, "last_write_ts": 1418760363, "last_write_ip": "127.0.0.1"}, "success": true}
	{u'data': {u'a': 1,
	           u'last_write_ip': u'127.0.0.1',
	           u'last_write_ts': 1418760363},
	 u'message': u'Success',
	 u'success': True}

	>>> bpclient.services.Register(name='test5',data='my data')
	{"message": "Success", "data": {"last_write_ts": 1418760632, "data": "my data", "last_write_ip": "127.0.0.1"}, "success": true}
	{u'data': {u'data': u'my data',
	           u'last_write_ip': u'127.0.0.1',
	           u'last_write_ts': 1418760632},
	 u'message': u'Success',
	 u'success': True}

	:param name: Unique registration name.  Often a name and a unique key.
	:param data: json object containing all data to associated with name
	"""

	r = requests.post("https://%s/services/Register/" % bpclient.BPBROKER,params={'name': name, 'data': data},verify=False)
	return(r.json())


def Replace(rh):
	"""Replacing existing content (if any).

	:param name: Unique registration name.  Often a name and a unique key.
	:param data: json object containing all data to associated with name
	:returns success: bool success
	:returns message: status message
	:returns data: query result for key 'name'
	"""
	Delete(rh,silent=True)
	Register(rh)


def Delete(name):
	"""Remove keyed entry.

	CLI:
	> ./bpclient.py  -f text -b 127.0.0.1:20443 service delete --name test2
	True	Success	{"last_write_ts": 1418760685, "data": "xxxx", "last_write_ip": "127.0.0.1"}

	REPL:
	>>> bpclient.services.Get('test1')
	{u'data': {u'data': u'xxxx',
	           u'last_write_ip': u'127.0.0.1',
	           u'last_write_ts': 1418760626},
	 u'message': u'Success',
	 u'success': True}

	>>> bpclient.services.Get('nokey')
	{u'message': u'Entry not found', u'data': {}, u'success': False}

	:param name: Unique registration name.  Often a name and a unique key.
	"""

	r = requests.post("https://%s/services/Delete/" % bpclient.BPBROKER,params={'name': name},verify=False)
	return(r.json())


def Update(rh):
	"""Update existing entry.

	If no entry exists insert it.  If entry already exists for given key then merge data together with
	new data taking precedence.

	:param name: Unique registration name.  Often a name and a unique key.
	:param data: json object containing all data to associated with name
	:returns success: bool success
	:returns message: status message
	:returns data: query result for key 'name'
	"""

	# Validate parameters
	data = []
	try:
		data = json.loads(rh.qs['data'])
	except:
		rh.send_error(400, "Unable to parse data json format")
		return()
	if 'name' not in rh.qs:  rh.send_error(400,"Missing name parameter")
	elif 'data' not in rh.qs:  rh.send_error(400,"Missing data parameter")
	elif 'last_write_ip' in data:  rh.send_error(400,"Used reserved data name last_write_ip")
	elif 'last_write_ts' in data:  rh.send_error(400,"Used reserved data name last_write_ts")

	# Set data
	elif data:  
		with bpbroker.config.rlock:
			if rh.qs['name'] not in bpbroker.config.data['services']:  bpbroker.config.data['services'][rh.qs['name']] = {}
			bpbroker.config.data['services'][rh.qs['name']] = \
				dict(bpbroker.config.data['services'][rh.qs['name']].items() + data.items() + 
				     {'last_write_ip': rh.RequestingHost(), 'last_write_ts': int(time.time())}.items())
			Get(rh)


def Get(name):
	"""Return data associated with given key.

	Returns all data associated with key unless specific fields are provided.

	CLI:
	> ./bpclient.py  -f text -b 127.0.0.1:20443 service get --name test2
	True	Success	{"last_write_ts": 1418760685, "data": "xxxx", "last_write_ip": "127.0.0.1"}

	REPL:
	>>> bpclient.services.Get('test1')
	{u'data': {u'data': u'xxxx',
	           u'last_write_ip': u'127.0.0.1',
	           u'last_write_ts': 1418760626},
	 u'message': u'Success',
	 u'success': True}

	>>> bpclient.services.Get('nokey')
	{u'message': u'Entry not found', u'data': {}, u'success': False}

	:param name: Unique registration name.  Often a name and a unique key.
	"""

	r = requests.post("https://%s/services/Get/" % bpclient.BPBROKER,params={'name': name},verify=False)
	return(r.json())


def List(name):
	"""Alias for Get."""
	Get(name)


