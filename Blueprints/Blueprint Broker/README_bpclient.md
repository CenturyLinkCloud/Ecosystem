
# bpclient

The bpclient tool, part of the [bpbroker](README.md) suite, facilitates easy communication with the bpbroker service as part of an application installation.
As with all items in the bpbroker toolset, this is cross-platform and designed as a drop-in tool to decrease the complexity of deployments by providing a standard set of
success oriented tools.

# Installing
See [bpbroker installation](README.md#installing).


# Usage
```shell
> bpclient.py
usage: bpclient [-h] [--bpbroker host:port] [--access-key KEY]
                [--cols [COL [COL ...]]]
                [--format {json,text,csv,csv-noheader}]
                {ping,service,execute,discover} ...

> bpclient --help
usage: bpclient [-h] [--bpbroker host:port] [--access-key KEY]
                [--cols [COL [COL ...]]]
                [--format {json,text,csv,csv-noheader}]
                {ping,service,execute,discover} ...

bpclient service client

optional arguments:
  -h, --help            show this help message and exit
  --bpbroker host:port, -b host:port
                        BP Broker to communicate with
  --access-key KEY, -a KEY
                        Optional access key required to access some BP Broker
                        modules
  --cols [COL [COL ...]]
                        Include only specific columns in the output
  --format {json,text,csv,csv-noheader}, -f {json,text,csv,csv-noheader}
                        Output result format (text is default)

Commands:
  {ping,service,execute,discover}
    ping                Connectivity health check
    service             Service broker registration and querying
    execute             Execute custom RPC on BP Broker server
    discover            Discover BP server on local subnet

```


# Configuraton
All configuration an interation is via command line parameters.


# Network communication
The toolset uses two modes of network communciation
* [Discovery](#discovery) sends plaintext UDP packets to the broadcast domain port 20443/UDP
* All other communications occur over SSL encrypted traffic by default on 20443/TCP

We recommend retaining the default port assignments to maximize compatibility.

# Access Keys
The bpbroker service may have access keys configured on a per-service basis.  If this is enabled all requests (besides discover) must include
the `--access-key` parameter.  Failure to do so will return an error.


# Discover
The bpbroker/bpclient suite is build to support discovery of service brokers located within the local broadcast domain.  If the **bpbroker** service is running wihtin
the same subnet as the **bpclient** tool there is no need for apriori knowledge of the bpbroker IP address.

Since multiple broker services may exist within the same subnet the discovery protocol is tagged with a specific key.  If the bpbroker contains that key in its
key/value service registry it will reply.  bpclient returns the IP address of the first response it recieves.  To mitigate the risk of unauthorized discovery or 
(more likely) mutliple bpbrokers responding for the same service request and developing a split-brain scenario best practices are to use a unique key.  For example 
if your application is `foo` you may tag one cluster `foo-cluster1` and anotehr `foo-cluster2`.  

Linux bash:
```shell
> BPBROKER_IP=`/usr/local/bpbroker/bin/bpclient discover --name foo-$CLUSTER_ID`
> echo $BPBROKER_IP
192.168.1.1
```

Windows Powershell:
``powershell
$psi = New-object System.Diagnostics.ProcessStartInfo 
$psi.CreateNoWindow = $true 
$psi.UseShellExecute = $false 
$psi.RedirectStandardOutput = $true 
$psi.RedirectStandardError = $true 
$psi.FileName = "C:\Program Files\bpbroker\Python27\Scripts\bpclient.exe" 
$psi.Arguments = @("discover","--name","foo-$CLUSTER_ID") 
$process = New-Object System.Diagnostics.Process 
$process.StartInfo = $psi 
[void]$process.Start()
$output = $process.StandardOutput.ReadToEnd() 
$process.WaitForExit()
$BPBROKER_IP = $output -replace "`t|`n|`r",""
```

# Ping
The ping method is used to verify end-to-end connectivity.  Specify the `--bpbroker` parameter as the endpoint to reach.  Will receive an echo
of the ``--data`` send to the bpbroker service.

```shell
# succssful call
> bpclient --bpbroker 127.0.0.1:20443 ping --data foo
foo

# connectivity successful but no bpbroker running at the target
> bpclient --bpbroker 127.0.0.1:20444 ping --data foo
Fatal error: ('Connection aborted.', error(61, 'Connection refused'))✘-1

# no connectivity
> bpclient --bpbroker 10.0.0.1:20443 ping --data foo
Fatal error: ('Connection aborted.', error(60, 'Operation timed out'))✘-1
```

# Service
Provide access to the key/value service broker data store.  Data stored here is durable across bpbroker service restarts.

## Usage
```shell
> ./bpclient service --help
usage: bpclient service [-h] {register,replace,update,get,delete} ...

positional arguments:
  {register,replace,update,get,delete}
    register            Register supplied data to supplied key
    replace             Replace data associated with supplied key
    update              Update data associated with supplied key
    get                 Return data associated with supplied key
    delete              Delete key from service broker
```

## Service Register

## Service Replace

## Service Update

## Service Get

## Service Delete


# Execute
Execute custom modules implemented on the server side.  An example of this is the **OSSEC** implementation with a custom Python module in [this github repo](Public Blueprint Source/OSSEC/noarch).  We also have a sample module in the [examples](examples) directory.

These custom modules are accessible to bpclient after successful installation on the bpbroker instance using the following command format:

```shell
```

