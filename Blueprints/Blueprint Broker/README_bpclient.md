
# bpclient

The bpclient tool, part of the [bpbroker](README.md) suite, facilitates easy communication with the bpbroker service as part of an application installation.
As with all items in the bpbroker toolset, this is cross-platform and designed as a drop-in tool to decrease the complexity of deployments by providing a standard set of
success oriented tools.

# Installing
See [bpbroker installation](README.md#installing).


# Usage
```shell
> bpclient
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
* [Discovery](#discover) sends plaintext UDP packets to the broadcast domain port 20443/UDP
* All other communications occur over SSL encrypted traffic by default on 20443/TCP

We recommend retaining the default port assignments to maximize compatibility.

# Access Keys
The bpbroker service may have access keys configured on a per-service basis.  If this is enabled all requests (besides discover) must include
the `--access-key` parameter.  Failure to do so will return an error.


# Discover
The bpbroker/bpclient suite is built to support discovery of service brokers located within the local broadcast domain.  If the **bpbroker** service is running wihtin
the same subnet as the **bpclient** tool there is no need for apriori knowledge of the bpbroker IP address.

Since multiple broker services may exist within the same subnet the discovery protocol is tagged with a specific key.  If the bpbroker contains that key in its
[key/value service registry](#service) it will reply.  bpclient returns the IP address of the first response it recieves.  To mitigate the risk of unauthorized discovery or 
(more likely) mutliple bpbrokers responding for the same service request and developing a split-brain scenario best practices are to use a unique key.  For example 
if your application is `foo` you may tag one cluster `foo-cluster1` and another `foo-cluster2`.  

Linux bash:
```shell
> BPBROKER_IP=`/usr/local/bpbroker/bin/bpclient discover --name foo-$CLUSTER_ID`
> echo $BPBROKER_IP
192.168.1.1
```

Windows Powershell:
```powershell
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
of the `--data` sent to the bpbroker service.

```shell
# successful call
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
> bpclient service --help
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
Registers data with the bpbroker service and returns the full data set as a response.  If the specified key already exists will return an error.

```shell
# successful registration
> bpclient  --bpbroker 127.0.0.1:20443 service register --name foo --data bar
bar

# attempted duplicate registration
> bpclient  --bpbroker 127.0.0.1:20443 service register --name foo --data bar
Fatal error: Entry 'foo' already exists
```

## Service Replace
Replaces existing data with the bpbroker service or if none exists creates new.  This is the recommended method if the `--name` may already be
in use but the data itself is not authoritative.

```shell
# 'foo' key already exists
> bpclient  --bpbroker 127.0.0.1:20443 service replace --name foo --data bar
bar

# 'new_key' does not already exist
> bpclient  --bpbroker 127.0.0.1:20443 service replace --name new_key --data bar
bar
```

## Service Update
Updates existing data with the bpbroker service or if none exists creates new.  If data can be parsed into a json object this permits safely adding
additional data.

```shell
# first register the new data point.  Notice different output when we suplied json data vs. a normal string
> bpclient  --bpbroker 127.0.0.1:20443 service register --name foo3 --data '{"key": "special data"}'
{"last_write_ts": 1420068290, "last_write_ip": "127.0.0.1", "key": "special data"}

# then update it
> bpclient  --bpbroker 127.0.0.1:20443 service update --name foo3 --data '{"new_key": "new data"}'
{"last_write_ts": 1420068317, "last_write_ip": "127.0.0.1", "key": "special data", "new_key": "new data"}
```

## Service Get
Performs a read of existing data.  If `--name` does not exist returns an error.

```shell
# key exists
> bpclient  --bpbroker 127.0.0.1:20443 service get --name foo
bar

# key does not exist
> bpclient  --bpbroker 127.0.0.1:20443 service get --name foo_no_exist
Fatal error: Entry 'foo_no_exist' not found
```

## Service Delete
Remove existing `--name`.  No result output on either success or failure.

```shell
> bpclient  --bpbroker 127.0.0.1:20443 service delete --name foo
```


# Execute
Execute custom modules implemented on the server side.  An example of this is the **OSSEC** implementation with a custom Python module in [this github repo](../Public Blueprint Source/OSSEC/noarch).  We also have a sample module in the [examples](examples/example_extension_module.py) directory.

These custom modules are accessible to bpclient after successful installation on the bpbroker instance by specifying the module and method name using the `--method`` parameter.
If there are errors with the access key or if the module is not enabled within the bpbroker service then bpclient will exist with a non-zero error status and provide an error
message.


```shell
> bpclient --bpbroker $BPBROKER_IP:20443 --access-key "$OSSEC_KEY" \
           execute --method ossec.AddAgent --data $HOSTNAME
```

