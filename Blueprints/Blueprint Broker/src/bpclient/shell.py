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
		self.MergeEnvironment()
		self.MergeCommands()


	def ParseArgs(self):
		parser = argparse.ArgumentParser(description="bpclient service client")
		parser_sp1 = parser.add_subparsers(title='Commands',dest='command')

		########## Ping ###########
		parser_ping = parser_sp1.add_parser('ping', help='Connectivity health check')
		parser_ping.add_argument('--data', help='Data payload.  This is echoed back from the server on successful test')
		parser_ping.add_argument('--raw', action="store_true", default=False, help='Return raw data')


		########## Services ###########
		parser_services = parser_sp1.add_parser('service', help='Service broker registration and querying')
		parser_sp3 = parser_services.add_subparsers(dest='sub_command')

		## Register
		parser_services_register = parser_sp3.add_parser('register', help='Register supplied data to supplied key')
		parser_services_register.add_argument('--name', required=True, help='Unique key for service broker registration')
		parser_services_register.add_argument('--data', required=True, help='Data associated with this key')
		parser_services_register.add_argument('--raw', action="store_true", default=False, help='Return raw data')

		## Replace
		parser_services_replace = parser_sp3.add_parser('replace', help='Replace data associated with supplied key')
		parser_services_replace.add_argument('--name', required=True, help='Unique key')
		parser_services_replace.add_argument('--data', required=True, help='Data associated with this key')
		parser_services_replace.add_argument('--raw', action="store_true", default=False, help='Return raw data')

		## Update
		parser_services_update = parser_sp3.add_parser('update', help='Update data associated with supplied key')
		parser_services_update.add_argument('--name', required=True, help='Unique key')
		parser_services_update.add_argument('--data', required=True, help='Data associated with this key')
		parser_services_update.add_argument('--raw', action="store_true", default=False, help='Return raw data')

		## Get
		parser_services_get = parser_sp3.add_parser('get', help='Return data associated with supplied key')
		parser_services_get.add_argument('--name', required=True, help='Unique key')
		parser_services_get.add_argument('--raw', action="store_true", default=False, help='Return raw data')

		## Delete
		parser_services_delete = parser_sp3.add_parser('delete', help='Delete key from service broker')
		parser_services_delete.add_argument('--name', required=True, help='Unique key')
		parser_services_delete.add_argument('--raw', action="store_true", default=False, help='Return raw data')


		########## Execute ###########
		parser_execute = parser_sp1.add_parser('execute', help='Execute custom RPC on BP Broker server')
		parser_execute.add_argument('--method', required=True, help='Fully qualified package and method to execute')
		parser_execute.add_argument('--data', required=True, help='Data payload')


		########## Discovery ###########
		parser_discovery = parser_sp1.add_parser('discover', help='Discover BP server on local subnet')
		parser_discovery.add_argument('--name', required=True, help='BP server containig specified key in service registry will respond')


		########## Email ###########


		########## Poll Account ###########


		########## Global ###########
		parser.add_argument('--bpbroker', '-b', metavar='host:port', help='BP Broker to communicate with')
		parser.add_argument('--access-key', '-a', default='', metavar='KEY', help='Optional access key required to access some BP Broker modules')
		parser.add_argument('--cols', nargs='*', metavar='COL', help='Include only specific columns in the output')
		parser.add_argument('--format', '-f', choices=['json','text','csv','csv-noheader'], default='text', help='Output result format (text is default)')
		self.args = parser.parse_args()


	def GetCommand(self):  return(self.args.command)
	def GetArgs(self):  return(self.args)


	def ImportIni(self):
		pass


	def MergeEnvironment(self):
		if 'BPBROKER' in os.environ:  bpclient.BPROKER = os.environ['BPROKER']


	def MergeCommands(self):
		if self.args.bpbroker:  bpclient.BPBROKER = self.args.bpbroker




