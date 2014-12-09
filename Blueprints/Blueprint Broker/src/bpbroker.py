#!/usr/bin/env python

import Queue
import bpbroker



####################################################


####################################################

queue_worker = Queue.Queue()
queue_health = Queue.Queue()

api_thread = bpbroker.API.APIThread(queue_worker,queue_health)
api_thread.start()


