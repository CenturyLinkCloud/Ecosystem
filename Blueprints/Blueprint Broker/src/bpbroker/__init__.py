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

## Add local path to support imported custom extensions
if os.name == 'posix':  sys.path.append("/usr/local/bpbroker/lib")
elif os.name == 'nt':  sys.path.append("%s/bpbroker/lib" % os.environ["ProgramW6432"])

from bpbroker.shell import Args, ExecCommand
import bpbroker.cli as cli
import bpbroker.server as server
import bpbroker.api as API
import bpbroker.worker as worker
import bpbroker.discover as discover
import bpbroker.ping as ping
import bpbroker.services as services
import bpbroker.config as config_class
import bpbroker.install as install

#if os.name == 'nt':  import bpbroker.windows_service as windows_service

####### module/object vars #######
#_V1_API_KEY = False

config = config_class.Config()

