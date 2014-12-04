#!/bin/bash

#
# This script creates a directory and file structure if needed, then
# appends supplied public key to authorized_keys.
#

id $1 >/dev/null 2>&1
if [[ $? != 0 ]]; then
        /usr/sbin/useradd $1
        echo "Creating new user $1"
fi

eval home="~$1"
mkdir -p $home/.ssh
echo "$2" >> $home/.ssh/authorized_keys

chmod 700 $home/.ssh $home/.ssh/authorized_keys
chown -R $1 $home/.ssh $home/.ssh/authorized_keys


