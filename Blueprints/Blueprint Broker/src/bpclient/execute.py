"""
bp_client execute module.

Package to initiate custom RPC call on BP Broker server
"""


import re
import requests

import bpclient


#####################################################

def Execute(method,data,access_key=''):
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
		
	:param method: RPC method to execute
	:param data: Data to be sent/echoed
	:returns : Sends returns all output to stdout
	"""

	method_match = re.match("(.*)\.(.*)",method)

	r = requests.post("https://%s/%s/%s/" % (bpclient.BPBROKER,method_match.group(1),method_match.group(2)),
	                  params={'access_key':access_key,'data': data},verify=False)
	if r.status_code != 200:  raise(Exception("Response Error %s" % r.status_code))

	return(r.text)


