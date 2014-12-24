#!/bin/bash

#
#
#

OSSEC_KEY=""
OSSEC_ID=""
BPBROKER_IP=""
OSSEC_URL="http://www.ossec.net/files/ossec-hids-2.8.1.tar.gz"

HOSTNAME=`hostname`
BP_DIR=`pwd`
BPBROKER_DIR="/usr/local/bpbroker"

#
# Pre-reqs
#
yum -y install gcc || apt-get -y install build-essential


#
# Discovery bpbroker IP if none provided
#
if [ -z "$BPBROKER_IP" ]; then
	BPBROKER_IP=`/usr/local/bpbroker/bin/bpclient discover --name ossec-manager-$OSSEC_ID`
fi


#
# Update OSSEC configuration file
#
cp preloaded-vars.conf cust-preloaded-vars.conf
perl -p -i -e "s/^USER_AGENT_SERVER_IP=.*/USER_AGENT_SERVER_IP=\"$BPBROKER_IP\"/" cust-preloaded-vars.conf


#
# OSSEC core
#
mkdir /tmp/$$ && cd /tmp/$$
curl -o ossec.tar.gz http://www.ossec.net/files/ossec-hids-2.8.1.tar.gz
tar xfz ossec.tar.gz

cd ossec-hids*
mv "$BP_DIR/cust-preloaded-vars.conf" etc/preloaded-vars.conf
./install.sh



#
# Use bpbroker to generate and retrieve agent key
#
source $BPBROKER_DIR/bin/activate
bpclient --bpbroker $BPBROKER_IP:20443 --access-key "$OSSEC_KEY" execute --method ossec.AddAgent --data $HOSTNAME > /var/ossec/etc/client.keys
if [ $? -gt 0 ]; then
	exit $?
fi

/var/ossec/bin/ossec-control restart




#
# Cleanup
#
rm -rf /tmp/$$





