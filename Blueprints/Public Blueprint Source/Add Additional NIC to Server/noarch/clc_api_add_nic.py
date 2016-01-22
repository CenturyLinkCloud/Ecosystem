#!/usr/bin/env python

#
# Expects the following environment variables for execution:
#	CONTROL_ALIAS
#	CONTROL_USER
#	CONTROL_PASSWD
#	NETWORK
#

import os
import re
import sys
import clc
import socket
import requests

#try:
#	requests.packages.urllib3.disable_warnings()
#except:
#	pass


# Packaging Windows as .exe can't find cacert so SSL fails
if os.name=='nt':  os.environ['REQUESTS_CA_BUNDLE'] = "%s\cacert.pem" % getattr(sys, '_MEIPASS', os.path.abspath("."))


# clc set creds
try:
	clc.v2.SetCredentials(os.environ['CONTROL_USER'],os.environ['CONTROL_PASSWD'])
except KeyError:
	sys.stderr.write("Must set the environment variables CONTROL_ALIAS, CONTROL_USER and CONTROL_PASSWD\n")
	sys.exit(1)


# clc get self
try:
	s = clc.v2.Server(id=socket.gethostname(),alias=os.environ['CONTROL_ALIAS'])
except:
	raise
	sys.stderr.write("Unable to access server.  Validate credentials are correct\n")
	sys.exit(1)


# clc add NIC
idc = socket.gethostname()[0:2]
n = clc.v2.Networks(location=idc).Get(os.environ('NETWORK'))
print "Adding NIC to %s\%s (%s)" % (idc,os.environ('NETWORK'),n.id)
s.AddNIC(network_id=n.id,ip='').WaitUntilComplete()


# clc refresh self
try:
	if os.name=='nt': file_path = 'c:\sysadmin\public_ip'
	else: file_path = '/sysadmin/public_ip'

	with open(file_path,'w') as fh:
		fh.write("%s\n" % clc.v2.Server(id=socket.gethostname(),alias=os.environ['CONTROL_ALIAS']).ip_addresses[0]['public'])
except:
	sys.stderr.write("Unable to access newly created public IP\n")
	sys.exit(1)

