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

def Register(access_key,name,data):
	"""Registers new service to service broker.

	Registers a new entry if none exists or returns error if entry already exists.
	Recommend using a name + key to mitigate misplaced overwrites

	CLI:
	> ./bpclient.py  -f json -b 127.0.0.1:20443 service register --name test2 --data '{"a": 3, "b": "foo"}'
	{"message": "Success", "data": {"a": 3, "last_write_ts": 1418760026, "b": "foo", "last_write_ip": "127.0.0.1"}, "success": true}

	REPL:
	>>> bpclient.services.Register(name='test6',data='{"a": 1}')
	{u'data': {u'a': 1,
	           u'last_write_ip': u'127.0.0.1',
	           u'last_write_ts': 1418760363},
	 u'message': u'Success',
	 u'success': True}

	>>> bpclient.services.Register(name='test5',data='my data')
	{u'data': {u'data': u'my data',
	           u'last_write_ip': u'127.0.0.1',
	           u'last_write_ts': 1418760632},
	 u'message': u'Success',
	 u'success': True}

	:param name: Unique registration name.  Often a name and a unique key.
	:param data: json object containing all data to associated with name
	"""

	r = requests.post("https://%s/services/Register/" % bpclient.BPBROKER,params={'access_key': access_key, 'name': name, 'data': data},verify=False)
	return(r.json())


def Replace(access_key,name,data):
	"""Replacing existing content (if any).

	CLI:
	> ./bpclient.py  -f text -b 127.0.0.1:20443 service register --name test1 --data 'original data'
	True	Success	{"last_write_ts": 1418761404, "data": "original data", "last_write_ip": "127.0.0.1"}
 	>./bpclient.py  -f text -b 127.0.0.1:20443 service replace --name test1 --data 'new data'
	True	Success	{"last_write_ts": 1418761411, "data": "new data", "last_write_ip": "127.0.0.1"}

	REPL:
	>>> bpclient.services.Register(name='test2',data='original data')
	{u'message': u'Success', u'data': {u'last_write_ts': 1418761514, u'data': u'original data', u'last_write_ip': u'127.0.0.1'}, u'success': True}

	>>> bpclient.services.Replace(name='test2',data='new data')
	{u'message': u'Success', u'data': {u'last_write_ts': 1418761523, u'data': u'new data', u'last_write_ip': u'127.0.0.1'}, u'success': True}

	:param name: Unique registration name.  Often a name and a unique key.
	:param data: json object containing all data to associated with name
	"""
	r = requests.post("https://%s/services/Replace/" % bpclient.BPBROKER,params={'access_key': access_key, 'name': name, 'data': data},verify=False)
	return(r.json())


def Delete(access_key,name):
	"""Remove keyed entry.  

	Returns scuccess=True whether key exists or not.

	CLI:
	> ./bpclient.py  -f text -b 127.0.0.1:20443 service delete --name test1
	True	Success

	REPL:
	>>> bpclient.services.Delete('test1')
	{u'message': u'Success', u'success': True}

	:param name: Unique registration name.  Often a name and a unique key.
	"""

	r = requests.post("https://%s/services/Delete/" % bpclient.BPBROKER,params={'access_key': access_key, 'name': name},verify=False)
	return(r.json())


def Update(access_key,name,data):
	"""Update existing entry.

	If no entry exists insert it.  If entry already exists for given key then merge data together with
	new data taking precedence.  Perform deep merge of data if it is a json object.

	CLI:
	> ./bpclient.py  -f text -b 127.0.0.1:20443 service update --name test4 --data '{"old_key": "old_data"}'
	True	Success	{"old_key": "old_data", "last_write_ts": 1418762954, "last_write_ip": "127.0.0.1"}
 	>./bpclient.py  -f text -b 127.0.0.1:20443 service update --name test4 --data '{"new_key": "new_data"}'
	True	Success	{"old_key": "old_data", "last_write_ts": 1418762962, "last_write_ip": "127.0.0.1", "new_key": "new_data"}

	REPL:
	>>> bpclient.services.Update(name='test3',data='{"orig_key": "orig_data"}')
	{u'data': {u'last_write_ip': u'127.0.0.1',
	           u'last_write_ts': 1418762718,
	           u'orig_key': u'orig_data'},
	 u'message': u'Success',
	 u'success': True}

	>>> bpclient.services.Update(name='test3',data='{"new_key": "new_data"}')
	{u'data': {u'last_write_ip': u'127.0.0.1',
	           u'last_write_ts': 1418762729,
	           u'new_key': u'new_data',
	           u'orig_key': u'orig_data'},
	 u'message': u'Success',
	 u'success': True}

	:param name: Unique registration name.  Often a name and a unique key.
	:param data: json object containing all data to associated with name
	"""

	r = requests.post("https://%s/services/Update/" % bpclient.BPBROKER,params={'access_key': access_key, 'name': name, 'data': data},verify=False)
	return(r.json())


def Get(access_key,name):
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

	r = requests.post("https://%s/services/Get/" % bpclient.BPBROKER,params={'access_key': access_key, 'name': name},verify=False)
	return(r.json())


def List(access_key,name):
	"""Alias for Get."""
	Get(access_key,name)


