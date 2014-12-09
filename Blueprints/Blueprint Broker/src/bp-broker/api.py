"""
bp_broker API module.

Listens and responds to ssl connections.  Proxies connection requests to registered event handlers.
"""


import BaseHTTPServer, SimpleHTTPServer
import ssl



#####################################################


