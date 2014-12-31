"""Command-line interface to bpmailer."""

import argparse
import ConfigParser
import os
import sys
import bpmailer


class Args:

	def __init__(self):
		bpmailer.args = self
		self.ParseArgs()
		self.MergeEnvironment()
		self.MergeCommands()


	def ParseArgs(self):
		parser = argparse.ArgumentParser(description="bpmailer tool")
		parser_sp1 = parser.add_subparsers(title='Commands',dest='command')

		########## Global ###########
		parser.add_argument('--from', required=True, help='source email address')
		parser.add_argument('--to', required=True, help='destination email address')
		parser.add_argument('--subject', required=True, help='email subject')
		parser.add_argument('--template', required=True, help='Path to mail template file')
		parser.add_argument('--css', help='Path to optional css file')
		parser.add_argument('--config', '-c', required=True, help='Path to non-default configuration file')
		self.args = parser.parse_args()


	def GetCommand(self):  return(self.args.command)
	def GetArgs(self):  return(self.args)


	def MergeEnvironment(self):
		#if 'BPBROKER' in os.environ:  bpmailer.BPROKER = os.environ['BPROKER']
		pass


	def MergeCommands(self):
		#if self.args.bpmailer:  bpmailer.BPBROKER = self.args.bpmailer
		pass




class ExecCommand():
	def __init__(self):
		try:
			if bpmailer.args.args.config:  bpmailer.config = bpmailer.config_class.Config(bpmailer.args.args.config)

			self.Bootstrap()
		except Exception as e:
			sys.stderr.write("Fatal error: %s\n" % str(e))
			sys.exit(1)

