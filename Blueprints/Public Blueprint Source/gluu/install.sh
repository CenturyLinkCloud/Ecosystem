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
### IP Address of the interface to host IDP
ip=`/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print \$1}'`
hostname=`/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print \$1}'`
admin_email=keith.resar@ctl.io
httpdKeyPass=Savvis11
shibJksPass=Savvis11
ldapPass=Savvis11
asimbaJksPass=Savvis11

### Do not change this unless you know what you're doing
install_dir=.
ldif_appliance=./output/appliance.ldif
ldif_attributes=./output/attributes.ldif
setup_properties_fn=./setup.properties
apache2_ssl_conf=./output/https_gluu.conf
httpdCertFn=/etc/certs/httpd.crt
openDjCertFn=/etc/certs/opendj.crt
ldapEncodePWCommand=/opt/opendj/bin/encode-password
apache_start_script=/etc/init.d/httpd
tomcat_server_xml=/opt/tomcat/conf/server.xml
ldif_site=./static/cache-refresh/o_site.ldif
certFolder=/etc/certs
staticFolder=./static/opendj
defaultTrustStorePW=changeit
tomcatWebAppFolder=/opt/tomcat/webapps
ldap_admin_port=4444
oxEncodePWCommand=/opt/gluu/bin/encode.py
importLdifCommand=/opt/opendj/bin/import-ldif
tomcat_gluuTomcatWrapper=/opt/tomcat/conf/gluuTomcatWrapper.conf
ldif_base=./output/base.ldif
asimba_configuration=./output/asimba.xml
idp_war=http\://ox.gluu.org/maven/org/xdi/oxidp/2.3.0.Final/oxidp-2.3.0.Final.war
ldif_people=./output/people.ldif
jarCommand=/usr/bin/jar
oxauth_client_id=@!052A.2CF7.D4FC.53B9!0008!6952.12FE
oxTrust_log_rotation_configuration=/opt/tomcat/conf/oxTrustLogRotationConfiguration.xml
httpdKeyFn=/etc/certs/httpd.key
oxauth_error_json=./static/oxauth/oxauth-errors.json
idpMetadataFolder=/opt/idp/metadata
asimbaJksFn=/etc/certs/asimbaIDP.jks
gluuOptBinFolder=/opt/gluu/bin
os_type=ubuntu
tomcat_max_ram=1536
ldap_start_script=/etc/init.d/opendj
ldapBaseFolder=/opt/opendj
oxtrust_war=https\://ox.gluu.org/maven/org/xdi/oxtrust-server/2.3.0.Final/oxtrust-server-2.3.0.Final.war
ldif_scripts=./output/scripts.ldif
distFolder=/opt/dist
inumApplianceFN=052A2CF7D4FC53B900026B3505B7
oxauth_lib=/opt/tomcat/webapps/oxauth/WEB-INF/lib
logError=./setup_error.log
idpFolder=/opt/idp
idpSPFolder=/opt/idp/sp
state=--
oxTrustConfigGeneration=disabled
ce_setup_zip=https\://github.com/GluuFederation/community-edition-setup/archive/version_2.3.zip
tomcat_oxauth_static_conf_json=/opt/tomcat/conf/oxauth-static-conf.json
tomcat_user_home_lib=/home/tomcat/lib
idpWarFolder=/opt/idp/war
outputFolder=./output
oxauth_war=https\://ox.gluu.org/maven/org/xdi/oxauth-server/2.3.0.Final/oxauth-server-2.3.0.Final.war
indexJson=./static/opendj/opendj_index.json
githubBranchName=version_2.3
templateFolder=./templates
inumOrgFN=052A2CF7D4FC53B900015BAE749F
oxauth_ldap_properties=/opt/tomcat/conf/oxauth-ldap.properties
savedProperties=./setup.properties.last
opensslCommand=/usr/bin/openssl
ldap_port=1389
orgName=-
keytoolCommand=/usr/java/latest/bin/keytool
apache2_conf=./output/httpd.conf
idpTempMetadataFolder=/opt/idp/temp_metadata
tomcatHome=/opt/tomcat
ldapDsconfigCommand=/opt/opendj/bin/dsconfig
oxBaseDataFolder=/var/ox
tomcat_log_folder=/opt/tomcat/logs
city=-
oxVersion=2.3.0.Final
baseInum=@!052A.2CF7.D4FC.53B9
log=./setup.log
ldaps_port=1636
oxPhotosFolder=/var/ox/photos
shibJksFn=/etc/certs/shibIDP.jks
defaultTrustStoreFN=/usr/java/latest/lib/security/cacerts
idpSslFolder=/opt/idp/ssl
ldif_groups=./output/groups.ldif
asimba_selector_configuration=/opt/tomcat/conf/asimba-selector.xml
idpLibFolder=/opt/idp/lib
ldif_clients=./output/clients.ldif
idpLogsFolder=/opt/idp/logs
eduperson_schema_ldif=%s/config/schema/96-eduperson.ldif
ldif_scopes=./output/scopes.ldif
oxauth_config_xml=/opt/tomcat/conf/oxauth-config.xml
ldap_jmx_port=1689
countryCode=--
ldap_setup_properties=./templates/opendj-setup.properties
ldapDsCreateRcCommand=/opt/opendj/bin/create-rc-script
ldapPassFn=/home/ldap/.pw
oxTrustRemovedFolder=/var/ox/oxtrust/removed
encode_salt=123456789012345678901234
tomcat_start_script=/etc/init.d/tomcat
ldapDsJavaPropCommand=/opt/opendj/bin/dsjavaproperties
inumOrg=@!052A.2CF7.D4FC.53B9!0001!5BAE.749F
ldapSetupCommand=/opt/opendj/setup
cas_properties=./output/cas.properties
inumAppliance=@!052A.2CF7.D4FC.53B9!0002!6B35.05B7
cas_war=http\://ox.gluu.org/maven/org/xdi/ox-cas-server-webapp/2.3.0.Final/ox-cas-server-webapp-2.3.0.Final.war
ldap_binddn=cn\=directory manager
idpConfFolder=/opt/idp/conf
asimba_war=http\://ox.gluu.org/maven/org/xdi/oxasimba-proxy/2.3.0.Final/oxasimba-proxy-2.3.0.Final.war
oxTrust_properties=/opt/tomcat/conf/oxTrust.properties
configFolder=/etc/gluu/config
schemaFolder=/opt/opendj/template/config/schema
ldap_type=opendj
ldap_hostname=localhost
org_custom_schema=/opt/opendj/config/schema/100-user.ldif
encode_script=/opt/gluu/bin/encode.py
etc_hosts=/etc/hosts
asimba_properties=./output/asimba.properties
gluuOptFolder=/opt/gluu
oxtrust_ldap_properties=/opt/tomcat/conf/oxTrustLdap.properties
etc_hostname=/etc/hostname




EOF

./setup.py -n -f

## Register Install
./slack_logger.py 'Gluu (community)' keith_resar 0

exit 0




