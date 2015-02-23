# Webhook Receiver for CenturyLink Cloud
	CLC WebHook Documentation:
	http://www.centurylinkcloud.com/api-docs/v2#webhooks

Receiver Code (PHP)

	Supported CLC webhook event types and actions:
		Types:
			server
			account
			user
		Actions per type:
			created
			deleted
			updated

	Configurable parameters:
		Webhook logs base directory… logs will be placed here.
			- $logsdir = "/var/log/webhooks/logs";
			
		CSV file output
			- $enable_csv = "yes";         // anything other than "yes" disables csv output
		
		Time zone setting.  The code will use this time zone to write it’s time stamps to logs as events come in.
		http://www.php.net/manual/en/timezones.america.php  
			- date_default_timezone_set('America/Los_Angeles');

Webhook Log Cleanup Script

	Configurable parameters:
		How many of each log should be kept. 12 keeps a year's worth.
			- number_to_keep=12

		Webhook logs base directory… should be set the same as in the receiver code.
			- logbase=/var/log/webhooks/logs

Installation on Linux

	# install httpd & php packages
	# On RHEL6 the following does the trick:
	yum -y install httpd httpd-tools php php-cli php-common
	
	mkdir -p /var/log/webhooks/logs
	
	# change ownership to apache user/group
	chown -R apache:apache /var/log/webhooks
	
	Place all php files in Apache's root directory.  Ensure Apache accessible via https with certificate from a valid public cert authority. (e.g. Verisign, GoDaddy, etc.)

Example URLs for Webhook Setup in CLC

	https://webhook.reciever.com/server.php?action=created
	https://webhook.reciever.com/server.php?action=updated
	https://webhook.reciever.com/server.php?action=deleted
	
	https://webhook.reciever.com/account.php?action=created
	https://webhook.reciever.com/account.php?action=updated
	https://webhook.reciever.com/account.php?action=deleted
	
	https://webhook.reciever.com/user.php?action=created
	https://webhook.reciever.com/user.php?action=updated
	https://webhook.reciever.com/user.php?action=deleted

Example receiver output from CLC webhook events

	user_summary_2015-02.log
		"event_type=created","datetime_stamp=2015-02-13-102358","accountAlias=TEST","userName=testingWH","firstName=testing","lastName=webhook","emailAddress=test@centurylinkcloud.com","status=Active","unique_id=54de413eee4b08.64544677"
		"event_type=updated","datetime_stamp=2015-02-13-102456","accountAlias=TEST","userName=testingWH","firstName=testing2","lastName=webhook","emailAddress=test@centurylinkcloud.com","status=Active","unique_id=54de4178a9f600.12967041"
		"event_type=deleted","datetime_stamp=2015-02-13-102526","accountAlias=TEST","userName=testingWH","firstName=testing2","lastName=webhook","emailAddress=test@centurylinkcloud.com","status=Deleted","unique_id=54de4196734a54.58562816"

	user_events_2015-02.csv
		event_type,accountAlias,userName,firstName,lastName,emailAddress,status,eventDate,eventTime,uniqueEvent_id
		created,TEST,testingWH,testing,webhook,test@centurylinkcloud.com,Active,2015-02-13,10:23:58,54de413eee4b08.64544677
		updated,TEST,testingWH,testing2,webhook,test@centurylinkcloud.com,Active,2015-02-13,10:24:56,54de4178a9f600.12967041
		deleted,TEST,testingWH,testing2,webhook,test@centurylinkcloud.com,Deleted,2015-02-13,10:25:26,54de4196734a54.58562816

	user_updated_2015-02.log
		-----------------------------------
		2015-02-13-102456
		54de4178a9f600.12967041
		Array
		(
		[Accept] => application/json
		[Tier3-RsaSha1] => KA5v2WiDq4sBCRk4uWWcRhhotvE8vzdAfhAChEDt780kbHIh38DrflJO5TyW7z3gYvjxN64fEDR5r5dP0hTdPOSg4EE29YMRGTdtpFg4+qadg4Jki9UiHwoRcIFDl2D5Cb446JGZ9wBHvU1/ddaITR085EGNS+3vTh05XM9B8gxyR+mJAbPO7YZNbxSdw2B8G+ZC3fgXaMn7hm2VsYG/WIzerOOrHCLh/9UdvOepphYymLS9PR+A6hkT37yAK31Aw/I8l/fVPrg2XalsDEwE0TuMoxS2YrxSdBk+x81uTH3ZSTEkdrqDHxJX2Ua3CDQPCc5bC7fTTgHFh0/wXqTnvw==
		[Content-Type] => application/json; charset=utf-8
		[Host] => webhook.reciever.com
		[X-NewRelic-ID] => VwUDWF9ACgsBXVJXBw==
		[X-NewRelic-Transaction] => PxQBI1dWCHcCXSNRcnMAUCFzFB8EBw8RVT8=
		[Content-Length] => 212
		[Expect] => 100-continue
		)
		{"uri":"/v2/users/testingWH","accountUri":"/v2/accounts/TEST","accountAlias":"TEST","userName":"testingWH","emailAddress":"test@centurylinkcloud.com","firstName":"testing2","lastName":"webhook","status":"Active"}
