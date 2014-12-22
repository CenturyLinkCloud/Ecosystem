# -*- coding: utf-8 -*-
"""
CenturyLink Cloud Blueprint Broker Toolset.

This broker foundation works to support advanced Blueprint deployment requiring
shared state and multi-server/multi-role communication across multiple server deployments.

CenturyLink Cloud: http://www.CenturyLinkCloud.com
Package Github page: 

"""

import sys
import os
if os.name == 'posix':  sys.path.append("/usr/local/bpbroker/lib")
elif os.name == 'nt':  pass

from bpbroker.shell import Args, ExecCommand
import bpbroker.cli as cli
import bpbroker.server as server
import bpbroker.api as API
import bpbroker.discover as discover
import bpbroker.ping as ping
import bpbroker.services as services
import bpbroker.config as config_class
import bpbroker.install as install


####### module/object vars #######
#_V1_API_KEY = False

config = config_class.Config()

