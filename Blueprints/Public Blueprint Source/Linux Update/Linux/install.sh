#!/bin/bash

#
# This script executes a yum update or apt-get update as appropriate
#


#########################################
#### RHEL and RPM compatible systems
##
if [ -f /etc/redhat-release ]; then
	/usr/bin/yum -y update

#########################################
#### Debian and APT compatible systems
##
elif [ -f /etc/debian_version ]; then
	apt-get -y update
	apt-get -y dist-upgrade
fi

