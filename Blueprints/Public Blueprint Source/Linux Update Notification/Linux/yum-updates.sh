#!/bin/sh

EMAIL="root"
HOSTNAME=`hostname`


/usr/bin/yum -q check-update > /tmp/$HOSTNAME-yum-updates.txt

if [ -s /tmp/$HOSTNAME-yum-updates.txt ]; then
        /bin/mail -s "$HOSTNAME Patch Updates Available" -a /tmp/$HOSTNAME-yum-updates.txt $EMAIL << HERE
A daily scan of $HOSTNAME shows there are one or more updates which need to be applied.

See attached file for details.

HERE
fi

/bin/rm -f /tmp/$HOSTNAME-yum-updates.txt

