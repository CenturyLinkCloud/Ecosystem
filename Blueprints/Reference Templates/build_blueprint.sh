#!/bin/bash

#
# Ease support of a development and testing lifecycle with your CenturyLink Cloud
# Blueprints using this script.  
#
#   o Seperate development from production by using different UUIDs
#   o Repeatably build your package archive
#
# Customize to use:
#
#   o Change aliases listed in the case statement
#   o Change UUIDs listed in the case statement
#   o Update PACKAGENAME.zip to you package name
#   o Add additional package files to the zip command as needed
#

ALIAS="$1"


# Import external pre-reqs


# Update uuid
case $ALIAS in 
	KRAP)
		uuid="540ec019-7de5-435d-b3ef-9a1651587d44"
		;;
	GOGO)
		uuid="76f15d6c-a60c-4f2a-8064-104640a9436e"
		;;
	*)
		echo "Specify alias"
		exit 1
esac
perl -p -i -e "s/<UUID>.*?<\/UUID>/<UUID>$uuid<\/UUID>/g" package.manifest


# Create package
zip PACKAGENAME.zip  \
	install.sh \
	package.manifest


# Cleanup


