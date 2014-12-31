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

		########## Run Service ###########
		parser_install = parser_sp1.add_parser('start', help='Start service')


		########## Install Service ###########
		parser_sp1.add_parser('install-service', help='Install and start service')
		parser_sp1.add_parser('uninstall-service', help='Remove service')


		########## Install Extension ###########
		parser_extension = parser_sp1.add_parser('install-extension', help='Install custom extension')
		parser_extension.add_argument('--script', required=True, help='Python script or package directory to install')


		########## Configure ###########
		parser_configure = parser_sp1.add_parser('configure', help='Apply additional configuration to bpbroker service')
		parser_configure.add_argument('--config-file', help='File containing configuration json to apply.  Default is stdin')


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
			if bpbroker.args.args.config:  bpbroker.config = bpbroker.config_class.Config(bpbroker.args.args.config)
			self.Bootstrap()
		except Exception as e:
			sys.stderr.write("Fatal error: %s\n" % str(e))
			sys.exit(1)


	def Bootstrap(self):
		if bpbroker.args.GetCommand() == 'start':  self.Start()
		elif bpbroker.args.GetCommand() == 'install-service':  self.Install()
		elif bpbroker.args.GetCommand() == 'uninstall-service':  self.Uninstall()
		elif bpbroker.args.GetCommand() == 'configure':  self.Configure()
		elif bpbroker.args.GetCommand() == 'install-extension':  self.InstallExtension()


	def Start(self):
		bpbroker.server.Start()


	def Install(self):
		bpbroker.install.Install()


	def Uninstall(self):
		bpbroker.install.Uninstall()


	def InstallExtension(self):
		bpbroker.install.InstallExtension(bpbroker.args.args.script)


	def Configure(self):
		if bpbroker.args.args.config_file:  bpbroker.config_class.ImportConfigFile(bpbroker.args.args.config_file)
		else:  bpbroker.config_class.ImportConfigString(sys.stdin.read())


