"""
Access and modify saved/running config.

This is thread safe.

"""


import sys
import json
import threading

import bpbroker

default_config = {
	'api': {
	},
	'worker':  {
	},
	'_global':  {
		'healthcheck_freq_sec': 10,
	},
	'_config':  {
		'backup_freq_secs': 3600,
		'backup_retain_n': 24,
	},

	'ping':  { },
	'services':  { },
}


#####################################################


def ImportConfigString(cstr):
	try:
		with bpbroker.config.rlock:
			bpbroker.config.data =  dict(list(bpbroker.config.data.items()) + list(json.loads(cstr).items()))
	except Exception as e:
		raise(Exception("Unable to import configuration: %s" % str(e)))


def ImportConfigFile(cfile):
	try:
		f = open(cfile)
		ImportConfigString(f.read())
	except Exception as e:
		raise(Exception("unable to import config file %s: %s\n" % (cfile,str(e))))


class Config(object):

	def __init__(self, source=False):
		self.data = {}
		self.source = source
		self.rlock = threading.RLock()

		self.data = default_config
		if self.source:  self._Load()


	def __exit__(self, type, value, traceback):
		if self.source:  self.Save()


	def _Load(self):
		with self.rlock:
			try:
				with open(self.source) as fp:
					self.data =  dict(list(self.data.items()) + list(json.load(fp).items()))
			except:
				raise


	def Save(self):
		with self.rlock:
			try:
				with open(self.source,"w") as fp:
					self.data = json.load(fp)
			except:
				raise




