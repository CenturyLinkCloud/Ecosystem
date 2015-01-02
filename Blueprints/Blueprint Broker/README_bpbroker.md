
# bpbroker

The bpbroker tool, part of the [bpbroker](README.md) suite, facilitates easy communication with the bpbroker service as part of an application installation.
As with all items in the bpbroker toolset, this is cross-platform and designed as a drop-in tool to decrease the complexity of deployments by providing a standard set of
success oriented tools.

# Contents

* [Installing](#installing)
* [Usage](#usage)
* [Configuration](#configuration)
* [Network Communication](#network-communication)
* [Access Keys](#access-keys) - optional authorization
* [Discovery](#discover) - self-discovery of bpbroker nodes
* [Ping](#ping) - end-to-end connectivity check
* [Service](#service) - durable key/value service broker store
* [Execute](#execute) - extending the bpbroker suite with custom modules


# Installing
See [bpbroker installation](README.md#installing).


# Usage
```shell
> bpbroker.py
usage: bpbroker.py [-h] [--config CONFIG]

                   {start,install-service,uninstall-service,install-extension,configure}
                   ...

> bpbroker.py -h
usage: bpbroker.py [-h] [--config CONFIG]

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


# Configuraton
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


# Built-in Modules

# Discover
The bpbroker/bpbroker suite is built to support discovery of service brokers located within the local broadcast domain.  If the **bpbroker** service is running wihtin
the same subnet as the **bpclient** tool there is no need for apriori knowledge of the bpbroker IP address.

Since multiple broker services may exist within the same subnet the discovery protocol is tagged with a specific key.  If the bpbroker contains that key in its
service register then bpbroker will reply.  To mitigate the risk of unauthorized discovery or (more likely) mutliple bpbrokers responding for the same service 
request and developing a split-brain scenario best practices are to use a unique key.  For example if your application is `foo` you may tag one cluster 
`foo-cluster1` and another `foo-cluster2`.  


# Ping
The ping method is used to verify end-to-end connectivity.  Will respond by echoing the `data` parameter supplied in the UDP packet.

# Service
Provide access to the key/value service broker data store.  Data stored here is durable across bpbroker service restarts.  Available methods are:
* Register
* Replace
* Update
* Delete
* Get


# Extending functionality with Custom Modules

# Execute
Execute custom modules implemented on the server side.  An example of this is the **OSSEC** implementation with a custom Python module in [this github repo](../Public Blueprint Source/OSSEC/noarch).  We also have a sample module in the [examples](examples/example_extension_module.py) directory.

These custom modules are accessible to bpbroker after successful installation on the bpbroker instance by specifying the module and method name using the `--method`` parameter.
If there are errors with the access key or if the module is not enabled within the bpbroker service then bpbroker will exist with a non-zero error status and provide an error
message.


```shell
> bpbroker --bpbroker $BPBROKER_IP:20443 --access-key "$OSSEC_KEY" \
           execute --method ossec.AddAgent --data $HOSTNAME
```

