"""Command-line interface to bpbroker."""

import argparse
import ConfigParser
import os
import sys
import bpbroker


class Args:

	def __init__(self):
		bpbroker.args = self
		self.ParseArgs()
		#self.ImportIni()
		self.MergeEnvironment()
		self.MergeCommands()


	def ParseArgs(self):
		parser = argparse.ArgumentParser(description="bpbroker service")
		parser_sp1 = parser.add_subparsers(title='Commands',dest='command')

		########## Install ###########
		parser_install = parser_sp1.add_parser('install', help='Install service')


		########## Configure ###########
		parser_configure = parser_sp1.add_parser('configure', help='Apply additional configuration to bpbroker service')
		parser_configure.add_argument('--config-file', help='File containing configuration json to apply.  Default is stdin')

		## Register
		parser_user_register = parser_sp3.add_parser('register', help='Register supplied data to supplied key')
		parser_user_register.add_argument('--name', required=True, help='Unique key for service broker registration')
		parser_user_register.add_argument('--data', required=True, help='Data associated with this key')
		parser_user_register.add_argument('--raw', action="store_true", default=False, help='Return raw data')

		## Replace
		parser_user_replace = parser_sp3.add_parser('replace', help='Replace data associated with supplied key')
		parser_user_replace.add_argument('--name', required=True, help='Unique key')
		parser_user_replace.add_argument('--data', required=True, help='Data associated with this key')
		parser_user_replace.add_argument('--raw', action="store_true", default=False, help='Return raw data')

		## Update
		parser_user_update = parser_sp3.add_parser('update', help='Update data associated with supplied key')
		parser_user_update.add_argument('--name', required=True, help='Unique key')
		parser_user_update.add_argument('--data', required=True, help='Data associated with this key')
		parser_user_update.add_argument('--raw', action="store_true", default=False, help='Return raw data')

		## Get
		parser_user_get = parser_sp3.add_parser('get', help='Return data associated with supplied key')
		parser_user_get.add_argument('--name', required=True, help='Unique key')
		parser_user_get.add_argument('--raw', action="store_true", default=False, help='Return raw data')

		## Delete
		parser_user_delete = parser_sp3.add_parser('delete', help='Delete key from service broker')
		parser_user_delete.add_argument('--name', required=True, help='Unique key')
		parser_user_delete.add_argument('--raw', action="store_true", default=False, help='Return raw data')


		########## Execute ###########
		parser_execute = parser_sp1.add_parser('execute', help='Execute custom RPC on BP Broker server')
		parser_execute.add_argument('--method', required=True, help='Fully qualified package and method to execute')
		parser_execute.add_argument('--data', required=True, help='Data payload')


		########## TODO Email ###########


		########## TODO Poll Account ###########


		########## Global ###########
		parser.add_argument('--config', '-c', help='Path to non-default configuration file')
		self.args = parser.parse_args()


	def GetCommand(self):  return(self.args.command)
	def GetArgs(self):  return(self.args)


	def ImportIni(self):
		pass


	def MergeEnvironment(self):
		#if 'BPBROKER' in os.environ:  bpbroker.BPROKER = os.environ['BPROKER']
		pass


	def MergeCommands(self):
		#if self.args.bpbroker:  bpbroker.BPBROKER = self.args.bpbroker
		pass




class ExecCommand():
	def __init__(self):
		try:
			self.Bootstrap()
		except Exception as e:
			sys.exit(1)


	def Bootstrap(self):
		if bpbroker.args.GetCommand() == 'ping':  self.Ping()
		elif bpbroker.args.GetCommand() == 'discovery':  self.Discovery()


	def Services(self):
		if bpbroker.args.GetArgs().sub_command == 'register':  self.ServicesRegister()
		elif bpbroker.args.GetArgs().sub_command == 'get':  self.ServicesGet()
		elif bpbroker.args.GetArgs().sub_command == 'replace':  self.ServicesReplace()
		elif bpbroker.args.GetArgs().sub_command == 'update':  self.ServicesUpdate()
		elif bpbroker.args.GetArgs().sub_command == 'delete':  self.ServicesDelete()


	def _ServicesWrapper(self,function,args,cols,opts={}):
		try:
			opts['supress_output'] = True
			r = self.Exec(function,args,cols,opts,supress_output=True)

			if 'data' in r and '_str' in r['data']:  r['data'] = r['data']['_str']
			if not bpbroker.args.args.raw and 'data' in r: 
				r = {'data': r['data']}
				cols = ('data',)

			if 'data' in r:
				if bpbroker.args.args.format == 'json':  print bpbroker.output.Json(r,cols,opts)
				elif bpbroker.args.args.format == 'text':  print bpbroker.output.Text(r,cols,opts)
				elif bpbroker.args.args.format == 'csv-noheader':  print bpbroker.output.Csv(r,cols,{'no_header': True})
				elif bpbroker.args.args.format == 'csv':  print bpbroker.output.Csv(r,cols,opts)

		except Exception as e:
			sys.stderr.write("Fatal error: %s" % str(e))
			sys.exit(1)


	def Ping(self):
		self._ServicesWrapper('bpbroker.ping.Ping',{'data': bpbroker.args.args.data},['src','pong'])


	def Execute(self):
		try:
			print self.Exec('bpbroker.execute.Execute',{'method': bpbroker.args.args.method, 'data': bpbroker.args.args.data}, [], supress_output=True)
		except Exception as e:
			sys.stderr.write("Fatal error: %s" % str(e))
			sys.exit(1)


	def Discovery(self):
		try:
			print self.Exec('bpbroker.discovery.discovery',{'name': bpbroker.args.args.name, ['bpbroker'])
		except Exception as e:
			sys.stderr.write("Fatal error: %s" % str(e))
			sys.exit(1)


	def ServicesRegister(self):
		self._ServicesWrapper('bpbroker.services.Register',{'name': bpbroker.args.args.name, 'data': bpbroker.args.args.data},
		          ['success','message','data'])


	def ServicesGet(self):
		self._ServicesWrapper('bpbroker.services.Get',{'name': bpbroker.args.args.name}, ['success','message','data'])


	def ServicesDelete(self):
		self._ServicesWrapper('bpbroker.services.Delete',{'name': bpbroker.args.args.name}, ['success','message'])


	def ServicesReplace(self):
		self._ServicesWrapper('bpbroker.services.Replace',{'name': bpbroker.args.args.name, 'data': bpbroker.args.args.data},
		          ['success','message','data'])


	def ServicesUpdate(self):
		self._ServicesWrapper('bpbroker.services.Update',{'name': bpbroker.args.args.name, 'data': bpbroker.args.args.data},
		          ['success','message','data'])


	def Exec(self,function,args=False,cols=None,opts={},supress_output=False):
		try:
			if args:  r = eval("%s(**%s)" % (function,args))
			else:  r = eval("%s()" % (function))

			if bpbroker.args.args.cols:  cols = bpbroker.args.args.cols

			# TODO - not sure whether we'll reuse this code at all or duplicate in wrappers as needed?
			if not supress_output and bpbroker.args.args.format == 'json':  print bpbroker.output.Json(r,cols,opts)
			elif not supress_output and bpbroker.args.args.format == 'text':  print bpbroker.output.Text(r,cols,opts)
			elif not supress_output and bpbroker.args.args.format == 'csv-noheader':  print bpbroker.output.Csv(r,cols,{'no_header': True})
			elif not supress_output and bpbroker.args.args.format == 'csv':  print bpbroker.output.Csv(r,cols,opts)

			return(r)

		except:
			raise


