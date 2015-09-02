#!/bin/bash

# Import external pre-reqs
cp "../../../BP Broker/Linux/get-pip.py" .
cp "../noarch/*.py"


# Update version counter
cp install.sh install.sh.$$
if [ ! -f .build_version ]; then
    echo "0" > .build_version
	    git add .build_version
		fi
		release=$[$(cat .build_version) + 1]
		echo $release > .build_version
		perl -p -i -e "s/<VERSION>/$release (build `date`)/g" install.ps1
		echo "Building version $release"


# Create package
zip ../../Blueprints_Completed_Packages/Linux_nat_primary_ip.zip  \
	package.manifest \
	install* \
	get-pip.py \
	*.py


# Cleanup
rm install_bpbroker.sh get-pip.py *.py


