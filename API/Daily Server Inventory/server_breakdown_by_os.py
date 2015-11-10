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

DATACENTERS = ('CA1','CA2','CA3','DE1','GB1','GB3','IL1','NY1','SG1','UC1','UT1','VA1','WA1' )		# Add all in-scope locations to this list
OUTPUT_FILE = "./server_inventory_export"
ALIAS = "XXXX"
APIV1_KEY = "XXXXX"
APIV1_PASSWD = "XXXX"



headers = {'content-type': 'application/json'}

## Login ##
try:
	r_login = requests.post("https://api.ctl.io/REST/Auth/Logon", data={'APIKey': APIV1_KEY, 'Password': APIV1_PASSWD} )
	if not re.search('Success="true"',r_login.text):
		print "Login Error"
		raise
except:
	sys.exit(1)

# Get OS list
os_itos = {}
r = requests.post("https://api.ctl.io/REST/Server/GetServerTemplates/JSON", cookies=r_login.cookies, headers=headers, 
					data=json.dumps({'AccountAlias': 'T3N', 'Location': 'WA1'}))
	
for tpl in r.json()['Templates']:  os_itos[tpl['OperatingSystem']] = tpl['Description']

## Iterate through all subaccounts ##
try:
	r = requests.post("https://api.ctl.io/REST/Account/GetAccounts/JSON", cookies=r_login.cookies, headers=headers)
	aliases = [ALIAS]
	for account in r.json()['Accounts']:  aliases.append(account['AccountAlias'])
except:
	print "Error retrieving account list"
	sys.exit(1)

output = []
output.append("	".join(('Name','Description','Status','IP Address','CPU','RAM','Disk','Environment',)))
operating_systems = {}
fh = open("servers.csv","w")
try:
	print "Processing %s accounts" % (len(aliases))
	for alias in aliases:
		## Iterate through locations ##
		for location in DATACENTERS:
			try:
				r = requests.post("https://api.ctl.io/REST/Server/GetServers/JSON", cookies=r_login.cookies, headers=headers, 
									data=json.dumps({'AccountAlias': alias, 'Location': location}))
	
				for server in r.json()['Servers']:
					try:
						if server['OperatingSystem'] in operating_systems:  operating_systems[server['OperatingSystem']] += 1
						else:  operating_systems[server['OperatingSystem']] = 1
						print "%s	%s	%s	- count %s" % (alias,location,server['Name'],sum(operating_systems.values()))
						fh.write("%s,%s\n" % (server['Name'],os_itos[server['OperatingSystem']]))
					except:
						print "*Error server*"
						pass
			except TypeError:
				print "*Error location*"
				pass
			except:
				pass
except:
	print "Error retrieving servers list"
	raise
	sys.exit(1)

fh.close()

print "***************************************"
for osid in os_itos.keys():
	print "%s - %s" % (os_itos[osid],operating_systems[osid])

