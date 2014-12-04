#
# This downloads and installs the specified puppet agent directly from
# the Puppet Labs distribution repo.  Set the specific versiojn/filename
# below for proper execution 
#
# Puppet is started and configured to restart at boot.
#
# No changes are made the the puppet.conf file - these need to be
# completed by the puppet manifest files themselves for full
# functionality.
#
#
# Command line arguments:
#	$1 - puppet master server name
#


$file="puppet-3.6.0.msi"    # SET PUPPET FILENAME/VERSION FOR PROPER EXECUTION



#########################################
#### Download file and install
##

$url = "https://downloads.puppetlabs.com/windows/$file"

$WebClient = New-Object System.Net.WebClient
$WebClient.Credentials = New-Object System.Net.Networkcredential("","")
$WebClient.DownloadFile( $url, "c:\windows\temp\puppet.msi" )


param( [string]$server)
Write-Host $server
msiexec /qn /i c:\windows\temp\puppet.msi SERVER=$server


