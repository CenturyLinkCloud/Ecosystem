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

def Start():

	queue_worker = Queue.Queue()
	queue_health = Queue.Queue()

	api_thread = bpbroker.API.APIThread(queue_worker,queue_health)
	api_thread.start()

	discover_thread = bpbroker.discover.DiscoverThread(queue_worker,queue_health)
	discover_thread.start()


	signal.signal(signal.SIGINT,Shutdown)
	while True:  time.sleep(5)
	

