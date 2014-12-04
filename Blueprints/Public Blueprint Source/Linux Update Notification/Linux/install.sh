#!/bin/bash

#
# This script executes a yum update or apt-get update as appropriate
#


#########################################
#### RHEL and RPM compatible systems
##
if [ -f /etc/redhat-release ]; then
	yum -y install mail
	cp yum-updates.sh /etc/cron.daily/
	EMAIL="$1" perl -pi -e 's/EMAIL=\".*\"/EMAIL=\"$ENV{EMAIL}\"/i' /etc/cron.daily/yum-updates.sh
	/etc/cron.daily/yum-updates.sh	# run first time manually

#########################################
#### Debian and APT compatible systems
##
elif [ -f /etc/debian_version ]; then
	apt-get -y update
	apt-get -y install apticron sendmail
	EMAIL="$1" perl -pi -e 's/EMAIL=\".*\"/EMAIL=\"$ENV{EMAIL}\"/i' /etc/apticron/apticron.conf
	/usr/sbin/apticron	# run first time manually
fi

