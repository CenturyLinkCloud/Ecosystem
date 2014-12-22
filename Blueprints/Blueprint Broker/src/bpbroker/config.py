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

	'example_extension_module':  { },
	'ping':  { },
	'services':  { },
}


#####################################################


def ImportConfigString(cstr):
	print "String follows:\n%s" % cstr


def ImportConfigFile(cfile):
	try:
		f = open(cfile)
		ImportconfigString(f.read())
	except Exception as e:
		print "b"
		sys.stderr.write("Fatal error importing config file %s error: %s\n" % (cfile,str(e)))
		sys.exit(1)


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




