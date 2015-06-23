#!/bin/bash

#
# This script installs the puppet agent (for RPM-based systems this
# is the latest release direectly from Puppet Labs, for APT-based
# systems this is the latest version from the apt repository.
#
# Puppet is started and configured to restart at boot.
#
# No changes are made the the puppet.conf file - these need to be
# completed by the puppet manifest files themselves for full
# functionality.
#
#
# Command line arguments:
#	$1 - puppet master server name
#


#########################################
#### RHEL and RPM compatible systems
##
if [ -f /etc/redhat-release ]; then
	# Add Puppetlabs repo
	rpm -ivh http://yum.puppetlabs.com/puppetlabs-release-el-`perl -p -e 's/.*release (\d+).*/\1/' /etc/redhat-release`.noarch.rpm

	# Install puppet
	yum -y install puppet
	chkconfig puppet on
fi

#########################################
#### RHEL and RPM compatible systems
##
if [ -f /etc/debian_version ]; then
	apt-get -y install /etc/default/puppet
	perl -pi -e 's/START=no/START=yes/i' puppet
fi


#########################################
#### Register with puppet master
##
puppet agent --server $1

