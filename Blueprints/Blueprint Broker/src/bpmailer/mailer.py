"""
bpmailer mailing module

"""


import re
import smtplib
import premailer
from email.Header import Header
from email.Utils import parseaddr, formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import bpmailer

# Disable cssutils warning messages about unknown property names
import logging
import cssutils
cssutils.log.setLevel(logging.CRITICAL)

#####################################################


class Mailer(object):

	def __init__(self,template_file,to_addr,subject,css_file=None,cc_addrs=[],from_addr=None,variables={}):
		self.css_file = css_file
		self.subject = subject
		self.to_addr = to_addr
		self.cc_addrs = cc_addrs
		self.from_addr = from_addr
		self.variables = variables

		self.template = open(template_file).read()
		self.ApplyVariables()
		self.InlineCSS()
		self.Deliver()


	def AddCC(self,cc_addrs):
		pass


	def InlineCSS(self):
		if self.css_file:
			self.template = re.sub("<\s*head\s*>","<head>\n<link rel='stylesheet' href='%s'>\n" % self.css_file,self.template,re.IGNORECASE)
		self.message = premailer.transform(self.template)


	def ApplyVariables(self):
		for key,val in self.variables.items():
			self.template = re.sub("%%%s%%" % key,val,self.template)


	def Deliver(self):
		msg = MIMEText(self.message.encode("UTF-8"), 'html', "UTF-8")
		msg['Subject'] = str(Header(unicode(self.subject), "UTF-8"))
		msg['From'] = str(Header(unicode(bpmailer.config.data["_bpmailer"]['mail_from_address']), "UTF-8"))
		msg['To'] = str(Header(unicode(self.to_addr), "UTF-8"))
		msg['CC'] = str(Header(unicode("; ".join(self.cc_addrs)), "UTF-8"))

		s = smtplib.SMTP(bpmailer.config.data['_bpmailer']['smtp_server'],bpmailer.config.data['_bpmailer']['smtp_port'])
		if 'smtp_user' in bpmailer.config.data['_bpmailer'] and len(bpmailer.config.data['_bpmailer']['smtp_user']):
			s.login(str(bpmailer.config.data['_bpmailer']['smtp_user']),str(bpmailer.config.data['_bpmailer']['smtp_password']))
		s.sendmail(bpmailer.config.data["_bpmailer"]['mail_from_address'], self.to_addr, msg.as_string())
		s.quit()


