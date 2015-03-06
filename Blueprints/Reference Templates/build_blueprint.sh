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

PACKAGE_NAME="foo"

ALIAS="$1"


# Import external pre-reqs


# Update uuid
case $ALIAS in 
	KRAP)
		uuid="540ec019-7de5-435d-b3ef-9a1651587d44"
		package_prefix="DEV "
		;;
	GOGO)
		uuid="76f15d6c-a60c-4f2a-8064-104640a9436e"
		package_prefix="DEV "
		;;
	*)
		echo "Specify alias"
		exit 1
esac
cp package.manifest package.manifest.$$
perl -p -i -e "s/(<NAME>)/\1$package_prefix/ig" package.manifest
perl -p -i -e "s/<UUID>.*?<\/UUID>/<UUID>$uuid<\/UUID>/ig" package.manifest


# Update version counter
cp install.sh install.sh.$$
if [ ! -f .build_version ]; then
    echo "0" > .build_version
	git add .build_version
fi
release=$[$(cat .build_version) + 1]
echo $release > .build_version
perl -p -i -e "s/<VERSION>/$release (build `date`)/g" install.sh
echo "Building version $release"


# Create package
zip PACKAGENAME.zip  \
zip ${ALIAS}_${PACKAGE_NAME}.zip
	install.sh \
	package.manifest


# Cleanup
mv package.manifest.$$ package.manifest
mv install.sh.$$ install.sh

