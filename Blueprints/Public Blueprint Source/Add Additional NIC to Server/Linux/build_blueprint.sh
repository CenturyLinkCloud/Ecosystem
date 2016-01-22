#!/bin/bash

ALIAS="${1}"

# Import external pre-reqs
cp "../../BP Broker/Linux/get-pip.py" .
cp ../noarch/clc_api_add_nic.py .


# Update version counter
cp install.sh install.sh.$$
if [ ! -f .build_version ]; then
    echo "0" > .build_version
	git add .build_version
fi
release=$[$(cat .build_version) + 1]
echo $release > .build_version
cp install.sh install.sh.$$
perl -p -i -e "s/<VERSION>/$release (build `date`)/g" install.*
echo "Building version $release"


# Update uuid
case $ALIAS in
    KRAP)
        uuid="53a36a41-e990-41d7-8e17-cddb5afa047f"
        package_prefix="DEV "
        ;;
    T3N)
        uuid="66222c2a-1a54-45fc-a259-9e92022ec94e"
        package_prefix=""
        ;;
    *)
        echo "Specify alias"
        exit 1
esac
cp package.manifest package.manifest.$$
perl -p -i -e "s/(<NAME>)/\1$package_prefix/ig" package.manifest
perl -p -i -e "s/<UUID>.*?<\/UUID>/<UUID>$uuid<\/UUID>/ig" package.manifest


# Create package
rm -f ../Blueprints_Completed_Packages/${ALIAS}_Linux_add_nic.zip
zip ../Blueprints_Completed_Packages/${ALIAS}_Linux_add_nic.zip  \
	package.manifest \
	install.sh \
	install_clc_sdk.sh \
	get-pip.py \
	clc_api_add_nic.py
ls -l ../Blueprints_Completed_Packages/${ALIAS}_Linux_add_nic.zip


# Cleanup
rm get-pip.py clc_api_add_nic.py install.sh

mv package.manifest.$$ package.manifest
mv install.sh.$$ install.sh


# Publish
if [ "${package_prefix}" = "DEV " ]; then
    bpformation package upload-and-publish \
            --file ../Blueprints_Completed_Packages/${ALIAS}_Linux_add_nic.zip \
            --type Linux --visibility Private --os 'Debian|Ubuntu|RHEL|CentOS'
fi


