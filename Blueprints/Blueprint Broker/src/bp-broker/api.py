"""
bp_broker API module.

Listens and responds to ssl connections.  Proxies connection requests to registered event handlers.
"""


import BaseHTTPServer, SimpleHTTPServer
import ssl

import bpbroker


#####################################################


web_server = BaseHTTPServer.HTTPServer(('localhost', 20443), SimpleHTTPServer.SimpleHTTPRequestHandler)
web_server.socket = ssl.wrap_socket (web_server.socket, 
									 server_side=True,
									 certfile="bp-broker/dummy_api.crt",
									 keyfile="bp-broker/dummy_api.key")
web_server.serve_forever()

