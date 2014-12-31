"""
bpmailer mailing module

"""


import re
import smtplib
import premailer
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import bpmailer



#####################################################


class Mailer(object):

	def __init__(self,template_file,subject,css_file=None,to_addr=None,cc_addrs=[],from_addr=None,variables={}):
		self.css_file = css_file
		self.subject = subject
		self.to_addr = to_addr
		self.cc_addrs = cc_addrs
		self.from_addr = from_addr
		self.variables = variables

		self.template = open(template_file).read()
		self.InlineCSS()
		self.ApplyVariables()
		self.Deliver()


	def AddCC(self,cc_addrs):
		pass


	def InlineCSS(self):
		if self.css_file:
			self.template = re.sub("<\s*head\s*>","<head>\n<link rel='stylesheet' href='%s'>\n" % self.css_file,self.template,re.IGNORECASE)


	def ApplyVariables(self):
		for key,val in self.variables.items():
			self.template = re.sub("%%%s%%" % key,val,self.template)


	def Deliver(self):
		msg = MIMEMultipart('alternative')
		msg['Subject'] = "Link"
		msg['From'] = self.from_addr
		msg['To'] = self.to_addr
		msg['CC'] = "; ".join(self.cc_addrs)
		msg.attach(MIMEText(self.template, 'html'))

		print bpmailer.config.data
		s = smtplib.SMTP(bpmailer.config.data['_bpmailer']['smtp_server'],bpmailer.config.data['_bpmailer']['smtp_port'])
		s.login(bpmailer.config.data['_bpmailer']['smtp_user'],bpmailer.config.data['_bpmailer']['smtp_password'])
		s.sendmail(self.to_addr, self.from_addr, msg.as_string())
		s.quit()


