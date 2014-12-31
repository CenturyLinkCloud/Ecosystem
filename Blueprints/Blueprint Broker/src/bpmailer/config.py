"""
Access and modify saved/running config.

This is thread safe.

"""


import os
import sys
import json
import socket
import threading

import bpmailer

default_config = {
	"_bpmailer":  {
		"mail_from_user": "bpmailer@%s" % socket.gethostname(),
		"smptp_server": "127.0.0.1",
		"smtp_port": 25,
		"smtp_user": "",
		"smtp_password": ""
	}
}


#####################################################


def ImportConfigString(cstr):
	try:
		with bpmailer.config.rlock:
			bpmailer.config.data =  dict(list(bpmailer.config.data.items()) + list(json.loads(cstr).items()))
			bpmailer.config.Save()
	except Exception as e:
		raise(Exception("Unable to import configuration: %s" % str(e)))


def ImportConfigFile(cfile):
	try:
		with open(cfile) as f:  
			ImportConfigString(f.read())
	except Exception as e:
		raise(Exception("Unable to import config file %s: %s\n" % (cfile,str(e))))


class Config(object):

	def __init__(self, source=False):
		self.data = {}
		self.source = source
		self.rlock = threading.RLock()

		if not self.source and os.name == 'posix':
			self.source = "/usr/local/bpmailer/etc/bpmailer.json"
		elif not self.source and os.name == 'nt':
			self.source = "%s/bpmailer/etc/bpmailer.json" % os.environ["ProgramW6432"]
		self.data = default_config
		if self.source:  self._Load()


	def __exit__(self, type, value, traceback):
		if self.source:  self.Save()


	def _Load(self):
		with self.rlock:
			try:
				with open(self.source) as fp:
					self.data =  dict(list(self.data.items()) + list(json.load(fp).items()))
			except IOError:
				# File doesn't exist - set note and save to self.source on program exit
				sys.stderr.write("No configuration file at %s, running with default configuration\n" % str(self.source))
			except:
				raise


	def Save(self,source=False):
		if source:  self.source = source

		if self.source:  
			with self.rlock:
				try:
					with open(self.source,"w") as fp:
						self.data = json.dump(self.data,fp)
				except Exception as e:
					raise(Exception("Error saving configuration file %s: %s" % (self.source,str(e))))




