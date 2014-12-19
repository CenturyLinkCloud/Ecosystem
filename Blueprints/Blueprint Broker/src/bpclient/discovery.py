"""
bp_client discovery module.

Package to initiate UDP broadcast to local networks searching for existing BP Broker servers.
"""


import sys, time
from socket import *

import bpclient


#####################################################

def Discovery(name):
	"""Broadcast BP Broker discovery traffic to local networks, returing BP Broker that resonds.

	Broadcasts UDP packet to all local networks containing a BP Broker discovery query.
	If BP Broker is on one of these networks and contains the specified "name" in the service
	registry then it will respond.

	:param name: Services key to search to broadcast to bp broker servers
	:returns bpboker: Returns IP address of responding BP Broker or False if no response
	"""


	s = socket(AF_INET, SOCK_DGRAM)
	s.bind(('', 0))
	s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	data = repr(time.time()) + '\n'
	s.sendto(data, ('<broadcast>', MYPORT))
	time.sleep(2)

