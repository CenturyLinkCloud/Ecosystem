# -*- coding: utf-8 -*-
"""
CenturyLink Cloud Blueprint Broker Toolset.

This broker foundation works to support advanced Blueprint deployment requiring
shared state and multi-server/multi-role communication across multiple server deployments.

CenturyLink Cloud: http://www.CenturyLinkCloud.com
Package Github page: 

"""

#import bpclient.api as API
from bpclient.shell import Args, ExecCommand
import bpclient.ping as ping
#import bpclient.services as services
import bpclient.config as config_class


####### module/object vars #######
#_V1_API_KEY = False

config = config_class.Config()

