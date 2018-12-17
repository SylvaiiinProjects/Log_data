#!/usr/bin/env python

"""Save sensor value."""

import os
import sys
import json
from time import time
import requests

FARMWARE_NAME = 'log_value'
#FARMWARE_NAME = farmware.replace(' ', '_').replace('-', '_').lower()

HEADERS = {
    'Authorization': 'bearer {}'.format(os.environ['FARMWARE_TOKEN']),
    'content-type': 'application/json'}

"""def get_input_env():
    prefix = FARMWARE_NAME        
    input_title = os.environ.get(prefix+"_pin")
    return input_title"""

""" 64 is always taken """

def get_env(key, type_=int):
	""" key = Farmware input name"""
    
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
    """ Sequence `Read Pin`et séquence position du bras suivant x """
    response = requests.get(
        os.environ['FARMWARE_URL'] + 'api/v1/bot/state',
        headers=HEADERS)
    try:
        #value0 = json.loads(os.getenv('pin_data_' + str(pin), '[]'))
	#value0 = response.json()['pins'][str(pin)]['value']
        value0 = response.json()['location_data']['position']['x']
    except KeyError:
        value0 = None
    if value0 is None:
        no_data()
        sys.exit(0)
    else:
        data(value0)
        sys.exit(0)
    #return value


def post(wrapped_data):
    """Send the Celery Script command."""
    payload = json.dumps(wrapped_data)
    requests.post(os.environ['FARMWARE_URL'] + 'api/v1/celery_script',     data=payload, headers=HEADERS)

if __name__ == '__main__':
    PIN = get_env('PIN') 
    #data(get_env('PIN'))   
    #PIN = get_input_env()
    get_pin_value(PIN)
    
