"""
bp_broker API module.

Listens and responds to ssl connections.  Proxies connection requests to registered event handlers.
"""


import os
import re
import sys

import bpbroker


#####################################################

def _InstallLinux():
	pass


def _InstallWindows():
	pass


def _UninstallLinux():
	pass


def _UninstallWindows():
	pass


def Install():
	if os.name=='nt':  _InstallWindows()
	else:  _InstallLinux()


def Uninstall():
	if os.name=='nt':  _UninstallWindows()
	else:  _UninstallLinux()


