"""Command-line interface to bpclient."""

import argparse
import ConfigParser
import os
import sys
import bpclient


class Args:

	def __init__(self):
		bpclient.args = self
		self.ParseArgs()
		#self.ImportIni()
		#self.MergeEnvironment()
		#self.MergeCommands()


	def ParseArgs(self):
		parser = argparse.ArgumentParser(description="bpbroker service client")
		parser_sp1 = parser.add_subparsers(title='Commands',dest='command')

		########## Ping ###########
		parser_account = parser_sp1.add_parser('ping', help='Connectivity health check')
		parser_sp2 = parser_account.add_subparsers(dest='sub_command')

		## Get
		parser_account_get = parser_sp2.add_parser('get', help='Get details on root or specified sub-account')
		parser_account_get.add_argument('--data', help='Data payload.  This is echoed back from the server on successful test')


		########## Services ###########
		parser_user = parser_sp1.add_parser('service', help='Service broker registration and querying')
		parser_sp3 = parser_user.add_subparsers(dest='sub_command')

		## Register
		parser_user_register = parser_sp3.add_parser('register', help='Register supplied data to supplied key')
		parser_user_register.add_argument('--name', required=True, help='Unique key for service broker registration')
		parser_user_register.add_argument('--data', required=True, help='Data associated with this key')

		## Replace
		parser_user_replace = parser_sp3.add_parser('replace', help='Replace data associated with supplied key')
		parser_user_replace.add_argument('--name', required=True, help='Unique key')
		parser_user_replace.add_argument('--data', required=True, help='Data associated with this key')

		## Update
		parser_user_update = parser_sp3.add_parser('update', help='Update data associated with supplied key')
		parser_user_update.add_argument('--name', required=True, help='Unique key')
		parser_user_update.add_argument('--data', required=True, help='Data associated with this key')

		## Get
		parser_user_get = parser_sp3.add_parser('get', help='Return data associated with supplied key')
		parser_user_get.add_argument('--name', required=True, help='Unique key')

		## Delete
		parser_user_delete = parser_sp3.add_parser('delete', help='Delete key from service broker')
		parser_user_delete.add_argument('--name', required=True, help='Unique key')


		########## Global ###########
		#parser.add_argument('--cols', nargs='*', metavar='COL', help='Include only specific columns in the output')
		#parser.add_argument('--config', '-c', help='Ini config file')
		#parser.add_argument('--quiet', '-q', action='count', help='Supress status output (repeat up to 2 times)')
		#parser.add_argument('--verbose', '-v', action='count', help='Increase verbosity')
		#parser.add_argument('--format', '-f', choices=['json','table','text','csv'], default='table', help='Output result format (table is default)')
		self.args = parser.parse_args()


	def GetCommand(self):  return(self.args.command)
	def GetArgs(self):  return(self.args)


	def ImportIni(self):
		pass


	def MergeEnvironment(self):
		pass


	def MergeCommands(self):
		pass




class ExecCommand():
	def __init__(self):
		try:
			self.Bootstrap()
		except Exception as e:
			sys.exit(1)


	def Bootstrap(self):
		if bpclient.args.GetCommand() == 'ping':  self.Ping()
		elif bpclient.args.GetCommand() == 'services':  self.Services()


	def Ping(self):
		if bpclient.args.GetArgs().sub_command == 'ping':  self.PingPing()


	def Services(self):
		if bpclient.args.GetArgs().sub_command == 'register':  self.ServicesRegister()
		elif bpclient.args.GetArgs().sub_command == 'get':  self.ServicesGet()
		elif bpclient.args.GetArgs().sub_command == 'replace':  self.ServicesReplace()
		elif bpclient.args.GetArgs().sub_command == 'update':  self.ServicesUpdate()
		elif bpclient.args.GetArgs().sub_command == 'delete':  self.ServicesDelete()


#	def Exec(self,function,args=False,cols=None,supress_output=False):
#		try:
#			if args:  r = eval("%s(**%s)" % (function,args))
#			else:  r = eval("%s()" % (function))
#
#			#  Filter results
#			if bpclient.args.args.cols:  cols = bpclient.args.args.cols
#
#			# Output results
#			# TODO - how do we differentiate blueprints vs. queue RequestIDs?
#			if r is not None and 'RequestID' in r and not bpclient.args.args.async:  
#				r = bpclient.output.RequestBlueprintProgress(r['RequestID'],self._GetLocation(),self._GetAlias(),bpclient.args.args.quiet)
#				cols = ['Server']
#
#			if not isinstance(r, list):  r = [r]
#			if not supress_output and bpclient.args.args.format == 'json':  print bpclient.output.Json(r,cols)
#			elif not supress_output and bpclient.args.args.format == 'table':  print bpclient.output.Table(r,cols)
#			elif not supress_output and bpclient.args.args.format == 'text':  print bpclient.output.Text(r,cols)
#			elif not supress_output and bpclient.args.args.format == 'csv':  print bpclient.output.Csv(r,cols)
#
#			return(r)
#		except bpclient.AccountDeletedException:
#			bpclient.output.Status('ERROR',2,'Unable to process, account in deleted state')
#		except bpclient.AccountLoginException:
#			bpclient.output.Status('ERROR',2,'Transient login error.  Please retry')


