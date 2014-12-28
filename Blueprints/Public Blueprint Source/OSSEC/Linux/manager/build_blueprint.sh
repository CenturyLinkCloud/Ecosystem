#!/bin/bash


# Import external pre-reqs
cp ../../noarch/* .
cp "../../../BP Broker/Linux/install_bpbroker.sh" .
cp "../../../BP Broker/Linux/get-pip.py" .


# Create package
zip ../../Blueprints_Completed_Packages/Linux_ossec_manager.zip  \
	install_ossec_manager.sh \
	package.manifest \
	preloaded-vars.conf \
	install_bpbroker.sh \
	get-pip.py \
	ossec.* 


# Cleanup
rm ossec.*
rm install_bpbroker.sh get-pip.py

