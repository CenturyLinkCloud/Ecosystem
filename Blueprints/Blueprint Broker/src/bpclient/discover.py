"""
bp_client discover module.

Package to initiate UDP broadcast to local networks searching for existing BP Broker servers.
"""


import socket
from socket import SOL_SOCKET, SO_BROADCAST
import sys

import bpclient


#####################################################

def Discover(name):
	"""Broadcast BP Broker discover traffic to local networks, returing BP Broker that resonds.

	Broadcasts UDP packet to all local networks containing a BP Broker discover query.
	If BP Broker is on one of these networks and contains the specified "name" in the service
	registry then it will respond.

	:param name: Services key to search to broadcast to bp broker servers
	:returns bpboker: Returns IP address of responding BP Broker or False if no response
	"""

	# SOCK_DGRAM is the socket type to use for UDP sockets
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.settimeout(3)
	sock.setsockopt(SOL_SOCKET, SO_BROADCAST, True)

	try:
		sock.sendto(name + "\n", ('<broadcast>', 20443))
		received, src = sock.recvfrom(1024)

		if received == "Key Exists\n":  return({'bpbroker': src[0]})
		else:  raise(Exception("No results"))

	except socket.timeout:
		raise(Exception("No results"))

