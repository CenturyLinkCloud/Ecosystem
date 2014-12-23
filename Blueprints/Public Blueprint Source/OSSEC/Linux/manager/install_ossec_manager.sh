#!/bin/bash

#
#
#

ADMIN_EMAIL='keith.resar@ctl.io'

SMTP_SERVER = 'localhost'
OSSEC_URL = "http://www.ossec.net/files/ossec-hids-2.8.1.tar.gz"

BPBROKER_DIR=/usr/local/bpbroker

#
# Pre-reqs
#
yum -y install gcc || apt-get install build-essential


#
# Update OSSEC configuration file
#

#USER_WHITE_LIST - space sperated list of IPs and networks.  Set to current nw/24


#
# OSSEC core
#
mkdir /tmp/$$ && cd /tmp/$$
curl -o ossec.tar.gz http://www.ossec.net/files/ossec-hids-2.8.1.tar.gz
tar xfz ossec.tar.gz

cd ossec-hids*


#
# Configure and enable bpbroker service
#
#source $BPBROKER_DIR/bin/activate




#
# Cleanup
#
#rm -rf /tmp/$$





