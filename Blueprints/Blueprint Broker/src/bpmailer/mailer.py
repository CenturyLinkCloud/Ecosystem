"""
bpmailer mailing module

"""


import re
import premailer
import bpmailer



#####################################################


class Mailer(object):

	def __init__(self,template,subject,to_addr):
		self.LoadTemplate(template)
		self.subject = subject
		self.to_addr = to_addr


	def AddCC(self,cc_addrs):
		pass


	def LoadCSS(self,f):
		fh = open(f)
		self.css = fh.readlines()


	def LoadTemplate(self,f):
		pass


	def InlineCSS(self):
		pass


	def ApplyVariables(self):
		pass


	def Deliver(self):
		pass

