#!/usr/bin/env bash

CONTROL_USER="${1}"
CONTROL_PASSWD="${2}"


echo "$0 version <VERSION>"

#
# Create python sandbox
#
#./install_clc_sdk.sh >/dev/null 2>&1
./install_clc_sdk.sh 

#
# Exec api call
#
CONTROL_USER="${CONTROL_USER}" CONTROL_PASSWD="${CONTROL_PASSWD}" clc_api_nat_ip.py

