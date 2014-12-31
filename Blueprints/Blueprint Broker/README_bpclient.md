
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

# Discovery
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
$psi.Arguments = @("discover","--name","foo-$CLUSER_ID") 
$process = New-Object System.Diagnostics.Process 
$process.StartInfo = $psi 
[void]$process.Start()
$output = $process.StandardOutput.ReadToEnd() 
$process.WaitForExit()
$BPBROKER_IP = $output -replace "`t|`n|`r",""
```

{
# Quickstart Example
Example execution by passing variables through stdin on Linux using a HERE document.  Variables can be read via a file or specify `-` for stdin (as shown below).
```shell
> bpclient --config bpclient.json  --to toaddr@example.com --subject "Test Message" \
           --template examples/bpclient_example_message_template \
           --css examples/bpclient_example_css --from "John Smith <john@example.com>" --variables - <<HERE
NAME=xxxx
foo=bar
HERE
```

Results in the following email:

![example_email](md_assets/bpclient_exmaple_email.png)

Starting from the email message and css inside the [examples](examples) directory will deliver a good multi-client experience.  This template is based on the
[ZURB](http://zurb.com/playground/responsive-email-templates) responsive email templates.  bpclient includes a css inliner to easy flexibility and decrease time
to implement.

# Using bpclient inside your CenturyLink Cloud Blueprints
Assume the following scenario

> You are an ISV distributing a new database engine.  You have developed a CenturyLink Cloud Blueprint package and a demo application so potential
> customers can easily test your application.  
>
> Your application takes a few minutes to populate with data which means an "application ready state" and the initial automated installation
> occur asynchronously.  To make using this demo application as easy as possible you want to tell the customer how to access it (the IP address
> and any initial credentials) and provide some example test queries.  To increase conversion rate you want to send this tailored message exactly
> when the application is ready to test.

Include a bpclient configuration file with your installation package that points towards your SMTP relay:
```json
{
	"_bpclient":  {
		"smtp_server": "relay.t3mx.com",
		"smtp_user": "username",
		"smtp_password": "password"
	}
}
```

After the data load is complete append the following lines to the end of your bash installation script:
```shell
> echo IP_ADDRESS=192.168.1.1 | bpclient --config isv_custom.json  --to prospect@example.com \
                                         --subject "Database Ready for Testing" \
                                         --template isv_message_template \
										 --from "ISV Inc <john@example.com>" --variables - 
```


