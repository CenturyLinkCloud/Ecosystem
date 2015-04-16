#! /bin/bash
set -e

# Take parameters from command line
USERNAME="$1"   # Username of the control portal user to connect to API as
PASSWORD="$2"   # Password for this user
ACCOUNT="$3"    # The account alias to query in the API (Example: TSTB)
SERVERID="$4"   # The server ID to query in the API (Example: CA2TSTBRR01)

apt-get -y update
apt-get -y install jq

# Names of value keys to get from JSON responses
TOKENKEY="bearerToken"

# Build JSON for authorization request
AUTHJSON="{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}"

# Store URLs for API requests
BASEURL="https://api.tier3.com/v2"
AUTHURL="$BASEURL/authentication/login"
GETSRVURL="$BASEURL/servers/$ACCOUNT/$SERVERID"

# Simple helper function to parse JSON response ($1) and return value for given key ($2)
jsonGetVal() {
    echo $1 | sed 's/[{}]//g' | awk -v k="text" '{n=split($0,a,","); for (i=1; i<=n; i++) print a[i]}' |
       sed 's/\"//g' | grep $2 | awk 'BEGIN { FS = ":" } ; {print $2}'
}

# Call to authentication API to get token
AUTHRESP=`curl -s -H "Content-Type: application/json" -d $AUTHJSON $AUTHURL`
TOKEN=`jsonGetVal $AUTHRESP $TOKENKEY`

# Call to server API to get data center id for given server id
SRVRESP=`curl -s -H "Authorization: Bearer $TOKEN" $GETSRVURL`

# Write information to given file name
echo -e "$SRVRESP" | jq -r '.details.ipAddresses[1].public' > /tmp/publicip
