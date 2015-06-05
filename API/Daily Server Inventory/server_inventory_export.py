#!/usr/bin/env python

#
# **Server Inventory Export**
# Export list of all servers deployed within the named CenturyLink Cloud datacenters.
# Designed to be run once daily from a job scheduler and writes basic server inventory
# data to a date-stamped file.  In event of errors the script exists and no file is
# created for that day.
#

import datetime
import requests
import json
import sys
import re

DATACENTERS = ('VA1', )		# Add all in-scope locations to this list
OUTPUT_FILE = "./server_inventory_export"
ALIAS = "XXXX"
APIV1_KEY = "XXXXX"
APIV1_PASSWD = "XXXX"



headers = {'content-type': 'application/json'}

## Login ##
try:
	r_login = requests.post("https://api.tier3.com/REST/Auth/Logon", data={'APIKey': APIV1_KEY, 'Password': APIV1_PASSWD} )
	if not re.search('Success="true"',r_login.text):
		print "Login Error"
		raise
except:
	sys.exit(1)


## Iterate through all subaccounts ##
try:
	r = requests.post("https://api.tier3.com/REST/Account/GetAccounts/JSON", cookies=r_login.cookies, headers=headers)
	aliases = [ALIAS]
	for account in r.json()['Accounts']:  aliases.append(account['AccountAlias'])
except:
	print "Error retrieving account list"
	sys.exit(1)

output = []
output.append("	".join(('Name','Description','Status','IP Address','CPU','RAM','Disk','Environment',)))
try:
	for alias in aliases:
		## Iterate through locations ##
		for location in DATACENTERS:
			r = requests.post("https://api.tier3.com/REST/Server/GetServers/JSON", cookies=r_login.cookies, headers=headers, 
								data=json.dumps({'AccountAlias': alias, 'Location': location}))
	
			for server in r.json()['Servers']:
				#print server
				output.append("	".join((server['Name'],server['Description'],server['Status'],server['IPAddress'],str(server['Cpu']), 
				                           str(server['MemoryGB']),str(server['TotalDiskSpaceGB']),server['CustomFields'][0]['Value'])))
except:
	print "Error retrieving servers list"
	sys.exit(1)


## Write results ##
try:
	f = open('%s.%s.tsv' % (OUTPUT_FILE,datetime.date.today().isoformat()),'w')
	f.write("\n".join(output))
	f.write("\n")
	f.close()
except:
	print "Error writing inventory list"
	sys.exit(1)


