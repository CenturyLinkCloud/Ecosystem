"""Command-line interface to bpclient."""

import argparse
import ConfigParser
import os
import sys
import bpclient


class Args:

	def __init__(self):
		bpclient.args = self
		self.ParseArgs()
		#self.ImportIni()
		#self.MergeEnvironment()
		#self.MergeCommands()


	def ParseArgs(self):
		parser = argparse.ArgumentParser(description="bpbroker service client")
		parser_sp1 = parser.add_subparsers(title='Commands',dest='command')

		########## Ping ###########
		parser_account = parser_sp1.add_parser('ping', help='Connectivity health check')
		parser_sp2 = parser_account.add_subparsers(dest='sub_command')

		## Get
		parser_account_get = parser_sp2.add_parser('get', help='Get details on root or specified sub-account')
		parser_account_get.add_argument('--alias', help='Operate on specific account alias')


		########## User ###########
		parser_user = parser_sp1.add_parser('users', help='User level activities (list, create, modify)')
		parser_sp3 = parser_user.add_subparsers(dest='sub_command')

		## Get
		parser_user_get = parser_sp3.add_parser('get', help='Get details on specified user')
		parser_user_get.add_argument('--alias', help='Operate on specific account alias')
		parser_user_get.add_argument('--user', required=True, help='Operate on specific user')

		## Delete
		parser_user_delete = parser_sp3.add_parser('delete', help='Delete specified user')
		parser_user_delete.add_argument('--user', required=True, help='Operate on specific user')

		## Suspend
		parser_user_suspend = parser_sp3.add_parser('suspend', help='Suspend specified user')
		parser_user_suspend.add_argument('--user', required=True, help='Operate on specific user')

		## Unsuspend
		parser_user_unsuspend = parser_sp3.add_parser('unsuspend', help='Unsuspend specified user')
		parser_user_unsuspend.add_argument('--user', required=True, help='Operate on specific user')

		## List
		parser_user_list = parser_sp3.add_parser('list', help='List all users')
		parser_user_list.add_argument('--alias', help='Operate on specific account alias')

		## Create
		parser_user_create = parser_sp3.add_parser('create', help='Create new user')
		parser_user_create.add_argument('--alias', help='Operate on specific account alias')
		parser_user_create.add_argument('--user', required=True, help='Operate on specific user')
		parser_user_create.add_argument('--email', required=True, help='Email address')
		parser_user_create.add_argument('--first-name', required=True, metavar='NAME', help='First Name')
		parser_user_create.add_argument('--last-name', required=True, metavar='NAME', help='Last Name')
		parser_user_create.add_argument('--roles', nargs='*', choices=['ServerAdministrator','BillingManager','DNSManager','AccountAdministrator',
		                                                            'AccountViewer','NetworkManager','SecurityManager','ServerOperator'], 
									 help='Space delimited list')

		## Update
		parser_user_update = parser_sp3.add_parser('update', help='Update existing user')
		parser_user_update.add_argument('--alias', help='Operate on specific account alias')
		parser_user_update.add_argument('--user', required=True, help='Operate on specific user')
		parser_user_update.add_argument('--email', required=True, help='Email address')
		parser_user_update.add_argument('--first-name', required=True, metavar='NAME', help='First Name')
		parser_user_update.add_argument('--last-name', required=True, metavar='NAME', help='Last Name')
		parser_user_update.add_argument('--roles', nargs='*', choices=['ServerAdministrator','BillingManager','DNSManager','AccountAdministrator',
		                                                               'AccountViewer','NetworkManager','SecurityManager','ServerOperator'], 
					                    help='Space delimited list')


		########## Server ###########
		parser_server = parser_sp1.add_parser('servers', help='Server level activities (list, create, modify)')
		parser_sp4 = parser_server.add_subparsers(dest='sub_command')

		## Get
		parser_server_get = parser_sp4.add_parser('get', help='Get server details')
		parser_server_get.add_argument('--alias', help='Operate on specific account alias')
		parser_server_get.add_argument('--server', nargs='*', required=True, metavar='NAME', help='Server name')

		## List
		parser_server_list = parser_sp4.add_parser('list', help='List all servers in a location or group')
		parser_server_list.add_argument('--location', metavar='LOCATION', help='Operate on specific datacenter')
		parser_server_list.add_argument('--group', metavar='NAME', help='Group Name (optional)')
		parser_server_list.add_argument('--alias', help='Operate on specific account alias')
		parser_server_list.add_argument('--name-groups', action="store_true", help='Output group names instead of group IDs')

		## List all
		parser_server_list_all = parser_sp4.add_parser('list-all', help='List all servers associated with alias')
		parser_server_list_all.add_argument('--alias', help='Operate on specific account alias')
		parser_server_list_all.add_argument('--name-groups', action="store_true", help='Output group names instead of group IDs')

		## Get templates
		parser_server_templates = parser_sp4.add_parser('templates', help='List all templates')
		parser_server_templates.add_argument('--alias', help='Operate on specific account alias')
		parser_server_templates.add_argument('--location', metavar='LOCATION', help='Operate on specific datacenter')

		## Create
		parser_server_create = parser_sp4.add_parser('create', help='Create new server')
		parser_server_create.add_argument('--alias', help='Operate on specific account alias')
		parser_server_create.add_argument('--location', metavar='LOCATION', help='Operate on specific datacenter')
		parser_server_create.add_argument('--group', required=True,metavar='NAME', help='Group Name or group ID')
		parser_server_create.add_argument('--name', required=True, help='Server name (up to 6 chars)')
		parser_server_create.add_argument('--description', default='', help='Server description')
		parser_server_create.add_argument('--template', required=True, metavar='NAME', help='Template name')
		parser_server_create.add_argument('--backup-level', default='Standard', choices=['Standard','Premier'], help='Storage backup level')
		parser_server_create.add_argument('--cpu', required=True, help='CPU Count (1-8)')
		parser_server_create.add_argument('--ram', required=True, help='RAM GB (1-128)')
		parser_server_create.add_argument('--network', required=True, help='Network name')
		parser_server_create.add_argument('--password', default='', help='Password (if blank system will generate one)')

		## Delete
		parser_server_delete = parser_sp4.add_parser('delete', help='Delete one or more servers')
		parser_server_delete.add_argument('--alias', help='Operate on specific account alias')
		parser_server_delete.add_argument('--server', nargs='*', required=True, metavar='NAME', help='Server name')

		## Archive
		parser_server_archive = parser_sp4.add_parser('archive', help='Archive one or more servers')
		parser_server_archive.add_argument('--alias', help='Operate on specific account alias')
		parser_server_archive.add_argument('--server', nargs='*', required=True, metavar='NAME', help='Server name')

		## Poweron
		parser_server_poweron = parser_sp4.add_parser('poweron', help='Power on one or more servers')
		parser_server_poweron.add_argument('--alias', help='Operate on specific account alias')
		parser_server_poweron.add_argument('--server', nargs='*', required=True, metavar='NAME', help='Server name')

		## Poweroff
		parser_server_poweroff = parser_sp4.add_parser('poweroff', help='Power off one or more servers')
		parser_server_poweroff.add_argument('--alias', help='Operate on specific account alias')
		parser_server_poweroff.add_argument('--server', nargs='*', required=True, metavar='NAME', help='Server name')

		## Reset
		parser_server_reset = parser_sp4.add_parser('reset', help='Reset one or more servers')
		parser_server_reset.add_argument('--alias', help='Operate on specific account alias')
		parser_server_reset.add_argument('--server', nargs='*', required=True, metavar='NAME', help='Server name')

		## Shutdown
		parser_server_shutdown = parser_sp4.add_parser('shutdown', help='Shutdown one or more servers')
		parser_server_shutdown.add_argument('--alias', help='Operate on specific account alias')
		parser_server_shutdown.add_argument('--server', nargs='*', required=True, metavar='NAME', help='Server name')

		## Snapshot
		parser_server_snapshot = parser_sp4.add_parser('snapshot', help='Snapshot one or more servers')
		parser_server_snapshot.add_argument('--alias', help='Operate on specific account alias')
		parser_server_snapshot.add_argument('--server', nargs='*', required=True, metavar='NAME', help='Server name')

		## Pause
		parser_server_pause = parser_sp4.add_parser('pause', help='Pause one or more servers')
		parser_server_pause.add_argument('--alias', help='Operate on specific account alias')
		parser_server_pause.add_argument('--server', nargs='*', required=True, metavar='NAME', help='Server name')

		## Get Credentials
		parser_server_get_credentials = parser_sp4.add_parser('get-credentials', help='Get server administrator login credentials')
		parser_server_get_credentials.add_argument('--alias', help='Operate on specific account alias')
		parser_server_get_credentials.add_argument('--server', nargs='*', required=True, metavar='NAME', help='Server name')

		## Get List Disks
		parser_server_list_disks = parser_sp4.add_parser('list-disks', help='List disks mounted to server')
		parser_server_list_disks.add_argument('--alias', help='Operate on specific account alias')
		parser_server_list_disks.add_argument('--server', nargs='*', required=True, metavar='NAME', help='Server name')


		########## Group ###########
		parser_group = parser_sp1.add_parser('groups', help='Group level activities (list, create, modify)')
		parser_sp5 = parser_group.add_subparsers(dest='sub_command')

		## List
		parser_group_list = parser_sp5.add_parser('list', help='List all groups')
		parser_group_list.add_argument('--location', metavar='LOCATION', help='Operate on specific datacenter')
		parser_group_list.add_argument('--alias', help='Operate on specific account alias')

		## Create
		parser_group_create = parser_sp5.add_parser('create', help='Create new group')
		parser_group_create.add_argument('--location', metavar='LOCATION', help='Operate on specific datacenter')
		parser_group_create.add_argument('--alias', help='Operate on specific account alias')
		parser_group_create.add_argument('--parent', metavar='NAME', help='Parent group name')
		parser_group_create.add_argument('--group', metavar='NAME', required=True, help='Group name')
		parser_group_create.add_argument('--description', help='Group description')

		## Delete
		parser_group_delete = parser_sp5.add_parser('delete', help='Delete specified group')
		parser_group_delete.add_argument('--alias', help='Operate on specific account alias')
		parser_group_delete.add_argument('--location', metavar='LOCATION', help='Operate on specific datacenter')
		parser_group_delete.add_argument('--group', required=True, metavar='NAME', help='Group name')

		## Pause
		parser_group_pause = parser_sp5.add_parser('pause', help='Pause specified group')
		parser_group_pause.add_argument('--alias', help='Operate on specific account alias')
		parser_group_pause.add_argument('--location', metavar='LOCATION', help='Operate on specific datacenter')
		parser_group_pause.add_argument('--group', required=True, metavar='NAME', help='Group name')

		## Poweron
		parser_group_poweron = parser_sp5.add_parser('poweron', help='Power on specified group')
		parser_group_poweron.add_argument('--alias', help='Operate on specific account alias')
		parser_group_poweron.add_argument('--location', metavar='LOCATION', help='Operate on specific datacenter')
		parser_group_poweron.add_argument('--group', required=True, metavar='NAME', help='Group name')

		## Archive
		parser_group_archive = parser_sp5.add_parser('archive', help='Archive specified group')
		parser_group_archive.add_argument('--alias', help='Operate on specific account alias')
		parser_group_archive.add_argument('--location', metavar='LOCATION', help='Operate on specific datacenter')
		parser_group_archive.add_argument('--group', required=True, metavar='NAME', help='Group name')

		## Restore
		# TODO - cannot find groups ID since not listed for archived groups
		#parser_group_list = parser_sp5.add_parser('restore', help='Unarchive specified group')
		#parser_group_list.add_argument('--alias', help='Operate on specific account alias')
		#parser_group_list.add_argument('--location', metavar='LOCATION', help='Operate on specific datacenter')
		#parser_group_list.add_argument('--group', required=True, metavar='NAME', help='Group name')


		########## Billing ###########
		parser_group = parser_sp1.add_parser('billing', help='Billing activities')
		parser_sp6 = parser_group.add_subparsers(dest='sub_command')

		## GetGroupEstimate
		parser_billing_group_estimate = parser_sp6.add_parser('group-estimate', help='Group level estimate')
		parser_billing_group_estimate.add_argument('--alias', help='Operate on specific account alias')
		parser_billing_group_estimate.add_argument('--location', metavar='LOCATION', help='Operate on specific datacenter')
		parser_billing_group_estimate.add_argument('--group', metavar='NAME', required=True, help='Hardware group Name')

		## GetServerEstimate
		parser_billing_server_estimate = parser_sp6.add_parser('server-estimate', help='Group level estimate')
		parser_billing_server_estimate.add_argument('--alias', help='Operate on specific account alias')
		parser_billing_server_estimate.add_argument('--server', required=True, metavar='NAME', help='Server name')

		## GetGroupSummaries
		parser_group_summaries = parser_sp6.add_parser('group-summaries', help='Get charges for all groups within an account')
		parser_group_summaries.add_argument('--alias', help='Operate on specific account alias')
		parser_group_summaries.add_argument('--date-start', metavar='YYYY-MM-DD', help='Date to start. Defaults to first date of cur month')
		parser_group_summaries.add_argument('--date-end', metavar='YYYY-MM-DD', help='Date to end. Defaults to cur day of cur month')

		## GetAccountSummary
		parser_group_summaries = parser_sp6.add_parser('account-summary', help='Get charge summary for an entire account')
		parser_group_summaries.add_argument('--alias', help='Operate on specific account alias')


		########## Network ###########
		parser_network = parser_sp1.add_parser('networks', help='Network activities')
		parser_sp7 = parser_network.add_subparsers(dest='sub_command')

		## List
		parser_network_list = parser_sp7.add_parser('list', help='List all networks')
		parser_network_list.add_argument('--alias', help='Operate on specific account alias')
		parser_network_list.add_argument('--location', metavar='LOCATION', help='Operate on specific datacenter')

		## Get
		parser_network_list = parser_sp7.add_parser('get', help='Get network details')
		parser_network_list.add_argument('--alias', help='Operate on specific account alias')
		parser_network_list.add_argument('--location', metavar='LOCATION', help='Operate on specific datacenter')
		parser_network_list.add_argument('--network', required=True, metavar='NAME', help='Network name')


		########## Queue ###########
		parser_queue = parser_sp1.add_parser('queue', help='Work queue')
		parser_sp8 = parser_queue.add_subparsers(dest='sub_command')

		## List
		parser_queue_list = parser_sp8.add_parser('list', help='List all queued activities')
		parser_queue_list.add_argument('--type', default='All', choices=['All','Pending','Complete','Error'], help='Queue items to show')


		########## Blueprints ###########
		parser_blueprints = parser_sp1.add_parser('blueprints', help='Blueprints')
		parser_sp9 = parser_blueprints.add_subparsers(dest='sub_command')

		## Pending
		parser_blueprints_pending = parser_sp9.add_parser('list-pending', help='List all pending packages')

		## List
		parser_blueprints_list = parser_sp9.add_parser('list', help='List active packages')
		parser_blueprints_list.add_argument('--type', default='Script', choices=['System','Script','Software'], help='Package category')
		parser_blueprints_list.add_argument('--visibility', default='Public', choices=['Public','Private','Shared'], help='Package visibility')

		## List-scripts, software, system
		parser_sp9.add_parser('list-system', help='List all system packages of any visibility')
		parser_sp9.add_parser('list-scripts', help='List all script packages of any visibility')
		parser_sp9.add_parser('list-software', help='List all software packages of any visibility')

		## TODO Validate package

		## Upload Package
		parser_blueprints_upload = parser_sp9.add_parser('package-upload', help='Upload specified package')
		parser_blueprints_upload.add_argument('--package', metavar='PACKAGE.zip', required=True, help='Package zipfile')
		parser_blueprints_upload.add_argument('--ftp', metavar='ftp://user:password@server', help='Properly formed FTP URL (ftp://user:password@server)')

		## Publish package
		parser_blueprints_publish = parser_sp9.add_parser('package-publish', help='Publish specified package')
		parser_blueprints_publish.add_argument('--package', metavar='NAME', required=True, help='Package name')
		parser_blueprints_publish.add_argument('--type', default='Script', choices=['System','Script','Software'], help='Package category')
		parser_blueprints_publish.add_argument('--visibility', default='Private', choices=['Public','Private','Shared'], help='Package visibility')
		# TODO - find way to capture explicit OS IDs or OS groupings like "Windows", "Linux", or if none supplied then display collector UI
		parser_blueprints_publish.add_argument('--os', nargs='*', metavar='ID', help='Operating system(s)')

		## TODO uvp (upload, validate, publish shortcut)


		########## Global ###########
		parser.add_argument('--cols', nargs='*', metavar='COL', help='Include only specific columns in the output')
		parser.add_argument('--config', '-c', help='Ini config file')
		parser.add_argument('--v1-api-key', metavar='KEY', help='V1 API key')
		parser.add_argument('--v1-api-passwd', metavar='PASSWORD', help='V1 API password')
		parser.add_argument('--v2-api-username', metavar='USERNAME', help='V2 API username')
		parser.add_argument('--v2-api-passwd', metavar='PASSWORD', help='V2 API password')
		parser.add_argument('--async', action="store_true", default=False, help='Return immediately after queueing long-running calls')
		parser.add_argument('--quiet', '-q', action='count', help='Supress status output (repeat up to 2 times)')
		parser.add_argument('--verbose', '-v', action='count', help='Increase verbosity')
		parser.add_argument('--format', '-f', choices=['json','table','text','csv'], default='table', help='Output result format (table is default)')
		self.args = parser.parse_args()


	def GetCommand(self):  return(self.args.command)
	def GetArgs(self):  return(self.args)


	def ImportIni(self):
		pass


	def MergeEnvironment(self):
		pass


	def MergeCommands(self):
		pass




