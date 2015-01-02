
# bpbroker

The bpbroker tool, part of the [bpbroker](README.md) suite, facilitates easy communication with the bpbroker service as part of an application installation.
As with all items in the bpbroker toolset, this is cross-platform and designed as a drop-in tool to decrease the complexity of deployments by providing a standard set of
success oriented tools.

# Contents

* [Installing](#installing)
* [Usage](#usage)
* [Configuration](#configuration)
* [Built-in Services](#built-in-services) - Disover, Ping, durable key/value store
* [Extending functionality with Custom Services](#extending-functionality-with-custom-services)


# Installing
See [bpbroker installation](README.md#installing).


# Usage
```shell
> bpbroker
usage: bpbroker [-h] [--config CONFIG]

                   {start,install-service,uninstall-service,install-extension,configure}
                   ...

> bpbroker -h
usage: bpbroker [-h] [--config CONFIG]

                   {start,install-service,uninstall-service,install-extension,configure}
                   ...

bpbroker service

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Path to non-default configuration file

Commands:
  {start,install-service,uninstall-service,install-extension,configure}
    start               Start service
    install-service     Install and start service
    uninstall-service   Remove service
    install-extension   Install custom extension
    configure           Apply additional configuration to bpbroker service
```

## start
Executes bpbroker in server mode.  Will keep the process running in the foreground.  Accepts optional
`--config` parameter to load configuration from a non-default location.  On SIGINT will write configuration.

```shell
> bpbroker start
```

## install-service
Performs a multi-platform service installation and configures service to start at boot.  Under Linux the file `/etc/init.d/bpbroker` is created
and distribution specific tools are used to enable startup at common runlevels.  Under Windows `nssm.exe` is used to register the service.  Running
this command does **not** start the service.

```shell
> bpbroker install-service
```

## uninstall-service
Under Windows this stops then removes the `bpbroker` service.  Not currently implemented for Linux hosts.


## install-extension
Installs a custom extension in the system bpbroker directory (`/usr/local/bpbroker/lib` and `%programfiles%\bpbroker\lib`) so it can be found
by bpbroker after enabling the extension in the configuration.  See [Extending functionality with Custom Services](#extending-functionality-with-custom-services)
for details on how to implement these extensions including working examples.

```shell
> bpbroker install-extension --script FILENAME
```

## configure
Imports specified configuration and saves with the global configuration file (or a local file if the `--config` option is used).  
Can be safely run multiple times with the same data or with differing data.  bpbroker configuration is strictly additive so only
net new variables are applied and existing configurations remain untouched.

**This should not be executed with the `bpbroker` service is running as changes will be overwritten.**

```shell
# supply configuration via filename
> sudo service bpbroker stop
> bpbroker configure --config-file FILENAME
> sudo service bpbroker start

# supply configuration via stdin
> bpbroker configure <<HERE
{
	"services": {
		"_access_key": "secret"
	}
}
HERE
```

# Configuration
Configuration can be made through any combination of the following methods in increasing order of priority.
* Hardcoded defaults
* Global json configuration file (`/usr/local/bpbrokr/etc/bpbroker.json` Linux and `%programfiles%\bpbroker\etc\bpbroker.json` Windows)
* Local json configuration file specified with `--config` option
* Command line options

## Hardcoded Defaults
The following defaults are embedded within the tool:
```json
{
    "api": {
    	"listen_port": 20443,
    	"listen_ip": "",    # default bind to all interfaces
    	"ssl_cert": "%s/dummy_api.crt" % os.path.dirname(bpbroker.__file__),
    	"ssl_key": "%s/dummy_api.key" % os.path.dirname(bpbroker.__file__),
    },
    "worker":  {
    },
    "_global":  {
        "healthcheck_freq_sec": 10,
    },
    "_config":  {
        "backup_freq_secs": 3600,
        "backup_retain_n": 24,
    },

    "ping":  { },
    "services":  { },
}
```

## Configuration File
The configuration file is written one program exit.  By default this is the global json configuration file unless the `--config` command
line option has been used.  The written configuration file includes all hardcoded defaults unles they have been overwritten.  This content
can be extended by using the `configure` execution mode and the `--config-file` parameter.

The configuration file contains both configuration options as well as any data stored within the service registry.


## Access Keys
The bpbroker service may have access keys configured on a per-service basis.  If this is enabled all cleint requests (besides discover) must include
the `access-key` parameter.  Optional access keys are defined within the configuration file, see example below:
```json
{
	"services": {
		"_access_key": "secret"
	}
}
```


# Built-in Services

## Discover
The bpbroker/bpbroker suite is built to support discovery of service brokers located within the local broadcast domain.  If the **bpbroker** service is running wihtin
the same subnet as the **bpclient** tool there is no need for apriori knowledge of the bpbroker IP address.

Since multiple broker services may exist within the same subnet the discovery protocol is tagged with a specific key.  If the bpbroker contains that key in its
service register then bpbroker will reply.  To mitigate the risk of unauthorized discovery or (more likely) mutliple bpbrokers responding for the same service 
request and developing a split-brain scenario best practices are to use a unique key.  For example if your application is `foo` you may tag one cluster 
`foo-cluster1` and another `foo-cluster2`.  


## Ping
The ping method is used to verify end-to-end connectivity.  Will respond by echoing the `data` parameter supplied in the UDP packet.

## Service
Provide access to the key/value service broker data store.  Data stored here is durable across bpbroker service restarts.  Available methods are:
* Register
* Replace
* Update
* Delete
* Get


# Extending functionality with Custom Services
This built in discovery and durable key/value service broker are compatible with a great many use cases.  However extended functionality is often
required if work tasks need to be executed on the local server itself.  Custom services can be easily adapted from the 
[provided example extension module](examples/example_extension_module.py).

## Extension Namespace and Accessing from bpclient


## Python server-side interface
Your custom module should look similar to the example below.  It requires a function with a single parameter (extended http request handler).  You will
have access to a lot of information about the request itself from the handler.

Your extension must set two parameters:
* rh.status - http return status code.  If not 200 then also set rh.status_message
* rh.data - if returning a 200 status code (success) populate this with the data you want your client to revieve

```python
def Test(rh):
	"""Echo source host and querystring back in response. """

	# A successful return is clean and looks like this:
	rh.data = json.dumps(rh.qs)

	# Where you to choose an errored response you may set the following:
	#rh.status = 500
	#rh.status_message = "End client visible message text explaining 500 error"
```

Clients have access to the extension only if all of the following are true:
* Extension is defined in the json configuration file (whitelist)
* Extension does not have a `_` at the start of the method name (used to hide "private" functions from this RPC)
* Access key matches (if one is provided)
* Module can be imported without error
* Method exists


## Working example using OSSEC
A working example that implements the server-side functions to register an **OSSEC** agent is available in [this github repo](../Public Blueprint Source/OSSEC/noarch) and below:

The filename is `ossec.py` and the method name is `AddAgent` which means:
* bpbroker needs a configuration whitelist entry of `ossec`
* bpclient executes the method `ossec.AddAgent`

```python
def AddAgent(rh):
	"""Add agent to local ossec manager and return key."""

	global OSSEC_DIR

	# Make sure not already registered
	with open("%s/etc/client.keys" % OSSEC_DIR) as f:  client_keys = f.readlines()

	if 'data' not in rh.qs or re.search("^a-z0-9\-",rh.qs['data'].lower()):
		rh.status = 500
		rh.status_message = "Invalid source host name content"
	elif re.search("\s%s\s" % rh.RequestingHost(),''.join(client_keys)):
		rh.status = 500
		rh.status_message = "Unable to add requested host IP in use"

	else:
		# Find next agent
		try:
			id = str(int(re.sub("\s.*","",sorted(client_keys)[-1]))+1).zfill(3)
		except IndexError:
			id = "001"

		# Generate key
		key = ''.join(random.SystemRandom().choice(string.hexdigits) for _ in range(64))

		# Append to client_keys file
		with bpbroker.config.rlock:
			with open("%s/etc/client.keys" % OSSEC_DIR,"aw") as f:
				f.write("%s %s %s %s\n" % (id,rh.qs['data'],rh.RequestingHost(),key))
			subprocess.Popen(["%s/bin/ossec-control" % OSSEC_DIR, "restart"], stdout=subprocess.PIPE).communicate()

		# Export encoded key
		rh.data = "%s %s %s %s" % (id,rh.qs['data'],rh.RequestingHost(),key)
```

The associated configuration file is relatively terse.  It includes the minimum which is a top-level definition of the `ossec` namespace
and in this case also keeps a placeholder for an `access_key`.

```json
{
	"ossec":  {
		"_access_key": ""
	}
}
```

