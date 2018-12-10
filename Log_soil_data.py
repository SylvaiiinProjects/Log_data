#!/usr/bin/env python




"""Save sensor value."""

import os
import sys
import json
from time import time
from functools import wraps
import requests

FARMWARE_NAME = 'Log Value'
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

def create_node(kind=None, args=None):
    """Create a kind, args Celery Script node."""
    node = {}
    node['kind'] = kind
    node['args'] = args
    return node


def read_pin(number=0, mode=0, label='---'):
    """Celery Script to read the value of a pin.
    Kind:
        read_pin
    Arguments:
        pin_number: 0
        pin_mode: 0 [0, 1]
        label: '---'
    """
    args = {}
    args['pin_number'] = number
    args['pin_mode'] = mode
    args['label'] = label
    _read_pin = create_node(kind='read_pin', args=args)
    return _read_pin



def get_pin_value(pin):
    """ Sequence `Read Pin` """
    response = requests.get(
        os.environ['FARMWARE_URL'] + 'api/v1/bot/state',
        headers=HEADERS)
    # bot/state endroit où sont stockées les données
    try:
        value = response.json()['pins'][str(pin)]['value']
    except KeyError:
        value = None
    if value is None:
        no_data()
        sys.exit(0)
    else:
        data(value)
        sys.exit(0)
    return value

def timestamp(value):
    """Add a timestamp to the pin value."""
    return {'time': time(), 'value': value}

def _print_json(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        """Send Celery Script or return the JSON string.
        Celery Script is sent by sending an HTTP POST request to /celery_script
        using the url in the `FARMWARE_URL` environment variable.
        """
        try:
            os.environ['FARMWARE_URL']
        except KeyError:
            # Not running as a Farmware: return JSON
            return function(*args, **kwargs)
        else:
            # Running as a Farmware: send Celery Script command
            farmware_token = os.environ['FARMWARE_TOKEN']
            headers = {'Authorization': 'bearer {}'.format(farmware_token),
                       'content-type': "application/json"}
            payload = json.dumps(function(*args, **kwargs))
            ret = requests.post(farmware_api_url() + 'celery_script',
                          data=payload, headers=headers)
            return ret
    return wrapper

def post(wrapped_data):
    """Send the Celery Script command."""
    payload = json.dumps(wrapped_data)
    requests.post(os.environ['FARMWARE_URL'] + 'api/v1/celery_script',
                  data=payload, headers=HEADERS)

if __name__ == '__main__':
    PIN = get_env('pin')    
    #PIN = get_input_env()
    #data(post(read_pin(number=64,mode=0, label='Value is ')))
    #pour afficher directement la valeur obtenue
    _print_json(read_pin(number=64,mode=0, label='Value is '))
    get_pin_value(PIN)
    



