#!/bin/bash

#
# This script installs the bpbroker package (+ associated scripts) including
# any missing dependencies.  This includes a system-wide pip library for
# package management.
#

# Python pre-req
command -v python >/dev/null 2>&1 || { echo >&2 "Cannot locate python, required to pre-requisite"; exit 1; }

yum -y install gcc python-devel libxml2-devel libxslt-devel || \
	(apt-get update && apt-get -y install zlib1g-dev gcc pip libxml2-dev libxslt1-dev python-dev python-dev libxslt1-dev python-lxml)

# pip pre-req (Python package manager)
command -v pip >/dev/null 2>&1 || { 
	echo >&2 "Cannot locate pip, installing"; 
	yum -y install curl gcc || (apt-get update && apt-get -y install curl gcc)
	curl https://bootstrap.pypa.io/get-pip.py | python;
	pip install --upgrade pip;
	}

# Virtualenv to fence this from the system libraries
pip --no-cache install virtualenv
virtualenv /usr/local/bpbroker
mkdir -p /usr/local/bpbroker/{etc,lib,bin}
source /usr/local/bpbroker/bin/activate

# Installing/Upgrading bpbroker package
pip --no-cache install --upgrade bpbroker

