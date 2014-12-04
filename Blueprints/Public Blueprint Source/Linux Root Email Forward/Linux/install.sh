#!/bin/bash

#
# This script executes a yum update or apt-get update as appropriate
#


# Add alias
grep -v "^root:" /tmp/aliases >/tmp/aliases; mv /tmp/aliases /etc/aliases
echo "root:	$1	# added by CenturyLink Cloud Blueprint on `date`" >> /etc/aliases
/usr/bin/newaliases


# Send Test message
if [ $2 = 'Yes' ]; then
	#########################################
	#### RHEL and RPM compatible systems
	##
	if [ -f /etc/redhat-release ]; then
		yum -y install mail
	
	#########################################
	#### Debian and APT compatible systems
	##
	elif [ -f /etc/debian_version ]; then
		apt-get -y update
		apt-get -y install sendmail
	fi


	echo "Successful test email forwarding from `hostname` to $1." | mail -s "`hostname` root email forwarding test" root
fi


