#!/bin/bash

#
# This script installs Python, pip, and the clc-cli tool.
# After install this script creates a base configuration file to support
# immediate cli use with provided credentials.
#


#########################################
#### RHEL and RPM compatible systems
##
if [ -f /etc/redhat-release ]; then
	yum -y install python-pip


#########################################
#### Debian and APT compatible systems
##
elif [ -f /etc/debian_version ]; then
	apt-get -y update
	apt-get -y install python-pip
fi


#########################################
#### Install and configure clc-cli
##
pip install --upgrade clc-sdk


mkdir -p /usr/local/etc/
cat >/usr/local/etc/clc_config <<HERE
;
; This configuration automatically created by the CenturyLink Cloud cli installer
;

[global]
V1_API_KEY=$1
V1_API_PASSWD=$2

;V2_API_USERNAME=
;V2_API_PASSWD=

;blueprint_ftp_url=ftp://user:password@ftp_fqdn

HERE


