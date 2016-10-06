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
    
        '''headers = {
            'Authorization': #str(access_token),
            'Bearer 7u4gey8behd39uprkfjqn3tp',
            'Accept': 'application/json',
            'Content-Type' : 'application/json'}'''
        req_data = ('https://api.lufthansa.com/v1/' + myrequest)

        req_call = requests.get(req_data, headers = header) 
        if req_call.status_code > 499:
            raise URLError('No data to process! :')
        else:
            return req_call.json()


try:   
    header = getHeader()
    flightDate = '2016-08-16'
    flightNumber = raw_input('Enter Flight: ')
    #print flightNumber
    methods = 'operations/flightstatus/' + flightNumber + '/' + flightDate #LH400/2016-04-10'
    
    lh_api = callRequest(methods, header) 
    #print lh_api
    flightStatus = lh_api.get('FlightStatusResource', {}).get('Flights',{}).get('Flight',{}).get('Departure',{}).get('TimeStatus',{}).get('Definition')
    originStatus = lh_api.get('FlightStatusResource', {}).get('Flights',{}).get('Flight',{}).get('Departure',{}).get('AirportCode',{}) 
    destinationStatus = lh_api.get('FlightStatusResource', {}).get('Flights',{}).get('Flight',{}).get('Arrival',{}).get('AirportCode',{}) 
    #print flightStatus ,"Origin", originStatus,"Destination", destinationStatus
    
    methods ='references/airports/'+ str(originStatus) + '?LHoperated=true'
    oCityCall = callRequest(methods, header) 
    origin =  oCityCall.get('AirportResource',{}).get('Airports',{}).get('Airport',{}).get('Names',{}).get('Name',{})[1].get('$',{})
    methods ='references/airports/'+ destinationStatus + '?LHoperated=true'
    dCityCall = callRequest(methods, header) 
    destination = dCityCall.get('AirportResource',{}).get('Airports',{}).get('Airport',{}).get('Names',{}).get('Name',{})[1].get('$',{})
    print flightStatus ,"Origin", origin,"Destination", destination
except URLError, e:
    print e
  
    

    