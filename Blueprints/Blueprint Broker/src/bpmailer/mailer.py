"""
bpmailer mailing module

"""


import re
import smtplib
import premailer
import bpmailer



#####################################################


class Mailer(object):

	def __init__(self,template_file,subject,css_file=None,to_addr=None,from_addr=None,variables={}):
		self.css_file = css_file
		self.subject = subject
		self.to_addr = to_addr
		self.from_addr = from_addr
		self.variables = variables

		#if css_file:  self.LoadCSS(css_file)

		self.LoadTemplate(template_file)
		self.InlineCSS()
		self.ApplyVariables()
		self.Deliver()


	def AddCC(self,cc_addrs):
		pass


	def LoadTemplate(self,f):
		fh = open(f)
		self.template = fh.read()


	def InlineCSS(self):
		if self.css_file:
			self.template = re.sub("<\s*head\s*>","<head>\n<link rel='stylesheet' href='%s'>\n" % self.css_file,self.template,re.IGNORECASE)


	def ApplyVariables(self):
		for key,val in self.variables.items():
			self.template = re.sub("%%%s%%" % key,val,self.template)


	def Deliver(self):
		pass


