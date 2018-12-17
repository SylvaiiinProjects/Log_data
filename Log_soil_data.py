#!/usr/bin/env python



import os
import sys
import json
from time import time
import requests

FARMWARE_NAME = 'log_value'
HEADERS = {
    'Authorization': 'bearer {}'.format(os.environ['FARMWARE_TOKEN']),
    'content-type': 'application/json'}

def get_env(key, type_=int):
    """Return the value of the namespaced Farmware input variable."""
    return type_(os.getenv('{}_{}'.format(FARMWARE_NAME, key), 64))

def no_data_error():
    
    message = '[soil] Pin {} value not available.'.format(PIN)
    wrapped_message = {
        'kind': 'send_message',
        'args': {
            'message_type': 'error',
            'message': message}}
    post(wrapped_message)

def get_pin_value(pin):
    
    response = requests.get(
        os.environ['FARMWARE_URL'] + 'api/v1/bot/state',
        headers=HEADERS)
    try:
        value = response.json()['pins'][str(pin)]['value']
    except KeyError:
        value = None
    if value is None:
        no_data_error()
        sys.exit(0)
    return value

"""

def wrap(data):
   
    return {
        'kind': 'set_user_env',
        'args': {},
        'body': [{
            'kind': 'pair',
            'args': {
                'label': LOCAL_STORE,
                'value': json.dumps(data)
            }}]}"""

def post(wrapped_data):
    
    payload = json.dumps(wrapped_data)
    requests.post(os.environ['FARMWARE_URL'] + 'api/v1/celery_script',
                  data=payload, headers=HEADERS)

if __name__ == '__main__':
    PIN = get_env('pin')
    #LOCAL_STORE = 'pin_data_' + str(PIN)
    post(get_pin_value(PIN))
