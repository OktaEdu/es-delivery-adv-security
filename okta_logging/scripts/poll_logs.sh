#!/bin/bash
file="org.txt"
check=`readlink -f $file`
if [ ! -f "$check" ]
then
        echo "ERROR: $file not found. Are you in the right directory?"
        exit 1
fi
touch no_orgs.tmp
org=`cat org.txt`
if [ "$org" == "" ]
then
	echo "No Org found in org.txt"
	exit 1
fi
api_key=`gpg -d api_key.txt.gpg`
total=0
while true
do
	if [ -e logs/$org.next ]
	then
		url=`cat logs/$org.next`
	else
		url="https://$org/api/v1/logs?sortOrder=ASCENDING"
		echo "[" > logs/$org.log
	fi
	curl -s --location -D logs/$org.headers --request GET "$url" \
	--header 'Accept: application/json' \
	--header 'Content-Type: application/json' \
	--header "Authorization: SSWS $api_key" > logs/tmp
	grep "Invalid token provided" logs/tmp > /dev/null
	if [ $? -eq 0 ]
	then
		echo "$org INVALID API TOKEN"
		rm -f logs/$org.headers
		rm -f logs/tmp
		exit 1
	fi
       	cat logs/tmp | json_pp | head -n -1 | tail -n +2 > logs/tmp2
	if [ ! -s logs/tmp2 ]
	then
		rm -f logs/$org.headers
		echo "Finished retreiving $total system log events"
		cat logs/$org.log | head -n -1 > logs/$org.json
		echo "]" >> logs/$org.json
		break
	else
		num=`cat logs/tmp2 | grep eventType | wc -l`
		total=`expr $total + $num`
		echo "Appending $num events to $org.log"
		rm -f no_orgs.tmp
		cat logs/tmp2 >> logs/$org.log
		echo "," >> logs/$org.log
		cat logs/$org.headers | grep link: | tail -1 | cut -d '<' -f 2 | cut -d '>' -f 1 > logs/$org.next
		rm -f logs/$org.headers
	fi
	sleep 5
done
rm -f logs/tmp
rm -f logs/tmp2
