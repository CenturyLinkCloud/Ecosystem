"""
Access and modify saved/running config.

This is thread safe.

"""


import os
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
			bpbroker.config.Save()
	except Exception as e:
		print e
		raise(Exception("Unable to import configuration: %s" % str(e)))


def ImportConfigFile(cfile):
	try:
		with open(cfile) as f:  
			#cstr = f.read()
			#print cstr
			ImportConfigString(f.read())
			#ImportConfigString(cstr)
	except Exception as e:
		raise(Exception("Unable to import config file %s: %s\n" % (cfile,str(e))))


class Config(object):

	def __init__(self, source=False):
		self.data = {}
		self.source = source
		self.rlock = threading.RLock()

		if not self.source and os.name == 'posix' and os.path.exists("/usr/local/bpbroker/etc/bpbroker.json"):
			self.source = "/usr/local/bpbroker/etc/bpbroker.json"
		elif not self.source and os.name == 'nt' and os.path.exists("tbd"):
			# TODO - windows default configuration location
			pass
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


	def Save(self,source=False):
		if source:  self.source = source

		with self.rlock:
			try:
				with open(self.source,"w") as fp:
					self.data = json.dump(self.data,fp)
			except:
				raise




