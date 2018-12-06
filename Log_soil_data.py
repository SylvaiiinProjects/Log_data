#!/usr/bin/env python

"""Log soil sensor value."""

import os
import sys
import json
import requests
import numpy as np


FARMWARE_NAME = Log_Value'
HEADERS = {    'Authorization': 'bearer {}'.format(os.environ['FARMWARE_TOKEN']),    'content-type': 'application/json'}


def get_env(key, type_=int):
    'Return the value of the namespaced Farmware input variable.'
    return type_(os.getenv('{}_{}'.format(FARMWARE_NAME, key), 64))

def post(wrapped_data):
    """Send the Celery Script command."""   
    payload = json.dumps(wrapped_data)
    requests.post(os.environ['FARMWARE_URL'] + 'api/v1/celery_script',
                  data=payload, headers= HEADERS)

def no_data_error():
    """Send an error to the log if there's no data."""
    message = '[Log sensor data] No data available for pin {}.'.format(PIN)
    wrapped_message = {
        'kind': 'send_message',
        'args': {
            'message_type': 'error',
            'message': message}}
    post(wrapped_message)

def log_value():

    message = '[Log sensor value] Value for pin {} is {}.'.format(PIN,value)
    wrapped_message = {
        'kind': 'send_message',
        'args': {
            'message_type': 'error',
            'message': message}}
    post(wrapped_message)
   

def get_pin_value(pin): 
   """Get the value read by a Sequence `Read Pin` step or the Sensor widget."""
  
  response = requests.get(  os.environ['FARMWARE_URL'] + 'api/v1/bot/state',   headers=HEADERS)
    try:       
	 value = response.json()['pins'][str(pin)]['value']
			
    except KeyError:   
   		  value = None
		  
     if value is None:   
  	   no_data_error() 
  	   sys.exit(0)
	 
     else:
	   log_value()
	   sys.exit(0) 
	 	
   



if __name__ == '__main__':
    PIN = get_env('pin')
    post(get_pin_value(PIN))
    
