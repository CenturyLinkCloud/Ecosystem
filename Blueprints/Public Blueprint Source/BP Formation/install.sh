#!/bin/bash
 
#
#     _____            _                    _     _       _      _____ _                 _ 
#     /  __ \          | |                  | |   (_)     | |    /  __ \ |               | |
#     | /  \/ ___ _ __ | |_ _   _ _ __ _   _| |    _ _ __ | | __ | /  \/ | ___  _   _  __| |
#     | |    / _ \ '_ \| __| | | | '__| | | | |   | | '_ \| |/ / | |   | |/ _ \| | | |/ _` |
#     | \__/\  __/ | | | |_| |_| | |  | |_| | |___| | | | |   <  | \__/\ | (_) | |_| | (_| |
#      \____/\___|_| |_|\__|\__,_|_|   \__, \_____/_|_| |_|_|\_\  \____/_|\___/ \__,_|\__,_|
#                                        __/ |                                               
#                                       |___/                                                
#
#    Blueprint package install.sh template generated via:
#    http://centurylinkcloud.github.io/Ecosystem/BlueprintManifestBuilder/
#
 
 
 
 
#####################################################

echo "$0 version <VERSION>"


yum -y update

# Install pre-reqs
yum -y install gcc python-devel libxslt-devel

# Install pip
curl https://bootstrap.pypa.io/get-pip.py | sudo python

## Install bpformation
pip install bpformation

## Set documentation
cat >> /etc/motd <<EOF

BPFORMATION has been installed on this host.

Getting started:

1. Complete configuration by modifying your ~/.bpformation configuration file:
   (example file: https://github.com/CenturyLinkCloud/bpformation/blob/master/examples/example_config.ini)

2. Execute bpformation from the command line:

   > bpformation package list
   > bpformation blueprint download --id 1234

3. Help and references available at: https://github.com/CenturyLinkCloud/bpformation


Happy Blueprinting!

EOF

exit 0




