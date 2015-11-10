#!/bin/bash


EMAIL=$1
HOSTNAME=`hostname`
DATE=`date`
BP_DIR=`pwd`


yum -y update
yum -y install git nodejs npm python-devel libxml2-devel libxslt-devel

## Copy retained files ##
mkdir -p ~/clc_installer
cp * ~/clc_installer


## Python system bootstrap ##
/usr/bin/curl https://bootstrap.pypa.io/get-pip.py | python
#pip install virtualenv 
#virtualenv bootstrap
#source bootstrap/bin/activate

## Python virtual env bootstrap ##
pip install requests bpbroker



## Phase I Activities below here




## Proceed with Phase II install - in background ##
cd ~/clc_installer
(setsid ./install_phase2.sh "$EMAIL" >/dev/null 2>&1 &)

exit 0

