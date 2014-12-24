#!/bin/bash

#
#
#

ADMIN_EMAIL="keith.resar@ctl.io"
OSSEC_KEY=""
OSSEC_ID=""
OSSEC_URL="http://www.ossec.net/files/ossec-hids-2.8.1.tar.gz"

SMTP_SERVER="127.0.0.1"
NETWORK=`ifconfig eth0 | grep Bcast | awk '{print $3}' | cut -c 7- | perl -p -i -e 's/255/0\/24/'`

BP_DIR=`pwd`
BPBROKER_DIR="/usr/local/bpbroker"

#
# Pre-reqs
#
yum -y install gcc || apt-get -y install build-essential


#
# Update OSSEC configuration file
#
cp preloaded-vars.conf cust-preloaded-vars.conf
ADMIN_EMAIL=$ADMIN_EMAIL perl -p -i -e 's/^USER_EMAIL_ADDRESS=.*/USER_EMAIL_ADDRESS="$ENV{ADMIN_EMAIL}"/' cust-preloaded-vars.conf
perl -p -i -e "s/^USER_EMAIL_SMTP=.*/USER_EMAIL_SMTP=\"$SMTP_SERVER\"/" cust-preloaded-vars.conf
perl -p -i -e "s#^USER_WHITE_LIST=.*#USER_WHITE_LIST=\"$NETWORK\"#" cust-preloaded-vars.conf


#
# OSSEC core
#
mkdir /tmp/$$ && cd /tmp/$$
curl -o ossec.tar.gz http://www.ossec.net/files/ossec-hids-2.8.1.tar.gz
tar xfz ossec.tar.gz

cd ossec-hids*
mv "$BP_DIR/cust-preloaded-vars.conf" etc/preloaded-vars.conf
./install.sh
touch /var/ossec/etc/client.keys

/var/ossec/bin/ossec-control start


#
# Configure and enable bpbroker service
#
source $BPBROKER_DIR/bin/activate

cd "$BP_DIR"
if [ ! -f ossec.json ]; then
	cd ../../noarch		# dev mode
fi
cp ossec.json cust-ossec.json
perl -p -i -e "s/\"_access_key\": \"\"/\"_access_key\": \"$OSSEC_KEY\"/g" cust-ossec.json
bpbroker install-service
service bpbroker stop
bpbroker configure --config-file cust-ossec.json
service bpbroker start
bpclient --bpbroker 127.0.0.1:20443 --access-key "$OSSEC_KEY" service replace --name "ossec-manager-$OSSEC_ID" --data "x" >/dev/null


#
# Cleanup
#
rm -rf /tmp/$$





