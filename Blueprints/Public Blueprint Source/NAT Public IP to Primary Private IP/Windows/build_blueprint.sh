#!/bin/bash

ALIAS="${1}"


# Update version counter
cp install.bat install.bat.$$
if [ ! -f .build_version ]; then
    echo "0" > .build_version
	git add .build_version
fi
release=$[$(cat .build_version) + 1]
echo $release > .build_version
perl -p -i -e "s/<VERSION>/$release (build `date`)/g" install.*
echo "Building version $release"


# Update uuid
case $ALIAS in
    KRAP)
        uuid="209fc0cc-e8dc-48db-b91e-804477007b50"
        package_prefix="DEV "
        ;;
    T3N)
        uuid="1def33fd-4870-4e84-975e-f84f9baf641a"
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
rm -f ../Blueprints_Completed_Packages/${ALIAS}_Windows_nat_primary_ip.zip
zip ../Blueprints_Completed_Packages/${ALIAS}_Windows_nat_primary_ip.zip  \
	package.manifest \
	install.bat \
	install_clc_sdk.bat \
	clc_api_nat_ip.exe 
ls -l ../Blueprints_Completed_Packages/${ALIAS}_Windows_nat_primary_ip.zip


# Cleanup
mv package.manifest.$$ package.manifest
mv install.bat.$$ install.bat


# Publish
if [ "${package_prefix}" = "DEV " ]; then
    bpformation package upload-and-publish \
            --file ../Blueprints_Completed_Packages/${ALIAS}_Windows_nat_primary_ip.zip \
            --type Windows --visibility Private --os 'Windows'
fi


