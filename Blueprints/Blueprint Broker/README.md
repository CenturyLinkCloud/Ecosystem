


## Installing
BP Broker tooling can be installed on any modern Linux OS (must have Python 2.x already installed) or Windows OS.


### Linux Installation

There are three ways to install on Linux.

If the Python package manager *pip* is already on the system BP Broker is listed in pypi and can be installed using:

```shell
> pip install bpbroker
```

Take note however that standard CenturyLink Cloud tools which depend on bpbroker expect it to be installed in a virtualenv rooted out of */usr/local/bpbroker*.  We have scripts to replicate this install via two methods.

Either download the shell script available *(HERE-tbd)[#]* and include in any packaging you're creating, or download it as part of your package execution.  An example of the latter is:

```shell
> curl https://raw.githubusercontent.com/CenturyLinkCloud/Ecosystem/bp_broker_a/Blueprints/Public%20Blueprint%20Source/BP%20Broker/Linux/install_bpbroker.sh | bash
```