class ExecCommand():
	def __init__(self):
		try:
			self.Bootstrap()
		except Exception as e:
			sys.exit(1)


	def Bootstrap(self):
		if bpclient.args.GetCommand() == 'ping':  self.Ping()
		elif bpclient.args.GetCommand() == 'services':  self.Services()


	def Ping(self):
		if bpclient.args.GetArgs().sub_command == 'ping':  self.PingPing()


	def Services(self):
		if bpclient.args.GetArgs().sub_command == 'register':  self.ServicesRegister()
		elif bpclient.args.GetArgs().sub_command == 'get':  self.ServicesGet()
		elif bpclient.args.GetArgs().sub_command == 'replace':  self.ServicesReplace()
		elif bpclient.args.GetArgs().sub_command == 'update':  self.ServicesUpdate()
		elif bpclient.args.GetArgs().sub_command == 'delete':  self.ServicesDelete()


#	def Exec(self,function,args=False,cols=None,supress_output=False):
#		try:
#			if args:  r = eval("%s(**%s)" % (function,args))
#			else:  r = eval("%s()" % (function))
#
#			#  Filter results
#			if bpclient.args.args.cols:  cols = bpclient.args.args.cols
#
#			# Output results
#			# TODO - how do we differentiate blueprints vs. queue RequestIDs?
#			if r is not None and 'RequestID' in r and not bpclient.args.args.async:  
#				r = bpclient.output.RequestBlueprintProgress(r['RequestID'],self._GetLocation(),self._GetAlias(),bpclient.args.args.quiet)
#				cols = ['Server']
#
#			if not isinstance(r, list):  r = [r]
#			if not supress_output and bpclient.args.args.format == 'json':  print bpclient.output.Json(r,cols)
#			elif not supress_output and bpclient.args.args.format == 'table':  print bpclient.output.Table(r,cols)
#			elif not supress_output and bpclient.args.args.format == 'text':  print bpclient.output.Text(r,cols)
#			elif not supress_output and bpclient.args.args.format == 'csv':  print bpclient.output.Csv(r,cols)
#
#			return(r)
#		except bpclient.AccountDeletedException:
#			bpclient.output.Status('ERROR',2,'Unable to process, account in deleted state')
#		except bpclient.AccountLoginException:
#			bpclient.output.Status('ERROR',2,'Transient login error.  Please retry')


