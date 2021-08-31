#!/c/Python39/python
##!/c/Users/Administrator/AppData/Local/Programs/Python/Python39/python
##!/usr/bin/python3
import time, os, configparser, shutil, json, re, sys
path=sys.argv[0].replace("/alerts.py","")
sys.path.append(path)
from shutil import copyfile
import alert
try:
    file = open('org.txt','r')
except Exception as e:
    print("ERROR: org.txt not found. Are you in the right directory?")
    quit()
orglist = file.readlines()
org = orglist[0].rstrip()
alerts = alert.load_alerts(org)
logfilename = "logs/" + org + ".json"
logfile = open(logfilename,'rb')
events = json.load(logfile)
for event in events:
    try:
        alertline = alerts[event["eventType"]]
        alertlinea = alertline.split(" ")
        objectsearch = alertlinea[0]
        message = alertlinea[1]
        displayattrs = alertlinea[2].split(",")
        searcha = objectsearch.split(",")
        jpath = searcha[0]
        regex = searcha[1].rstrip()
        objects = jpath.split(":")
        check = 're.search("' + regex + '", ' + 'event'
        for object in objects:
            if object.isnumeric():
                check = check + '[' + object + ']'
            else:
                check = check + '["' + object + '"]'
        check = check + ", re.IGNORECASE)"
        try:
            z = eval(check)
            if z:
                attrs = ""
                for displayattr in displayattrs:
                    objects = displayattr.split(":")
                    attr = 'event'
                    for object in objects:
                        if object.isnumeric():
                            attr = attr + '[' + object + ']'
                        else:
                            attr = attr + '["' + object + '"]'
                    a = eval(attr)
                    attrs = attrs + " " + displayattr + " " + a
                check = ""
                try:
                    checkparms = alertlinea[3].split(",")
                    if checkparms[0] == "CHECK_USER":
                        check = alert.check_user(org,event,checkparms[1])
                except Exception as e:
                    print(e)
                    noop = "noop"
                print(message + " " + attrs + check)
        except Exception as e:
            noop = "noop"
    except Exception as e:
        noop = "noop"
