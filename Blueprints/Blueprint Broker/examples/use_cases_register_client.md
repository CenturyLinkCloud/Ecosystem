# Problem Statement

I have a multi-server cluster and need to enable self registration of new nodes from service.  
This requires executing some tools
on the master.


# Solution

Use the bpbroker and bpclient tools in execute mode

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

# Create the server-side RPC extension
Assume we save this in a file "clustertools.py":

```python
def AddNode(rh):
    """Add agent to local ossec manager and return key."""

    ouptut = subprocess.Popen(["YOUR_SPECIAL_COMMAND", "--add-node", rh.RequestingHost()], stdout=subprocess.PIPE).communicate()
    rh.data = output
```

# Create the json configuration
Assume we  write this to the file "clustertools.json":

```json
{
    "clustertools":  { }
}
```


# Install module then start bpbroker on the master server

Linux:
```shell
> service bpbroker stop
> /usr/local/bpbroker/bin/bpbroker configure --config-file clustertools.json
> /usr/local/bpbroker/bin/bpbroker install-extension --script clustertools.py
> /usr/local/bpbroker/bin/bpbroker install-service
> service bpbroker start
```

Windows:
```powershell
Stop-Service bpbroker
"./$env:programfiles/bpbroker/bin/bpbroker.lnk" configure --config-file clustertools.json
"./$env:programfiles/bpbroker/bin/bpbroker.lnk" install-extension --script clustertools.py
"./$env:programfiles/bpbroker/bin/bpbroker.lnk" install-service
Start-Service bpbroker
```

# Run custom RPC from bpclient

Linux:
```shell
> /usr/local/bpbroker/bin/bpclient --bpbroker $BPBROKER_IP:20443 \
                                   execute --method clustertools.AddNode --data xx > output
if [ $? -gt 0 ]; then
	exit $?
fi
```

Windows:
```powershell
$psi = New-object System.Diagnostics.ProcessStartInfo 
$psi.CreateNoWindow = $true 
$psi.UseShellExecute = $false 
$psi.RedirectStandardOutput = $true 
$psi.RedirectStandardError = $true 
$psi.FileName = "C:\Program Files\bpbroker\Python27\Scripts\bpclient.exe" 
$psi.Arguments = @("--bpbroker","$BPBROKER_IP$bpbroker_port","execute","--method","clustertools.AddNode","--data","xx") 
$process = New-Object System.Diagnostics.Process 
$process.StartInfo = $psi 
[void]$process.Start()
$output = $process.StandardOutput.ReadToEnd() 
$process.WaitForExit()
```

