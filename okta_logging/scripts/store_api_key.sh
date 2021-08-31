#!/bin/bash
echo "Paste the API key here"
read api_key
echo $api_key > api_key.txt
gpg -c api_key.txt
if [ -f api_key.txt.gpg ]
then
	rm api_key.txt
	echo "API key stored as api_key.txt.gpg"
else
	echo "Error: API key not encrypted"
	rm api_key.txt
fi
