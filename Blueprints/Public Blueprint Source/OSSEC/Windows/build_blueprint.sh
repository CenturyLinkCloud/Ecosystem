#!/bin/bash


# Import external pre-reqs
cp "../../BP Broker/Windows/install_bpbroker.ps1" .
cp "../../BP Broker/Windows/nssm.exe" .
cp "../../BP Broker/Windows/python-2.7.9.zip" .


# Create package
zip ../Blueprints_Completed_Packages/Windows_ossec_agent.zip  \
	install_ossec_agent.ps1 \
	package.manifest \
	ossec-agent-win32-2.7.1.exe \
	ossec.conf \
	nssm.exe \
	python-2.7.9.zip \
	install_bpbroker.ps1


# Cleanup
rm install_bpbroker.ps1 nssm.exe python-2.7.9.zip

