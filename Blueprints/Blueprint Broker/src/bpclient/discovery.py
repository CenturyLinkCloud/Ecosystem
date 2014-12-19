"""
bp_client discovery module.

Package to initiate UDP broadcast to local networks searching for existing BP Broker servers.
"""


import requests

import bpclient


#####################################################

def Discovery(name):
	"""Execute custom RPC on BP Broker server passing along data payload.

	Expects RPC method to be fully qualified incusive of file/package to execute and the actual method.
	For example if you were to execute the following on the BP Broker server:

		import testpacakage
		testpackage.testmodule.method(params)

	The equivalent call to this method is:

		bpclient.Execute(method="testpackage.testmodule.method",data="params")

	The actual call to the BP Broker is:

		POST https://broker/testpackage.testmodule/method?data=params

	If using the bpclient cli this is accomplished with the following command:

		bpclient --method testpackage.testmodule.method --data params
		
	:param name: Services key to search to broadcast to bp broker servers
	:returns bpboker: Returns IP address of responding BP Broker or False if no response
	"""

	method_match = re.match("(.*)\.(.*)",method)

	r = requests.post("https://%s/%s/%s/" % (bpclient.BPBROKER,method_match.group(1),method_match.group(2)),params={'data': data},verify=False)
	return(r.text)


