#!/usr/bin/env python

"""Save sensor value."""

import os
import sys
import json
from time import time
import requests

FARMWARE_NAME = 'Log_Value'
HEADERS = {
    'Authorization': 'bearer {}'.format(os.environ['FARMWARE_TOKEN']),
    'content-type': 'application/json'}

"""def get_input_env():
    prefix = FARMWARE_NAME        
    input_title = os.environ.get(prefix+"_pin")
    return input_title"""


""" 64 is always taken """
def get_env(key, type_=int):
    
    return type_(os.getenv('{}_{}'.format(FARMWARE_NAME, key),64))

def no_data():
    
    message = '[Soil sensor Value] Pin {} value is not available.'.format(PIN)
    wrapped_message = {
        'kind': 'send_message',
        'args': {
            'message_type': 'error',
            'message': message}}
    post(wrapped_message)

def data(value):
    
    message = '[Soil sensor Value] Pin {} value  is {}.'.format(PIN,value)
    wrapped_message = {
        'kind': 'send_message',
        'args': {
            'message_type': 'info',
            'message': message}}
    post(wrapped_message)

def get_pin_value(pin):
    """ Sequence `Read Pin` """
    response = requests.get(
        os.environ['FARMWARE_URL'] + 'api/v1/bot/state',
        headers=HEADERS)
    try:
        value = response.json()['pins'][str(pin)]['value']
        value1 = response.json()['location_data']['position']['x'
    except KeyError:
        value1 = None
    if value is None:
        no_data()
        sys.exit(0)
    else:
        data(value1)
        sys.exit(0)
    return value1

def timestamp(value):
    """Add a timestamp to the pin value."""
    return {'time': time(), 'value': value}



def post(wrapped_data):
    """Send the Celery Script command."""
    payload = json.dumps(wrapped_data)
    requests.post(os.environ['FARMWARE_URL'] + 'api/v1/celery_script',
                  data=payload, headers=HEADERS)

if __name__ == '__main__':
    PIN = get_env('pin')    
    #PIN = get_input_env()
    get_pin_value(PIN)
    
