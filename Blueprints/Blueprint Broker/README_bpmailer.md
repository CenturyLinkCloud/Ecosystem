


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

# bpmailer


## Usage
Example executing by passing variables through stdin on Linux using a HERE document.

```shell
> /bpmailer.py --config bpmailer.json  --to toaddr@example.com --subject "Test Message" --template examples/bpmailer_example_message_template \
               --css examples/bpmailer_example_css --from "John Smith <john@example.com>" --variables - <<HERE
NAME=xxxx
foo=bar
HERE
```

## Configuraton
Configuration can be made through any combination of the following methods in increasing order of priority.
* Hardcoded defaults
* json configuration file
* Environment variables
* Command line options

### Hardcoded Defaults
The following defaults are embedded within the tool:
```json
{
    "_bpmailer":  {
        "smptp_server": "127.0.0.1",
        "smtp_port": 25,
        "smtp_user": "bpmailer@%s" % socket.gethostname(),
        "smtp_password": ""
    }
}
```

### Configuration File
This format is compatible with the bpbroker configuration file and both tools can use the same configuration.
See (Example bpmailer_config.json)[examples/bpmailer_example_config.json] also shown below:
```json
{
	"_bpmailer":  {
		"mail_from_address": "test@example.com",
		"mail_cc_addresses": ["cc1@example.com","cc2@example.com"],

		"smtp_server": "127.0.0.1",
		"smtp_port": 25,
		"smtp_user": "",
		"smtp_password": ""
	}
}
```

### Available environment variables
The following environment variables are interpreted:
* MAIL_FROM_ADDRESS
* MAIL_CC_ADDRESSES
* SMTP_SERVER
* SMTP_PORT
* SMTP_USER
* SMTP_PASSWORD
* MAIL_FROM_ADDRESS

