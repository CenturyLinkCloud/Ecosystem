"""
bp_broker API Worker.

"""


import threading
import Queue
import time

import bpbroker


default_config = {
}



#####################################################



class WorkerThread(threading.Thread):

	def __init__(self,worker_queue,health_queue,config={}):
		threading.Thread.__init__(self)
		self.worker_queue = worker_queue
		self.health_queue = health_queue
		self._stop_event = threading.Event()
		self.config = dict(list(default_config.items()) + list(config.items()))
		self.backup_ts = time.time()


	def join(self,timeout=None):
		self._stop_event.set()
		threading.Thread.join(self, timeout)


	def run(self):

		while not self._stop_event.is_set():
			with bpbroker.config.rlock:
				if time.time()>self.backup_ts+bpbroker.config.data['_config']['backup_freq_secs']:
					self.Backup()

			time.sleep(5)
			#self.HealthCheck()


	def Backup(self):
		# TODO - backup file rotation
		bpbroker.config.Save()


	def HealthCheck(self):
		self.health_queue.put_nowait({'thread': 'worker', 'ts': int(time.time())})



