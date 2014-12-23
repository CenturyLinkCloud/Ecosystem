#!/bin/bash

#
#
#

ADMIN_EMAIL="keith.resar@ctl.io"
OSSEC_KEY=""
BPBROKER=""

SMTP_SERVER="127.0.0.1"
NETWORK=`ifconfig eth0 | grep Bcast | awk '{print $3}' | cut -c 7- | perl -p -i -e 's/255/0\/24/'`
OSSEC_URL="http://www.ossec.net/files/ossec-hids-2.8.1.tar.gz"

BP_DIR=`pwd`
BPBROKER_DIR="/usr/local/bpbroker"

#
# Pre-reqs
#
yum -y install gcc || apt-get install build-essential


#
# Update OSSEC configuration file
#
perl -p -i -e "s/^USER_EMAIL_SMTP=.*/USER_EMAIL_SMTP=\"$SMTP_SERVER\"/" preloaded-vars.conf
perl -p -i -e "s#^USER_WHITE_LIST=.*#USER_WHITE_LIST=\"$NETWORK\"#" preloaded-vars.conf


#
# OSSEC core
#
mkdir /tmp/$$ && cd /tmp/$$
curl -o ossec.tar.gz http://www.ossec.net/files/ossec-hids-2.8.1.tar.gz
tar xfz ossec.tar.gz

cd ossec-hids*
cp $BP_DIR/preloaded-vars.conf etc/
./install.sh
touch /var/ossec/etc/client.keys


#
# Configure and enable bpbroker service
#
source $BPBROKER_DIR/bin/activate
perl -p -i -e "s/\"access_key\": \"\"/\"access_key\": \"$OSSEC_KEY\"/g"
bpbroker configure --config-file ossec.json
bpbroker install-service
bpclient --bpbroker 127.0.0.1:20443 service replace --name ossec --data x

#if [ -z "$BPBROKER" ]; then
#	BPBROKER=`bpclient discover --name ossec-manager`
#fi




#
# Cleanup
#
#rm -rf /tmp/$$





