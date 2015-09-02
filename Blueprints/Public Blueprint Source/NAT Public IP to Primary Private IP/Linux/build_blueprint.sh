#!/bin/bash

ALIAS="${1}"

# Import external pre-reqs
cp "../../BP Broker/Linux/get-pip.py" .
cp ../noarch/clc_api_nat_ip.py .


# Update version counter
cp install.sh install.sh.$$
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
        uuid="3387f499-63f7-4538-b283-7699c0d0263d"
        package_prefix="DEV "
        ;;
    T3N)
        uuid="58c00f0e-6af6-41c1-a50f-307ec22f8b83"
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
rm -f ../Blueprints_Completed_Packages/${ALIAS}_Linux_nat_primary_ip.zip
zip ../Blueprints_Completed_Packages/Linux_nat_primary_ip.zip  \
	package.manifest \
	install* \
	get-pip.py \
	clc_api_nat_ip.py
ls -l ../Blueprints_Completed_Packages/${ALIAS}_Linux_nat_primary_ip.zip


# Cleanup
rm get-pip.py clc_api_nat_ip.py install.sh

mv package.manifest.$$ package.manifest
mv install.sh.$$ install.sh


# Publish
if [ "${package_prefix}" = "DEV " ]; then
    bpformation package upload-and-publish \
            --file ../Blueprints_Completed_Packages/${ALIAS}_Linux_nat_primary_ip.zip \
            --type Linux --visibility Private --os '*'
fi
