#!/bin/bash

ALIAS="$1"

package_type="Linux"
package_os="Ubuntu"


# Import external pre-reqs
cp ../../../../ecosystem_private_git/shared_assets/slack/slack_logger.py .


# Update uuid
case $ALIAS in 
	KRAP)
		uuid="0d7d0b8e-6b10-4620-9106-9496a3f99044"
		package_prefix="DEV "
		package_visibility="Private"
		;;
	ECO)
		uuid="099dd557-d258-4715-88f0-5bee32b56584"
		package_prefix=""
		package_visibility="Public"
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
echo "Creating ${ALIAS}_${package_os}_${package_type}_${PWD##*/}.zip"
zip Blueprints_Completed_Packages/${ALIAS}_${package_os}_${package_type}_${PWD##*/}.zip  \
	install.sh \
	package.manifest \
	slack_logger.py 



# Cleanup
rm -f slack_logger.py
mv install.sh.$$ install.sh
mv package.manifest.$$ package.manifest


# Publish
if [ "${package_prefix}" = "DEV " ]; then 
	bpformation package upload-and-publish \
			--file Blueprints_Completed_Packages/${ALIAS}_${package_os}_${package_type}_${PWD##*/}.zip \
			--type $package_type --visibility $package_visibility --os $package_os
fi


