from urllib2 import Request, urlopen, URLError
import requests, datetime, os
from datetime import datetime, timedelta
import json
import Myheader

req_prefix = 'https://api.lufthansa.com/v1/'
 
def getHeader():       
    file = './key.txt'
    headers = Myheader.header_token(file)
    return headers

def callRequest(myrequest, header):
    try:
        '''headers = {
            'Authorization': #str(access_token),
            'Bearer 7u4gey8behd39uprkfjqn3tp',
            'Accept': 'application/json',
            'Content-Type' : 'application/json'}'''
        req_data = ('https://api.lufthansa.com/v1/' + myrequest)

        #req_data = ('https://api.lufthansa.com/v1/references/airports/FRA')
        req_call = requests.get(req_data, headers = header) 
        #print req_call.status_code
    except URLError, e:
        print 'Error: ', e

    return req_call.json()

    
header = getHeader()

flightDate = '2016-04-10'
flightNumber = raw_input('Enter Flight: ')
print flightNumber
methods = 'operations/flightstatus/' + flightNumber + '/' + flightDate #LH400/2016-04-10'

lh_api = callRequest(methods, header) 
flightStatus = lh_api.get('FlightStatusResource', {}).get('Flights',{}).get('Flight',{}).get('Departure',{}).get('TimeStatus',{}).get('Definition')
print flightStatus



    