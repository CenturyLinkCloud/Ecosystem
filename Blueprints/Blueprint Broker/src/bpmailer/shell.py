"""Command-line interface to bpmailer."""

import argparse
import ConfigParser
import os
import sys
import bpmailer


class Args:

	def __init__(self):
		try:
			bpmailer.args = self
			self.ParseArgs()
			if bpmailer.args.args.config:  bpmailer.config = bpmailer.config_class.Config(bpmailer.args.args.config)
			self.MergeEnvironment()
			self.MergeCommands()
		except Exception as e:
			sys.stderr.write("Fatal error: %s\n" % str(e))
			sys.exit(1)


	def ParseArgs(self):
		parser = argparse.ArgumentParser(description="bpmailer tool")

		########## Global ###########
		parser.add_argument('--config', '-c', required=True, help='Path to non-default configuration file')
		parser.add_argument('--to', dest="to_addr", required=True, help='Destination email address')
		parser.add_argument('--subject', required=True, help='Email subject')
		parser.add_argument('--template', required=True, help='Path to mail template file')
		parser.add_argument('--from', dest="from_addr", help='Source email address')
		parser.add_argument('--css', help='Path to optional css file')
		self.args = parser.parse_args()


	def GetCommand(self):  return(self.args.command)
	def GetArgs(self):  return(self.args)


	def MergeEnvironment(self):
		if 'MAIL_FROM_ADDRESS' in os.environ:  bpmailer.config.data["_bpmailer"]['mail_from_address'] = os.environ['MAIL_FROM_ADDRESS']
		if 'MAIL_CC_ADDRESSES' in os.environ:  bpmailer.config.data["_bpmailer"]['mail_cc_addresses'] = os.environ['MAIL_CC_ADDRESSES'].split(",")
		if 'SMTP_SERVER' in os.environ:  bpmailer.config.data["_bpmailer"]['smtp_server'] = os.environ['SMTP_SERVER']
		if 'SMTP_PORT' in os.environ:  bpmailer.config.data["_bpmailer"]['smtp_port'] = os.environ['SMTP_PORT']
		if 'SMTP_USER' in os.environ:  bpmailer.config.data["_bpmailer"]['smtp_user'] = os.environ['SMTP_USER']
		if 'SMTP_PASSWORD' in os.environ:  bpmailer.config.data["_bpmailer"]['smtp_password'] = os.environ['SMTP_PASSWORD']
		if 'MAIL_FROM_ADDRESS' in os.environ:  bpmailer.config.data["_bpmailer"]['mail_from_address'] = os.environ['MAIL_FROM_ADDRESS']


	def MergeCommands(self):
		if self.args.from_addr:  bpmailer.config.data["_bpmailer"]['mail_from_address'] = self.args.from_addr




class ExecCommand():
	def __init__(self):
		try:
			msg = bpmailer.Mailer(template=self.args.template,subject=self.args.subject,to_addr=self.args.to_addr)
			if self.args.css:  msg.LoadCSS(self.args.css)
			print msg.css
		except Exception as e:
			sys.stderr.write("Fatal error: %s\n" % str(e))
			sys.exit(1)