class ExecCommand():
	def __init__(self):
		try:
			self.Bootstrap()
		except Exception as e:
			sys.exit(1)


	def Bootstrap(self):
		if bpclient.args.GetCommand() == 'ping':  self.Ping()
		elif bpclient.args.GetCommand() == 'discover':  self.Discover()
		elif bpclient.args.GetCommand() == 'execute':  self.Execute()
		elif bpclient.args.GetCommand() == 'service':  self.Services()


	def Services(self):
		if bpclient.args.GetArgs().sub_command == 'register':  self.ServicesRegister()
		elif bpclient.args.GetArgs().sub_command == 'get':  self.ServicesGet()
		elif bpclient.args.GetArgs().sub_command == 'replace':  self.ServicesReplace()
		elif bpclient.args.GetArgs().sub_command == 'update':  self.ServicesUpdate()
		elif bpclient.args.GetArgs().sub_command == 'delete':  self.ServicesDelete()


	def _ServicesWrapper(self,function,args,cols,opts={}):
		try:
			opts['supress_output'] = True
			r = self.Exec(function,args,cols,opts,supress_output=True)

			if 'success' in r and not r['success']:  raise(Exception(r['message']+"\n"))
			if 'data' in r and '_str' in r['data']:  r['data'] = r['data']['_str']
			if not bpclient.args.args.raw and 'data' in r: 
				r = {'data': r['data']}
				cols = ('data',)

			if 'data' in r:
				if bpclient.args.args.format == 'json':  print bpclient.output.Json(r,cols,opts)
				elif bpclient.args.args.format == 'text':  print bpclient.output.Text(r,cols,opts)
				elif bpclient.args.args.format == 'csv-noheader':  print bpclient.output.Csv(r,cols,{'no_header': True})
				elif bpclient.args.args.format == 'csv':  print bpclient.output.Csv(r,cols,opts)

		except Exception as e:
			sys.stderr.write("Fatal error: %s" % str(e))
			sys.exit(1)


	def Ping(self):
		self._ServicesWrapper('bpclient.ping.Ping',{'data': bpclient.args.args.data, 'access_key': bpclient.args.args.access_key},['src','pong'])


	def Execute(self):
		try:
			print self.Exec('bpclient.execute.Execute',
			                {'method': bpclient.args.args.method, 'data': bpclient.args.args.data, 'access_key': bpclient.args.args.access_key}, 
							[], supress_output=True)
		except Exception as e:
			sys.stderr.write("Fatal error: %s\n" % str(e))
			sys.exit(1)


	def Discover(self):
		try:
			self.Exec('bpclient.discover.Discover',{'name': bpclient.args.args.name}, ['bpbroker'])
		except Exception as e:
			sys.stderr.write("Fatal error: %s\n" % str(e))
			sys.exit(1)


	def ServicesRegister(self):
		self._ServicesWrapper('bpclient.services.Register',
		                      {'name': bpclient.args.args.name, 'data': bpclient.args.args.data, 'access_key': bpclient.args.args.access_key},
		                      ['success','message','data'])


	def ServicesGet(self):
		self._ServicesWrapper('bpclient.services.Get',
		                      {'name': bpclient.args.args.name, 'access_key': bpclient.args.args.access_key}, 
							  ['success','message','data'])


	def ServicesDelete(self):
		self._ServicesWrapper('bpclient.services.Delete',
		                      {'name': bpclient.args.args.name, 'access_key': bpclient.args.args.access_key}, 
							  ['success','message'])


	def ServicesReplace(self):
		self._ServicesWrapper('bpclient.services.Replace',
		                      {'name': bpclient.args.args.name, 'access_key': bpclient.args.args.access_key, 'data': bpclient.args.args.data},
		                      ['success','message','data'])


	def ServicesUpdate(self):
		self._ServicesWrapper('bpclient.services.Update',
		                      {'name': bpclient.args.args.name, 'data': bpclient.args.args.data, 'access_key': bpclient.args.args.access_key},
		                      ['success','message','data'])


	def Exec(self,function,args=False,cols=None,opts={},supress_output=False):
		try:
			if args:  r = eval("%s(**%s)" % (function,args))
			else:  r = eval("%s()" % (function))

			if bpclient.args.args.cols:  cols = bpclient.args.args.cols

			# TODO - not sure whether we'll reuse this code at all or duplicate in wrappers as needed?
			if not supress_output and bpclient.args.args.format == 'json':  print bpclient.output.Json(r,cols,opts)
			elif not supress_output and bpclient.args.args.format == 'text':  print bpclient.output.Text(r,cols,opts)
			elif not supress_output and bpclient.args.args.format == 'csv-noheader':  print bpclient.output.Csv(r,cols,{'no_header': True})
			elif not supress_output and bpclient.args.args.format == 'csv':  print bpclient.output.Csv(r,cols,opts)

			return(r)

		except:
			raise


