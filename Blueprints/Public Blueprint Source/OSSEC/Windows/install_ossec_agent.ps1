

param (
	[string]$OSSEC_ID = "",
	[string]$OSSEC_KEY = "",
	[string]$BPBROKER_IP = ""
)



$HOSTNAME=hostname
$bpbroker_port = ":20443"

#
# Install BP Broker
#
&install_bpbroker.ps1


#
# Run base ossec install
#
./ossec-agent-win32-2.7.1.exe /S


#
# Find bpbroker IP if none provided
#
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


#
# Get key
# 
$psi = New-object System.Diagnostics.ProcessStartInfo 
$psi.CreateNoWindow = $true 
$psi.UseShellExecute = $false 
$psi.RedirectStandardOutput = $true 
$psi.RedirectStandardError = $true 
$psi.FileName = "C:\Program Files\bpbroker\Python27\Scripts\bpclient.exe" 
$psi.Arguments = @("--bpbroker","$BPBROKER_IP$bpbroker_port","--access-key",$OSSEC_KEY,"execute","--method","ossec.AddAgent","--data",$HOSTNAME) 
$process = New-Object System.Diagnostics.Process 
$process.StartInfo = $psi 
[void]$process.Start()
$output = $process.StandardOutput.ReadToEnd() 
$process.WaitForExit()
$client_key = $output


#
# Install key
#
$client_key | Out-File "C:\Program Files (x86)\ossec-agent\client.keys" -encoding ascii


#
# Configure Server
#
(gc ossec.conf) -replace 'OSSEC_MANAGER_IP',$BPBROKER_IP | Out-File "C:\Program Files (x86)\ossec-agent\ossec.conf" -encoding ascii


#
# Start service
#
sc start OssecSrv

