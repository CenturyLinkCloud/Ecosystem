# -*- coding: utf-8 -*-
"""
CenturyLink Cloud Blueprint Broker Toolset.

Facilitates email delivery as part of Bluerprint deployment.

CenturyLink Cloud: http://www.CenturyLinkCloud.com
Package Github page: 

"""

from bpmailer.shell import Args, ExecCommand
import bpmailer.cli as cli
import bpmailer.config as config_class


import requests
requests.packages.urllib3.disable_warnings()


config = config_class.Config()

