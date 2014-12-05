Updated: December 2, 2014

**Partner Profile**

*   CloudMine - "Blend public cloud with private data to accelerate the next generation of enterprise mobility"
*   [www.cloudmine.me](https://cloudmine.me)
*   Customer Support:

    *   CenturyLinksupport@cloudmine.me
    *   CenturyLink Cloud Account Alias: CMNE
    *   All support requests can be sent to CenturyLinksupport@cloudmine.me. Please include as much detail as possible regarding your issue and list pertinent contact information so that our team may address your question quickly.

# **Description**

CloudMine has integrated their technology with the CenturyLink Cloud platform.  The purpose of this KB article is to help the reader take advantage of this integration to achieve rapid time-to-value for this Mobile Backend solution.

# **Audience**

*   CenturyLink Cloud Users

# **Impact**

After reading this article, the user should feel comfortable getting started using the partner technology on CenturyLink Cloud.

# **Prerequisite** 

*   Access to the CenturyLink Cloud platform as an authorized user.

# **Detailed Steps**

Follow these step by step instructions to get started with a single-server CloudMine deployment.  

1.  _Locate the Blueprint in the Blueprint Library_. 

    *   Starting from the CenturyLink Control Panel, navigate to the Blueprints Library.
    *   Search for “CloudMine” in the keyword search on the right side of the page.
    *   ![CM1.png](http://ca.tier3.io/ecokb/CM1.png)
    *   Click the “CloudMine Single Server” blueprint.
    *   ![CM2.png](/attachments/token/bwYULRqYHsobb5jyg1jPtOS8W/?name=CM2.png)

2.  _Choose the Blueprint_. 

    *   Click on the "Deploy Blueprint" button.
    *   ![CM3.png](/attachments/token/7w7WQEjwMFz4HocjlmwncK5zD/?name=CM3.png)

3.  _Configure the Blueprint_. 

    *   Complete the information/fields required by the Blueprint wizard.
    *   On the first page, “Customize Blueprint”, ensure the following options are configured.

        *   Password/Confirm Password (This is the root password for the server. Keep this in a secure place).
    *   Set DNS to “Manually Specify” and use “8.8.8.8” (or any other public DNS server of your choice).
    *   Optionally set the server name prefix.
    *   Read and accept the CloudMine terms of service (https://cloudmine.me/eula/centurylink).
    *   The default values are fine for every other option.*   ![CM4.png](/attachments/token/ZXYoYubqKeri9E4zQVk6zjZtd/?name=CM4.png)

4.  _Review and Confirm the Blueprint_. 

    *   Click “next: step 2”
    *   Verify your configuration details.

5.  _Deploy the Blueprint_. 

    *   Once verified, click on the ‘deploy blueprint’ button. You will see the deployment details along with an email stating the Blueprint is queued for execution.
    *   This will kick off the blueprint deploy process and load a page to allow you to track the progress of the deployment. Generally, it will take 15 to 20 minutes to configure all of the components.

6.  _Monitor the Activity Queue_. 

    *   Monitor the Deployment Queue to view the progress of the blueprint.
    *   You can access the queue at any time by clicking the Queue link under the Blueprints menu on the main navigation drop-down.

7.  _Get Busy!_ 

*   Once the blueprint completes successfully, you will receive an email stating that the blueprint build is complete. Please do not use the application until you have received this email notification. 
*   Once the process has completed ­ you will need to determine the public IP address for the newly deployed host. If you navigate to the “Servers” panel and look under “recent activity” you should see a status about “Mapping a Public IP”. Note this public IP, it will be required in future steps.

*   Before navigating to the web interface, you will need to run a script on the server to let the server know what public IP address it was assigned. To do this, ssh into the public IP address as root, using the password set in step 5.

*   ![cm7.png](/attachments/token/sfFfNITb1wPq7Zg1hvFmtWxfw/?name=cm7.png)
*   Once in the server, you will need to run a script in root’s home directory like so:
*   ![cm8.png](/attachments/token/7UnKb2QnZVFmsmhdTVbJKm9q2/?name=cm8.png)
*   After a couple seconds, the script should complete. You are now ready to use CloudMine!8.  Access The CloudMine Interface

#  

# **Pricing**

The costs listed above in Steps 1 and 2 are for the CenturyLink Cloud infrastructure only.  There are no CloudMine license costs or additional fees bundled in.

After deploying this Blueprint, the user can secure entitlements to the CloudMine technology by using the following steps:

*   Contact CloudMine via telephone: (855) 662-7722
*   <span class="s1">Contact Cloudmine via [<span class="s2">contact page one their website</span>](https://cloudmine.me/contact/)</span>

 

# **Frequently Asked Questions**

Where do I obtain my CloudMine License?

*   Contact CloudMine via telephone: (855) 662-7722
*   <span class="s1">Contact Cloudmine via [<span class="s2">contact page one their website</span>](https://cloudmine.me/contact/)</span>

 Who should I contact for support?

*   For issues related to deploying the CloudMine Blueprint on CenturyLink Cloud, please contact [CenturyLinksupport@cloudmine.me](mailto:CenturyLinksupport@cloudmine.me)
*   For issues related to cloud infrastructure (VM’s, network, etc), please open a ticket using the CenturyLink Cloud [Support Process](https://t3n.zendesk.com/entries/23610702-How-do-I-report-a-support-issue-).