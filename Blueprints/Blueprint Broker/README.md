# CenturyLink Cloud Blueprint Broker Toolset

This repository contains a toolset for 
This repository contains a ***Python SDK*** and a command line interface **CLI** (based on the SDK) to interact with the ***[CenturyLink Cloud](http://www.centurylinkcloud.com)*** API.  At present this aligns most closely to [V1](https://t3n.zendesk.com/categories/20012068-API-v1-0) of the CenturyLink Cloud API though efforts are in process to merge [V2](https://t3n.zendesk.com/categories/20067994-API-v2-0-Beta-) API as it nears full release.

## Contents

* [Installing](#installing)
* [bpbroker](README_bpbroker.md) tool with native service broker capabilities for state management that's easily extendable to decrease Blueprint complexity
* [bpclient](README_bpclient.md) client-side tool that interacts with server-side bpbroker
* [bpmailer](README_bpmailer.md) client-side tool to facilitate rich email with successful transactional delivery routing


## Installing
This toolset is developed to be natively cross-platform

### Via Pyhthon's pip
Cross-platform installation is available via pypi.  Requires *Python 2.7* - this is not currently compatible with Python 3.
If you have pip already installed the following command will get you running:
```
> pip install clc-sdk
```

This should automatically install the following dependencies used by the CLI: prettytable, clint, argparse, requests

If you do not have pip (the Python package manager) installed a quickstart install of this prereq on Linux/Mac is:
```
> curl https://bootstrap.pypa.io/get-pip.py | sudo python
```


