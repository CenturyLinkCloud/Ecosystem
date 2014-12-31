
# bpmailer

The bpmailer tool, part of the [bpbroker](README.md) suite, facilitates easily adding emailing customers and support personnel as part of an application installation.
As with all items in the bpbroker toolset, this is cross-platform and designed as a drop-in tool to decrease the complexity of deployments by providing a standard set of
success oriented tools.

# Installing
See [bpbroker](README.md#installing).


# Usage
```shell
> bpmailer
usage: bpmailer [-h] --config CONFIG --to TO_ADDR --subject SUBJECT
                --template TEMPLATE [--from FROM_ADDR] [--css CSS]
                [--variables VARIABLES]

> bpmailer --help
usage: bpmailer.py [-h] --config CONFIG --to TO_ADDR --subject SUBJECT
                   --template TEMPLATE [--from FROM_ADDR] [--css CSS]
                   [--variables VARIABLES]

bpmailer tool

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Path to non-default configuration file
  --to TO_ADDR          Destination email address
  --subject SUBJECT     Email subject
  --template TEMPLATE   Path to mail template file
  --from FROM_ADDR      Source email address
  --css CSS             Path to optional css files not referenced in template
  --variables VARIABLES
                        Path to optional key=value variables files or '-' for
                        stdin.
```


# Configuraton
Configuration can be made through any combination of the following methods in increasing order of priority.
* Hardcoded defaults
* json configuration file
* Environment variables
* Command line options

## Hardcoded Defaults
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

## Configuration File
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

## Available environment variables
The following environment variables are interpreted:
* MAIL_FROM_ADDRESS
* MAIL_CC_ADDRESSES
* SMTP_SERVER
* SMTP_PORT
* SMTP_USER
* SMTP_PASSWORD
* MAIL_FROM_ADDRESS

# Quickstart Example
Example executing by passing variables through stdin on Linux using a HERE document.
```shell
> bpmailer --config bpmailer.json  --to toaddr@example.com --subject "Test Message" --template examples/bpmailer_example_message_template \
           --css examples/bpmailer_example_css --from "John Smith <john@example.com>" --variables - <<HERE
NAME=xxxx
foo=bar
HERE
```

Results in the following email:
![alt text][md_assets/bpmailer_exmaple_email.png]

Starting from the email msg and css inside the [examples](examples) directory will deliver a good multi-client experience.  This template is basded on 
