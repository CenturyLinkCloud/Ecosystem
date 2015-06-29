#!/usr/bin/env bash
 
#
#     _____            _                    _     _       _      _____ _                 _ 
#     /  __ \          | |                  | |   (_)     | |    /  __ \ |               | |
#     | /  \/ ___ _ __ | |_ _   _ _ __ _   _| |    _ _ __ | | __ | /  \/ | ___  _   _  __| |
#     | |    / _ \ '_ \| __| | | | '__| | | | |   | | '_ \| |/ / | |   | |/ _ \| | | |/ _` |
#     | \__/\  __/ | | | |_| |_| | |  | |_| | |___| | | | |   <  | \__/\ | (_) | |_| | (_| |
#      \____/\___|_| |_|\__|\__,_|_|   \__, \_____/_|_| |_|_|\_\  \____/_|\___/ \__,_|\__,_|
#                                        __/ |                                               
#                                       |___/                                                
#
#    Blueprint package install.sh template generated via:
#    http://centurylinkcloud.github.io/Ecosystem/BlueprintManifestBuilder/
#
 
 
 
 
#####################################################

echo "$0 version <VERSION>"

# Update OS
if [ -f /etc/redhat-release ]; then
	/usr/bin/yum -y update
elif [ -f /etc/debian_version ]; then
	apt-get -y update
	apt-get -y upgrade
fi


echo "deb http://repo.gluu.org/ubuntu/ trusty main" > /etc/apt/sources.list.d/gluu-repo.list 
curl http://repo.gluu.org/ubuntu/gluu-apt.key | apt-key add -
apt-get update 
apt-get install gluu-server 


service gluu-server start 
service gluu-server login 


cd /install/community-edition-setup/

cat > setup.properties <<EOF
EOF

./setup.py 

## Register Install
./slack_logger.py 'Gluu (community)' keith_resar 0

exit 0




