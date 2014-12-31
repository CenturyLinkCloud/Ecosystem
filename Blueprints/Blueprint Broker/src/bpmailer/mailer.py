"""
bpmailer mailing module

"""


import re
import premailer

import bpmailer



#####################################################


class Mailer(object):

	def __init__(self):
		self.LoadCSS()
		self.LoadTemplate()
		self.InlineCSS()
		self.ApplyVariables()
		self.Deliver()

	def LoadCSS():
		pass


	def LoadTemplate():
		pass


	def InlineCSS():
		pass


	def ApplyVariables():
		pass


	def Deliver():
		pass


