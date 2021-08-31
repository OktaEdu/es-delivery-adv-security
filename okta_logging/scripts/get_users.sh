#!/bin/bash
file="org.txt"
check=`readlink -f $file`
if [ ! -f "$check" ]
then
        echo "ERROR: $file not found. Are you in the right directory?"
        exit 1
fi
org=`cat org.txt`
api_key=`gpg -d api_key.txt.gpg`
curl -s --location --request GET "https://$org/api/v1/users?filter=status+eq+%22DEPROVISIONED%22+or+status+eq+%22ACTIVE%22" \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--header "Authorization: SSWS $api_key" > logs/tmp.users
cat logs/tmp.users | json_pp > logs/$org.users
num=`cat logs/$org.users | grep '"login"' | wc -l`
echo "Retreived $num users from $org"
rm -f logs/tmp.users
