#!/usr/bin/env bash

#
# This script installs the clc-sdk python package including
# any missing dependencies.  This includes a system-wide pip library for
# package management.
#

# Python pre-req
command -v python >/dev/null 2>&1 || { echo "Cannot locate python, required to pre-requisite" >&2; exit 1; }


# pip pre-req (Python package manager)
command -v pip >/dev/null 2>&1 || {
        echo "Cannot locate pip, installing" >&2;
        yum -y install curl gcc || (apt-get update ; apt-get -y install curl gcc);
        curl https://bootstrap.pypa.io/get-pip.py | python;
        pip install --upgrade pip;
        }
PATH="/usr/local/bin:$PATH"
export PATH


# Virtualenv to fence this from the system libraries
echo "Installing and creating virtualenv"
#pip --no-cache install virtualenv
pip install virtualenv
virtualenv ./clc_api
source ./clc_api/bin/activate


# Installing/Upgrading bpbroker package
echo "Installing clc-sdk"
pip --no-cache install --upgrade clc-sdk

