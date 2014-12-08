# **Partner Profile**

*   Bacula - "The open source network backup solution."
*  [http://www.bacula.org/](http://www.bacula.org/ "Bacula Website")
*   Customer Support:
    *   [Bacula Support Website](http://blog.bacula.org/support/)
*   Partner Tier: Silver

# **Description**

CenturyLink has integrated the Bacula network backup solution in to the CenturyLink Cloud platform to enable customers to perform self-service backups. The purpose of this KB article is to help CenturyLink Cloud support personnel understand how to best support our customers and make them successful with this technology. 

Bacula is a set of Open Source, computer programs that permit you (or the system administrator) to manage backup, recovery, and verification of computer data across a network of computers of different kinds. Bacula is relatively easy to use and very efficient, while offering many advanced storage management features that make it easy to find and recover lost or damaged files. In technical terms, it is an Open Source, network based backup program.

According to Source Forge statistics (rank and downloads), Bacula is by far the most popular Open Source program backup program.

As a Silver-certified member of the [CenturyLink Cloud Ecosystem Program](https://t3n.zendesk.com/entries/58187134-CenturyLink-Cloud-Ecosystem-Program-Guide-), the only thing which CenturyLink Cloud certifies is that the Partner technology deploys successfully to the CenturyLink Cloud.  We provide complementary knowledge-base articles to get the customer started, and we rely up on the Cloud Ecosystem partner to provide their own sales and customer support.

# **Audience**
*   CenturyLink Cloud Support Personnel

# **Impact**

The purpose of this KB article is to address common issues which could arise when CenturyLink Cloud customers start using the Bacula integration.

# **Prerequisites**

Any CenturyLink Cloud customer who uses the Bacula integration must satisfy the following pre-requisites:

*   Customers must meet Bacula platform/OS and software requirements.  Refer to the [Bacula documentation.](http://blog.bacula.org/documentation/)
*   Software Install must be able to reach public repos to download bacula-fd via apt-get or yum
*   Customers must know how to configure Bacula.  CenturyLink does not support configuring Bacula!

# **How The Integration Works**

## Script Package and Blueprint Integration Details

CenturyLink Ecosystem team has created a Script Package that will install Bacula and a Blueprint that will call the script package.

The Blueprint has been created to deploy Bacula to an existing server and will not provision any infrastructure.

The Script Package will call a Linux install script that will do the following:

*   Identify the Linux platform, RHEL, CentOS, Debian, Ubuntu
*   Install the Bacula-FD client from the public repo via apt-get or yum, depending on platform
*   Run a sed command to input the users Bacula-FD password in to the Bacula config file
*   Enable Bacula to start on server boot up via chkconfig
*   [Re]Start Bacula after install

# **Frequently Asked Questions**

What should I do when a customer opens a ticket related to Bacula?

*   Validate the customer’s identity via normal [verification procedures](https://t3n.zendesk.com/entries/57394474-How-to-perform-and-verify-PIN-requests).
*   Review the Activity Queue for the customer account:
    *   If the Blueprint has stalled: Attempt to restart the Blueprint, and advise Customer how they can try this themselves in the future
    *   If the Blueprint has failed, or repeatedly stalled:

As a Silver Tier Partner, how do I contact Bacula for Support?

* We don't. Bacula is open source software package and supported by a community via the Bacula website.

How do I troubleshoot Bacula Blueprints?

*   Check to see if the Blueprint deployed successfully
*   Is the platform compatible with the Linux install script? 
*   Was there a problem running the apt-get or yum commands to download the software from the public repos?