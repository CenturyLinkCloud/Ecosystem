

param (
	[string]$OSSEC_ID = "",
	[string]$OSSEC_KEY = "",
	[string]$BPBROKER_IP = ""
)



#HOSTNAME=`hostname`
#BP_DIR=`pwd`
#BPBROKER_DIR="/usr/local/bpbroker"



$script_path = split-path -parent $MyInvocation.MyCommand.Definition
$bpbroker_dir = "$env:programfiles\bpbroker"
$bpclient = "$bpbroker_dir\bin\bpclient.lnk"

#
# Install BP Broker
#
#&install_bpbroker.ps1


#
# Run base ossec install
#
#&ossec-agent-win32-2.7.1.exe /S


#
# Find bpbroker IP if none provided
#
echo "pre: $BPBROKER_IP"
if (!$BPBROKER_IP)  {
	$psi = New-object System.Diagnostics.ProcessStartInfo 
	$psi.CreateNoWindow = $true 
	$psi.UseShellExecute = $false 
	$psi.RedirectStandardOutput = $true 
	$psi.RedirectStandardError = $true 
	$psi.FileName = "C:\Program Files\bpbroker\Python27\Scripts\bpclient.exe" 
	$psi.Arguments = @("discover","--name","ossec-manager-x") 
	$process = New-Object System.Diagnostics.Process 
	$process.StartInfo = $psi 
	[void]$process.Start()
	$output = $process.StandardOutput.ReadToEnd() 
	$process.WaitForExit()
	$BPBROKER_IP = $output -replace "`t|`n|`r",""
} 
echo "*$BPBROKER_IP*"
