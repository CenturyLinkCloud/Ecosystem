#!/usr/bin/env python

import Queue
import signal
import time
import sys
import os

import bpbroker



####################################################

def Shutdown(signum, fram):
	print "\n"
	sys.exit(0)

####################################################

def _StartPosix():

	queue_worker = Queue.Queue()
	queue_health = Queue.Queue()

	api_thread = bpbroker.API.APIThread(queue_worker,queue_health)
	api_thread.start()

	discover_thread = bpbroker.discover.DiscoverThread(queue_worker,queue_health)
	discover_thread.start()


	signal.signal(signal.SIGINT,Shutdown)
	while True:  time.sleep(5)


def _StartNt():
	win32serviceutil.HandleCommandLine(AppServerSvc)


def Start():
	#if os.name == 'posix':  _StartPosix()
	#if os.name == 'nt':  _StartNt()
	_StartPosix()


if os.name == 'nt':
	
	#import pythoncom
	import win32serviceutil
	import win32service
	import win32event
	import servicemanager
	import socket
	
	
	class AppServerSvc (win32serviceutil.ServiceFramework):
	    _svc_name_ = "BPBroker"
	    _svc_display_name_ = "BP Broker Service"
	
	    def __init__(self,args):
	        win32serviceutil.ServiceFramework.__init__(self,args)
	        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
	        socket.setdefaulttimeout(60)
	
	    def SvcStop(self):
	        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
	        win32event.SetEvent(self.hWaitStop)
	
	    def SvcDoRun(self):
	        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
	                              servicemanager.PYS_SERVICE_STARTED,
	                              (self._svc_name_,''))
	        self.main()
	
	    def main(self):
			bpbroker.server.Start()
	

