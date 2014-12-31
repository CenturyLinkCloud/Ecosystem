# CenturyLink Cloud Blueprint Broker Toolset

This repository contains a toolset for 
This repository contains a ***Python SDK*** and a command line interface **CLI** (based on the SDK) to interact with the ***[CenturyLink Cloud](http://www.centurylinkcloud.com)*** API.  At present this aligns most closely to [V1](https://t3n.zendesk.com/categories/20012068-API-v1-0) of the CenturyLink Cloud API though efforts are in process to merge [V2](https://t3n.zendesk.com/categories/20067994-API-v2-0-Beta-) API as it nears full release.

## Contents

* [Installing](#installing)
* [bpbroker](README_bpbroker.md) tool with native service broker capabilities for state management that's easily extendable to decrease Blueprint complexity
* [bpclient](README_bpclient.md) client-side tool that interacts with server-side bpbroker
* [bpmailer](README_bpmailer.md) client-side tool to facilitate rich email with successful transactional delivery routing


## Installing
This toolset is developed to be natively cross-platform with no unreferenced dependencies.  Interactive installation options are available via pip but in reality this is packaged to support a drop-in scripted installation.

### Via CenturyLink Cloud package
bpbroker is available for Linux and Windows on the CenturyLink Cloud platform via a script package.  Execute the script directly on an existing server or add it to a new Blueprint.
These packages are public and their source is available via [this github repo](../Public Blueprint Source/BP Broker/).


### Linux Quickstart
The installation script is available inside [this github repo](../Public Blueprint Source/BP Broker/Linux/install_bpbroker.sh).  It can be installed via the following one-liner:
```shell
> curl https://raw.githubusercontent.com/CenturyLinkCloud/Ecosystem/bp_broker_a/Blueprints/Public%20Blueprint%20Source/BP%20Broker/Linux/install_bpbroker.sh | bash
```

### Windows Quickstart
This installation includes Python 2.7


### Via Pyhton's pip
Cross-platform installation is available via pypi.  Requires *Python 2.7* - this is not currently compatible with Python 3.
If you have pip already installed the following command will get you running.  Other tools built to interact with bpbroker
often expect it to be rooted in /usr/local/bpbroker (Linux) or %programfiles%\bpbroker (Windows).

```shell
# system-wide installation
> pip install bpbroker

# virtualenv installation (Linux)
> pip install virtualenv
> virtualenv /usr/local/bpbroker
> source /usr/local/bpbroker/bin/activate
> pip install bpbroker
```

This should automatically install the following dependencies used by the CLI: argparse,requests, premailer

If you do not have pip (the Python package manager) installed a quickstart install of this prereq on Linux/Mac is:
```shell
> curl https://bootstrap.pypa.io/get-pip.py | sudo python
```


