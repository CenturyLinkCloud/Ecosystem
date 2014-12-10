#!/usr/bin/env python

import Queue
import signal
import time
import sys

import bpbroker



####################################################

def Shutdown(signum, fram):
	print "\n"
	sys.exit(0)

####################################################


#bpbroker.c['test'] = 5
#bpbroker.c.testy = 5
#print bpbroker.c['test']
#print bpbroker.c
with bpbroker.config.rlock:
	print bpbroker.config.data
with bpbroker.config.rlock:
	bpbroker.config.data['x'] = 5
with bpbroker.config.rlock:
	print bpbroker.config.data
sys.exit()


queue_worker = Queue.Queue()
queue_health = Queue.Queue()

api_thread = bpbroker.API.APIThread(queue_worker,queue_health)
api_thread.start()


signal.signal(signal.SIGINT,Shutdown)
while True:  time.sleep(5)
	

