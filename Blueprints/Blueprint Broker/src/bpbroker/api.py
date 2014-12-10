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
from urlparse import urlparse, parse_qs

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
	def log_request(self, code='-', size='-'):
		pass


	def ParseRequest(self):
		(undef,self.package,self.method) = urlparse(self.path).path.split("/",3)
		self.qs = parse_qs(urlparse(self.path).query)


	def ValidateRequest(self):
		error = False
		with bpbroker.config.rlock:
			if self.package not in bpbroker.config.data:  error = True
			if re.match("_",self.method):  error = True
			else:
				try:
					if not hasattr(__import__(self.package),self.method):  return(False)
				except:
					error = True

		if error: self.send_error(401, "Unauthorized")

		return(error)


	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		self.ParseRequest()
		if self.ValidateRequest():
		print self.path


class APIThread(threading.Thread):

	def __init__(self,worker_queue,health_queue,config={}):
		threading.Thread.__init__(self)
		self.worker_queue = worker_queue
		self.health_queue = health_queue
		self._stop_event = threading.Event()
		bpbroker.config.data['hits'] = []
		self.config = dict(list(default_config.items()) + list(config.items()))


	def join(self,timeout=None):
		self._stop_event.set()
		threading.Thread.join(self, timeout)


	def run(self):
		#self.web_server = TimeoutBaseHTTPServer((self.config['listen_ip'], self.config['listen_port']), SimpleHTTPServer.SimpleHTTPRequestHandler)
		self.web_server = TimeoutBaseHTTPServer((self.config['listen_ip'], self.config['listen_port']), APIHTTPRequestHandler)
		self.web_server.socket = ssl.wrap_socket (self.web_server.socket, 
									 			  server_side=True,
									 			  certfile=self.config['ssl_cert'],
									 			  keyfile=self.config['ssl_key'],
												  )
		while not self._stop_event.is_set():
			self.web_server.handle_request()
			self.HealthCheck()


	def HealthCheck(self):
		self.health_queue.put_nowait({'thread': 'API', 'ts': int(time.time())})



