#!/bin/bash

# Import external pre-reqs
cp "../../../BP Broker/Linux/install_bpbroker.sh" .


# Create package
zip ../../Blueprints_Completed_Packages/Linux_ossec_agent.zip  \
	install_ossec_agent.sh \
	package.manifest \
	preloaded-vars.conf \


# Cleanup
rm install_bpbroker.sh


