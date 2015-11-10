#!/bin/bash


EMAIL=$1



## Phase II activities below here


## Email completion notice ##
cd /opt/orchestrate_demo/
bpmailer --config bpmailer.json --to $EMAIL --subject "Service Ready on CenturyLink Cloud" \
         --template bpmailer_ready.message --css bpmailer.css \
         --variables -  <<HERE
HOSTNAME=`hostname`
DATACENTER=`hostname|cut -c 1-3`
IP_ADDR=`/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'`
HERE


## Cleanup ##
cd ~
rm -f clc_installer


