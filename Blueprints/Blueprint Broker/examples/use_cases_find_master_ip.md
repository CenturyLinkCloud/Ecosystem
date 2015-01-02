# Problem Statement

I am creating a new database cluster but the client node does not know apriori what IP or hostname to use for the master.
How can I can this IP address?


# Solution

Use the bpbroker and bpclient tool in discover mode.

# Install bpbroker
Perform a bpbroker installation for your platform as documented [here](../README.md#installing)

Linux:
```shell
> curl https://raw.githubusercontent.com/CenturyLinkCloud/Ecosystem/master/Blueprints/Public%20Blueprint%20Source/BP%20Broker/Linux/install_bpbroker.sh | bash
```

Windows:
Include the package or download then unzip: 
```powershell
# Include or Download then unzip
#   https://raw.githubusercontent.com/CenturyLinkCloud/Ecosystem/master/Blueprints/Public Blueprint Source/BP Broker/Blueprints_Completed_Packages/Windows_bpbroker.zip
./install_bpbroker.ps1
```


# Start bpbroker on the master server and register the key

Linux:
```shell
> /usr/local/bpbroker/bin/bpbroker install-service
> service bpbroker start
> /usr/local/bpbroker/bin/bpclient --bpbroker 127.0.0.1:20443 \
                                   --access-key "$OPTIONAL_ACCESS_KEY" service replace \
                                   --name "database-master-$OPTIONAL_CLUSTER_ID" \
                                   --data "x" >/dev/null
```

Windows:
```powershell
"./$env:programfiles/bpbroker/bin/bpbroker.lnk" install-service
Start-Service bpbroker
"./$env:programfiles/bpbroker/bin/bpclient.lnk" --bpbroker 127.0.0.1:20443 \ --access-key "$OPTIONAL_ACCESS_KEY" service replace \ --name "database-master-$OPTIONAL_CLUSTER_ID" \ --data "x" >/dev/null
```

# Run discover mode on bpclient

Linux:
```shell
> BPBROKER_IP=`/usr/local/bpbroker/bin/bpclient discover --name "database-master-$OPTIONAL_CLUSTER_ID"`
```

Windows:
```powershell
$psi = New-object System.Diagnostics.ProcessStartInfo 
$psi.CreateNoWindow = $true 
$psi.UseShellExecute = $false 
$psi.RedirectStandardOutput = $true 
$psi.RedirectStandardError = $true 
$psi.FileName = "C:\Program Files\bpbroker\Python27\Scripts\bpclient.exe" 
$psi.Arguments = @("discover","--name","database-master-$OPTIONAL_CLUSTER_ID") 
$process = New-Object System.Diagnostics.Process 
$process.StartInfo = $psi 
[void]$process.Start()
$output = $process.StandardOutput.ReadToEnd() 
$process.WaitForExit()
$BPBROKER_IP = $output -replace "`t|`n|`r",""
```

