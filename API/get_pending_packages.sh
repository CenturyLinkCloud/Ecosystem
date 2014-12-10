#!/bin/bash
                                                                                   
#   ,-----.                 ,--.                          ,--.   ,--.        ,--.      #
#  '  .--./ ,---. ,--,--, ,-'  '-.,--.,--.,--.--.,--. ,--.|  |   `--',--,--, |  |,-.   #
#  |  |    | .-. :|      \'-.  .-'|  ||  ||  .--' \  '  / |  |   ,--.|      \|     /   #
#  '  '--'\\   --.|  ||  |  |  |  '  ''  '|  |     \   '  |  '--.|  ||  ||  ||  \  \   #
#   `-----' `----'`--''--'  `--'   `----' `--'   .-'  /   `-----'`--'`--''--'`--'`--'  # 
#                                                `---'                                 #
#                       ,-----.,--.    ,-----. ,--. ,--.,------.                       #
#                      '  .--./|  |   '  .-.  '|  | |  ||  .-.  \                      #
#                      |  |    |  |   |  | |  ||  | |  ||  |  \  :                     #
#                      '  '--'\|  '--.'  '-'  ''  '-'  '|  '--'  /                     #
#                       `-----'`-----' `-----'  `-----' `-------'                      #
                                                                                   

# This script will make a Public API call to the CenturyLink Cloud to publish a Script Package
# Usage Example: $ ./get_pending_packages.sh
# Output will simply list the package names on each line

# Declare variables
# Variable info found here: https://t3n.zendesk.com/entries/20428161-Get-Pending-Packages

API_KEY="REPLACE"
API_PWD="REPLACE"

# Authenticate and place encrypted cookie in current directory and bury the output
curl -s -X POST -H "Content-type: application/json" -c cookies.txt -X POST https://api.tier3.com/REST/Auth/Logon -d '
{
"APIKey":"'$API_KEY'",
"Password":"'$API_PWD'"
}
' -o /dev/null

# POST the input via CenturyLink Cloud API to publish a Script Package
curl -s -X POST -H "Content-type: application/json" -b cookies.txt -X POST https://api.tier3.com/REST/Blueprint/GetPendingPackages/ -d '
{
}
'| tr -d { | tr -d } | tr , '\n' | grep Name | tr -d \" | cut -f 2 -d :
