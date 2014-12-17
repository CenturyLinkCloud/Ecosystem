"""
bp_broker API module.

Listens and responds to ssl connections.  Proxies connection requests to registered event handlers.
"""


import threading
import Queue
import json
import BaseHTTPServer, SimpleHTTPServer
import ssl
import time
import re
from urlparse import urlparse, parse_qs, parse_qsl
from StringIO import StringIO

import bpbroker


default_config = {
	'listen_port': 20443,
	'listen_ip': '',	# default bind to all interfaces
	'ssl_cert': 'bpbroker/dummy_api.crt',
	'ssl_key': 'bpbroker/dummy_api.key',
}



#####################################################


class TimeoutBaseHTTPServer(BaseHTTPServer.HTTPServer):
	timeout = 1



class APIHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	def log_error(self, format, *args):
		pass
	def log_request(self, code='-', size='-'):
		pass


	def RequestingHost(self):  return(self.client_address[:2][0])


	def _ParseRequest(self):
		self.path = re.sub("/\?","?",self.path)
		(undef,self.package,method) = urlparse(self.path).path.split("/",2)
		self.method = re.sub("/$","",method)
		self.qs = dict(parse_qsl(urlparse(self.path).query))	# Read Get qs
		if not self.qs:	
			length = int(self.headers['Content-Length'])
			self.qs = dict(parse_qsl(self.rfile.read(length),keep_blank_values=True))


	def _ValidateRequest(self):
		error = False
		with bpbroker.config.rlock:
			#if self.package not in bpbroker.config.data:  error = "Unauthorized package"
			if re.match("_",self.method):  error = "Unauthorized method"
			else:
				try:
					if not hasattr(getattr(bpbroker,self.package), self.method):  error = "Unauthorized method"
				except:
					try:
						i = __import__(self.package)
						print self.method
						if not hasattr(i, self.method):  print "this"
						if not hasattr(i, self.method):  error = "Unauthorized method"
						print "e"
					except:
						error = "Unauthorized method"

		if error: self.send_error(401, error)

		return(not error)


	def do_GET(self):  self.ProcessRequest()
	def do_POST(self):  self.ProcessRequest()
	def do_DELETE(self):  self.ProcessRequest()


	def ProcessRequest(self):
		self._ParseRequest()
		if self._ValidateRequest():  getattr(getattr(bpbroker,self.package), self.method)(self)



class APIThread(threading.Thread):

	def __init__(self,worker_queue,health_queue,config={}):
		threading.Thread.__init__(self)
		self.worker_queue = worker_queue
		self.health_queue = health_queue
		self._stop_event = threading.Event()
		self.config = dict(list(default_config.items()) + list(config.items()))


	def join(self,timeout=None):
		self._stop_event.set()
		threading.Thread.join(self, timeout)


	def run(self):
		self.api_server = TimeoutBaseHTTPServer((self.config['listen_ip'], self.config['listen_port']), APIHTTPRequestHandler)
		self.api_server.socket = ssl.wrap_socket (self.api_server.socket, 
									 			  server_side=True,
									 			  certfile=self.config['ssl_cert'],
									 			  keyfile=self.config['ssl_key'],
												  )
		while not self._stop_event.is_set():
			self.api_server.handle_request()
			self.HealthCheck()


	def HealthCheck(self):
		self.health_queue.put_nowait({'thread': 'API', 'ts': int(time.time())})


