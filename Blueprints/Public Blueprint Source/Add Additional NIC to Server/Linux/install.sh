#!/usr/bin/env bash

CONTROL_ALIAS="${1}"
CONTROL_USER="${2}"
CONTROL_PASSWD="${3}"
NETWORK="${4}"


echo "$0 version <version>"

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
CONTROL_ALIAS="${CONTROL_ALIAS}" CONTROL_USER="${CONTROL_USER}" CONTROL_PASSWD="${CONTROL_PASSWD}" NETWORK='${NETWORK}' ./clc_add_nic.py
error=$?
if [ $error -ne 0 ]; then
	>&2 echo "`date`    Fatal error, exiting ($error)"
	exit $error
fi

