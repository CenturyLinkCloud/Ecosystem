"""
bp_broker API module.

Listens and responds to ssl connections.  Proxies connection requests to registered event handlers.
"""


import os
import subprocess
from distutils import dir_util, file_util

import bpbroker


#####################################################

INIT_D_HEADER_RPM = """#!/bin/bash

# bpbroker daemon
# chkconfig: 345 25 85
# description: bpbroker service
# processname: bpbroker

"""

INIT_D_HEADER_DEB = """#!/bin/bash

### BEGIN INIT INFO
# Provides:          bpbroker
# Required-Start:    $syslog $remote_fs
# Required-Stop:     
# Default-Start:     3 4 5
# Default-Stop:      0 1 6
# Short-Description: bpbroker service
# Description:       BP Broker service
### END INIT INFO

"""

INIT_D_SCRIPT = '''
DAEMON_PATH="/usr/local/bpbroker/bin/"
BINARY_GREP_STR='/usr/local/bpbroker/bin/python\s+./bpbroker\s+start'

DAEMON=bpbroker
DAEMONOPTS="start"

NAME=bpbroker
DESC="Blueprint Broker Service"
PIDFILE=/var/run/$NAME.pid
SCRIPTNAME=/etc/init.d/$NAME

case "$1" in
start)
	ps ax|egrep "${BINARY_GREP_STR}"|awk '{print $1}' | xargs kill
	printf "%-50s" "Starting $NAME..."
	cd $DAEMON_PATH
	PID=`./$DAEMON $DAEMONOPTS > /dev/null 2>&1 & echo $!`
	#echo "Saving PID" $PID " to " $PIDFILE
        if [ -z $PID ]; then
            printf "%s\n" "Fail"
        else
            echo $PID > $PIDFILE
            printf "%s\n" "Ok"
        fi
;;
status)
        printf "%-50s" "Checking $NAME..."
        if [ -f $PIDFILE ]; then
            PID=`cat $PIDFILE`
            if [ -z "`ps axf | grep ${PID} | grep -v grep`" ]; then
                printf "%s\n" "Process dead but pidfile exists"
            else
                echo "Running"
            fi
        else
            printf "%s\n" "Service not running"
        fi
;;
stop)
        printf "%-50s" "Stopping $NAME"
		ps ax|egrep "$BINARY_GREP_STR"|awk '{print $1}' | xargs kill
		printf "%s\n" "Ok"
		rm -f $PIDFILE
;;

restart)
  	$0 stop
  	$0 start
;;

*)
        echo "Usage: $0 {status|start|stop|restart}"
        exit 1
esac
'''

#####################################################




def _InstallLinux():
	global INIT_D_SCRIPT

	## Write init file ##
	if os.path.exists("/sbin/chkconfig"):
		with open("/etc/init.d/bpbroker","w") as f:  f.write(INIT_D_HEADER_RPM)
	elif os.path.exists("/usr/sbin/update-rc.d"):
		with open("/etc/init.d/bpbroker","w") as f:  f.write(INIT_D_HEADER_DEB)
	else:
		raise(Exception("Unable to install service, not RPM or DEB system"))
	with open("/etc/init.d/bpbroker","aw") as f:  f.write(INIT_D_SCRIPT)
	os.system("chmod oug+x /etc/init.d/bpbroker")
	
	## Dump current configuration ##
	if not os.path.exists("/usr/local/bpbroker/etc"):  os.makedirs("/usr/local/bpbroker/etc")
	if not os.path.exists("/usr/local/bpbroker/lib"):  os.makedirs("/usr/local/bpbroker/lib")
	bpbroker.config.Save("/usr/local/bpbroker/etc/bpbroker.json")

	## Install and start ##
	error = False
	if os.path.exists("/sbin/chkconfig"):
		# RHEL or RPM based
		#error = os.system("/sbin/chkconfig --add bpbroker && /sbin/chkconfig bpbroker on && /sbin/service bpbroker restart")
		error = os.system("/sbin/chkconfig --add bpbroker && /sbin/chkconfig bpbroker")
	elif os.path.exists("/usr/sbin/update-rc.d"):
		#error = os.system("/usr/sbin/update-rc.d bpbroker enable 3 4 5 && /usr/sbin/service bpbroker restart")
		error = os.system("/usr/sbin/update-rc.d bpbroker enable 3 4 5")
	else:
		raise(Exception("Unable to install service, not RPM or DEB system"))

	if error:  raise(Exception("OS error %s executing service install" % error))


