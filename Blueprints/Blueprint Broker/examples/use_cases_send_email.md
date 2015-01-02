# Problem Statement

Sending email from a system with unknown configuration can be difficult.  Are the dependent packages installed, how can I easily customize it,
is there a secure way to send through an authenticated proxy and if so what are my credentials.  

Doing so across both Windows and Linux platforms can be difficult


# Solution

Use the bpmailer tool.

# Install bpbroker
Perform a bpbroker installation for your platform as documented [here](../README.md#installing)

Linux:
```shell
> curl https://raw.githubusercontent.com/CenturyLinkCloud/Ecosystem/master/Blueprints/Public%20Blueprint%20Source/BP%20Broker/Linux/install_bpbroker.sh | bash
```

Windows:
Include the package or download then unzip: 
```powershell
# Include or Download then unzip
#   https://raw.githubusercontent.com/CenturyLinkCloud/Ecosystem/master/Blueprints/Public Blueprint Source/BP Broker/Blueprints_Completed_Packages/Windows_bpbroker.zip
./install_bpbroker.ps1
```


# Create SMTP configuration file
Store this file locally with your package.  If it contains credentials make sure it is removed from the remporary directory after execution.
If sending via CenturyLink Cloud SMTP relay then create relay credentials (follow the 
[SMTP Relay Services](https://t3n.zendesk.com/entries/20902593-SMTP-Relay-Services-Simple-) KB) and use the following configuration.
```json
{
    "_bpmailer":  {
        "smtp_server": "relay.t3mx.com",
        "smtp_user": "username",
        "smtp_password": "password"
    }
}
```


# Customize message file
For a simple message you can use something as basic as the below example, though starting with the [example template](bpmailer_example_message_template) and 
[example css](bpmailer_example_message_css) will provide a better looking foundation.

A basic template can look like the following:

```html
<html>
  <body>
    <p>Thank you %NAME% for installing our product.<p>

    <p>Please find access details below:</p>
    <ul>
      <li>Server is accessible from <b>https://%SERVER_IP</b>
      <li>Help is available from http://www.eample.com/quick_start
    </ul>
  </body>
</html>
```


# Send email
Our example message has two variables we need to substitute - we can do so by passing this information to stdin or we can save to a file.

Linux using stdin:
```shell
> /usr/local/bpbroker/bin/bpmailer \
           --config isv_custom.json  --to prospect@example.com \
           --subject "Database Ready for Testing" \
           --template isv_message_template \
           --from "ISV Inc <john@example.com>" --variables - << HERE
NAME=John Smith
SERVER_IP=10.50.100.10
HERE
```

Windows writing to a file:
```powershell
$config = @"
NAME=John Smith
SERVER_IP=10.50.100.10
"@
$ini| "vars_config" -encoding ascii

&"$env:programfiles" --config isv_custom.json  --to prospect@example.com \ --subject "Database Ready for Testing" \ --template isv_message_template \ --from "ISV Inc <john@example.com>" --variables vars_config
```

