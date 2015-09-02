CenturyLink Cloud  - Blueprint - NAT Public IP to Primary Private IP
=======================

CenturyLink Cloud Blueprint that NATs the servers primary private IP to a public IP.

http://www.CenturyLinkCloud.com


## Obtaining the new IP
This script will add a new public IP NAT or update the ports associated with one if it
already exists.

The current public IP will be written to the following file:

* **Linux** - `/root/sysadmin/public_ip`
* **Windows** - `c:\sysadmin\public_ip`