def _InstallWindows():
	## Dump current configuration ##
	if not os.path.exists("%s/bpbroker/etc" % os.environ["ProgramW6432"]):  os.makedirs("%s/bpbroker/etc" % os.environ["ProgramW6432"])
	if not os.path.exists("%s/bpbroker/lib" % os.environ["ProgramW6432"]):  os.makedirs("%s/bpbroker/lib" % os.environ["ProgramW6432"])
	if not os.path.exists("%s/bpbroker/bin" % os.environ["ProgramW6432"]):  os.makedirs("%s/bpbroker/bin" % os.environ["ProgramW6432"])
	bpbroker.config.Save("%s/bpbroker/etc/bpbroker.json" % os.environ["ProgramW6432"])

	# Install service
	if os.path.exists("%s\\bpbroker\\bin\\nssm.exe" % os.environ["ProgramW6432"]):
		subprocess.call(["%s\\bpbroker\\bin\\nssm.exe" % os.environ["ProgramW6432"], "stop", "bpbroker"])
		subprocess.call(["%s\\bpbroker\\bin\\nssm.exe" % os.environ["ProgramW6432"], "remove", "bpbroker", "confirm"])
		error = subprocess.call(["%s\\bpbroker\\bin\\nssm.exe" % os.environ["ProgramW6432"],
		                         "install",
								 "bpbroker",
								 "%s\\bpbroker\\Python27\\Scripts\\bpbroker.exe" % os.environ["ProgramW6432"],
								 "start"])
		if error:  raise(Exception("OS error %s installing service: " % error))
	else:
		raise(Exception("nssm.exe not present as expected at %s\\bpbroker\\nssm.exe" % os.environ["ProgramW6432"]))

	# Start service
	#error = subprocess.call(["%s\\bpbroker\\bin\\nssm.exe" % os.environ["ProgramW6432"],
	#                         "start",
	#						 "bpbroker"])
	#if error:  raise(Exception("OS error %s executing service start following install" % error))


def _UninstallLinux():
	pass


def _UninstallWindows():
	subprocess.call(["%s\\bpbroker\\bin\\nssm.exe" % os.environ["ProgramW6432"], "stop", "bpbroker"])
	subprocess.call(["%s\\bpbroker\\bin\\nssm.exe" % os.environ["ProgramW6432"], "remove", "bpbroker", "confirm"])


def Install():
	if os.name=='nt':  _InstallWindows()
	else:  _InstallLinux()

	print "Service installed successfuly and configured to start at boot.  Note service is not yet started"


def Uninstall():
	if os.name=='nt':  _UninstallWindows()
	else:  _UninstallLinux()


def InstallExtension(script):
	"""Copy a python script / package directory to the bp broker system lib.  Used to easily extend bpbroker functionality."""

	if os.name == "nt":  bpbroker_dir = "%s/bpbroker" % os.environ["ProgramW6432"]
	elif os.name == "posix":  bpbroker_dir = "/usr/local/bpbroker"

	try:
		if os.path.isfile(script):  file_util.copy_file(script,bpbroker_dir+"/lib/")
		else:  dir_util.copy_tree(script,bpbroker_dir+"/lib/")
	except Exception as e:
		raise(Exception("Error installing extension %s: %s" % (script,str(e))))



