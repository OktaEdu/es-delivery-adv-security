import json, re
def load_alerts(org):
    alertsfilename = "alerts.txt"
    alertsfile = open(alertsfilename,'r')
    alertslist = alertsfile.readlines()
    alerts = {}
    for aline in alertslist:
        alerta = aline.split(" ")
        alerts[alerta[0]] = alerta[1] + " " + alerta[2] + " " + alerta[3].rstrip()
        try:
            alerts[alerta[0]] = alerts[alerta[0]] + " " + alerta[4].rstrip()
        except:
            noop = "noop"
    return(alerts)

def load_users(org):
    users= {}
    usersfilename = "logs/" + org + ".users"
    usersfile = open(usersfilename,'r')
    userobjs =  json.load(usersfile)
    for userobj in userobjs:
        login = userobj["profile"]["login"]
        users[login] = userobj
        if re.search("@",login):
            shortlogina = login.split("@")
            users[shortlogina[0]] = userobj
    return(users)

def check_user(org,event,checkparms):
    users = load_users(org)
    objects = checkparms.split(":")
    attr = 'event'
    for object in objects:
        if object.isnumeric():
            attr = attr + '[' + object + ']'
        else:
            attr = attr + '["' + object + '"]'
    a = eval(attr)
    if a in users:
        check = ""
    else:
        check = " UNKNOWN USER"
    return(check)
