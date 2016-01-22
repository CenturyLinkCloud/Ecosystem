#!/usr/bin/env bash

CONTROL_ALIAS="${1}"
CONTROL_USER="${2}"
CONTROL_PASSWD="${3}"
PORTS="${4}"


echo "$0 version <VERSION>"

#
# Create python sandbox
#
./install_clc_sdk.sh >/dev/null 2>&1
#./install_clc_sdk.sh 

#
# Exec api call
#
mkdir -p /sysadmin
source ./clc_api/bin/activate
CONTROL_ALIAS="${CONTROL_ALIAS}" CONTROL_USER="${CONTROL_USER}" CONTROL_PASSWD="${CONTROL_PASSWD}" ./clc_api_nat_ip.py ${PORTS}
error=$?
if [ $error -ne 0 ]; then
	>&2 echo "`date`    Fatel error, exiting ($error)"
	exit $error
fi
echo "Public IP: `cat /sysadmin/public_ip`"

