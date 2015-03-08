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
import os
from urlparse import urlparse, parse_qs, parse_qsl
from StringIO import StringIO

import bpbroker



default_config = {
	'listen_port': 20443,
	'listen_ip': '',	# default bind to all interfaces
	'ssl_cert': '%s/dummy_api.crt' % os.path.dirname(bpbroker.__file__),
	'ssl_key': '%s/dummy_api.key' % os.path.dirname(bpbroker.__file__),
}



#####################################################

class TimeoutBaseHTTPServer(BaseHTTPServer.HTTPServer):
	timeout = 1



class APIHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	# Response variables populated by individual request handlers
	status = 200
	status_message = ''
	content_type = "Application/json"
	data = ''


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
			if self.package not in bpbroker.config.data:  error = "Unauthorized package"
			elif '_access_key' in bpbroker.config.data[self.package] and bpbroker.config.data[self.package]['_access_key'] and \
			   ('access_key' not in self.qs or self.qs['access_key'] != bpbroker.config.data[self.package]['_access_key']):
			   	error = "Incorrect access key"
			elif re.match("_",self.method):  error = "Unauthorized method"
			else:
				try:
					self.package_obj = __import__("bpbroker."+self.package)
					for mod in self.package.split("."):  self.package_obj = getattr(self.package_obj,mod)
					if not hasattr(self.package_obj, self.method):  error = "Unauthorized method"
				except:
					try:
						self.package_obj = __import__(self.package)
						if re.search("\.",self.package):
							for mod in re.sub(".*?\.","",self.package).split("."):  self.package_obj = getattr(self.package_obj,mod)
						if not hasattr(self.package_obj, self.method):  error = "Unauthorized method"
					except:
						error = "Unauthorized method"

		if error: self.send_error(401, error)

		return(not error)


	def do_GET(self):  self.ProcessRequest()
	def do_POST(self):  self.ProcessRequest()
	def do_DELETE(self):  self.ProcessRequest()


	def ProcessRequest(self):
		self._ParseRequest()
		if self._ValidateRequest():  
			getattr(self.package_obj, self.method)(self)
			if self.status==200:  
				self.send_response(self.status)
				self.send_header('Content-Type',self.content_type)
				self.end_headers()
				self.wfile.write(self.data)
			else:  self.send_error(self.status,self.status_message)



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
			#self.HealthCheck()


	def HealthCheck(self):
		self.health_queue.put_nowait({'thread': 'API', 'ts': int(time.time())})



