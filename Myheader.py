from urllib2 import Request, urlopen, URLError
import requests, datetime, os
from datetime import datetime, timedelta
import json



client_id = ('m5gdx2czz986mj3agrdrcq8a')
client_secret = ('zRwRSKgGkk')


def header_token (file):
    now = datetime.now()
    old = now 
    try:
        f = open(file,'r')
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)     
    tmp = f.read()
    f.close()
    if tmp:
        strtime = tmp.split(';')[0]
        time = datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=+24)
        access_token = tmp.split(';')[1]
        if time < now or len(access_token) <= 20: #Token is invalid because older than 24h
            print ('get new header')
            access_token =  getNewToken()
            f = open(file,'w')
            stream = str(now) + ';' + str(access_token)
            f.write(stream)
            f.close() 
            header_call = getHeader(access_token)
            return header_call
        else:
            header_call = getHeader(access_token)
            return header_call 
    else:
        print 'get initial Header'
        access_token =  getNewToken()
        f = open(file,'w')
        stream = str(now) + ';' + str(access_token)
        f.write(stream)
        f.close()
        header_call = getHeader(access_token)
        return header_call 
    return 'Error in Authentication'

def getNewToken():
    request = ('https://api.lufthansa.com/v1/oauth/token')
    header_auth = {
        'client_id' : client_id,
        'client_secret': client_secret, 
        'grant_type' : 'client_credentials'}
#    try:            
    r = requests.post(request, data = header_auth)
    j =  r.json() 
#        access_token = { 'Authorization': 'Bearer ' + j['access_token']}
        
    if r.status_code > 299:
        raise URLError('No access token retrieved! :')
    else:
        token = j['access_token']
        return token
#    except URLError, e:
#        print 'Error: ', e
 #   else:
         
    
def getHeader(access_token):
    header_call = {
            'Authorization': 'Bearer ' + str(access_token),
        'Accept': 'application/json'}
    return header_call