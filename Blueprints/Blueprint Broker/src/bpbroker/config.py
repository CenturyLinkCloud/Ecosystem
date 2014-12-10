"""
Access and modify saved/running config.

This is thread safe.

"""


import threading

import bpbroker



#####################################################


class Config(dict):

	def __init__(self, *args, **kwargs):
		self.update(*args, **kwargs)


	def __getattr__(self, attr):
		return self.get(attr)


	def __getattr__(self, key):
		return self[key]


	def __setattr__(self, key, value):
		self[key] = value


	def __setitem__(self, key, value):
		# optional processing here
		super(Config, self).__setitem__(key, value)


	def update(self, *args, **kwargs):
		if args:
			if len(args) > 1:
				raise TypeError("update expected at most 1 arguments, "
								"got %d" % len(args))
			other = dict(args[0])
			for key in other:
				self[key] = other[key]
		for key in kwargs:
			self[key] = kwargs[key]


	def setdefault(self, key, value=None):
		if key not in self:
			self[key] = value
		return self[key]

