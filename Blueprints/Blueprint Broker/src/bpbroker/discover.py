"""
bp_broker API module.

Listens and responds to ssl connections.  Proxies connection requests to registered event handlers.
"""


import threading
import Queue
#import json
import SocketServer
import time
#import re
#from urlparse import urlparse, parse_qs, parse_qsl
#from StringIO import StringIO

import bpbroker


default_config = {
	'listen_port': 20443,
	'listen_ip': '',	# default bind to all interfaces
}



#####################################################


class TimeoutBaseUDPServer(SocketServer.UDPServer):
    timeout = 1



class DiscoverUDPHandler(SocketServer.BaseRequestHandler):

	def handle(self):
		data = self.request[0].strip()
		with bpbroker.config.rlock:
			socket = self.request[1]
			if data in bpbroker.config.data['services']:
				socket.sendto("Key Exists\n", self.client_address)



class DiscoverThread(threading.Thread):

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
		self.discover_server = TimeoutBaseUDPServer((self.config['listen_ip'], self.config['listen_port']), DiscoverUDPHandler)

		while not self._stop_event.is_set():
			self.discover_server.handle_request()
			#self.HealthCheck()


	def HealthCheck(self):
		self.health_queue.put_nowait({'thread': 'discover', 'ts': int(time.time())})



