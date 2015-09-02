#!/usr/bin/env python

#
# Expects the following environment variables for execution:
#	CONTROL_ALIAS
#	CONTROL_USER
#	CONTROL_PASSWD
#
# Takes zero or more port/protocol tuples on the command line.  ICMP is always enabled.
# For example:
#	./clc_api_nat_ip.py 80/TCP 443/TCP 100-500/UDP
#
# This does not add source port restrictions to the public IP.
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


# clc set creds
try:
	clc.v2.SetCredentials(os.environ['CONTROL_USER'],os.environ['CONTROL_PASSWD'])
except KeyError:
	sys.stderr.write("Must set the environment variables CONTROL_USER and CONTROL_PASSWD\n")
	sys.exit(1)


# clc get self
try:
	s = clc.v2.Server(id=socket.gethostname(),alias=os.environ['CONTROL_ALIAS'])
	p = s.PublicIPs()
except:
	sys.stderr.write("Unable to access server or public IP.  Validate credentials are correct\n")
	sys.exit(1)


# build port/proto request
try:
	ports_req = []
	for kv in sys.argv[1:]:
		(port_group,protocol) = re.split("/",kv)

		if protocol.upper() not in ('TCP','UDP'):  raise(Exception())
		if not re.match("^[\d\-]+$",port_group):  raise(Exception())

		ports = re.split("-",port_group)
		if len(ports)==1:  ports_req.append({'protocol': protocol.upper(), 'port': ports[0]})
		else:  ports_req.append({'protocol': protocol.upper(), 'port': ports[0], 'port_to': ports[1]})
except:
	sys.stderr.write("Invalid port/protocol syntax\n")
	sys.exit(1)


# clc add/update public IP
if 'public' not in s.ip_addresses[0].keys():
	p.Add(ports=ports_req,private_ip=s.ip_addresses[0]['internal']).WaitUntilComplete()
else:
	p.public_ips[0].AddPorts(ports_req).WaitUntilComplete()


# clc refresh self
try:
	if os.name=='bt': file_path = 'c:\sysadmin\public_ip'
	else: file_path = '/sysadmin/public_ip'

	with open(file_path,'w') as fh:
		fh.write("%s\n" % clc.v2.Server(id=socket.gethostname(),alias=os.environ['CONTROL_ALIAS']).ip_addresses[0]['public'])
except:
	sys.stderr.write("Unable to access newly created public IP\n")
	sys.exit(1)

