#!/usr/bin/env python

"""Log soil sensor data."""

import os
import sys
import json
import requests
import numpy as np


FARMWARE_NAME = 'log_sensor_data'


def get_env(key, type_=int):
    'Return the value of the namespaced Farmware input variable.'
    return type_(os.getenv('{}_{}'.format(FARMWARE_NAME, key), 64))

def post(wrapped_data):
    """Send the Celery Script command."""
    headers = {
        'Authorization': 'bearer {}'.format(os.environ['FARMWARE_TOKEN']),
        'content-type': 'application/json'}
    payload = json.dumps(wrapped_data)
    requests.post(os.environ['FARMWARE_URL'] + 'api/v1/celery_script',
                  data=payload, headers=headers)

def no_data_error():
    """Send an error to the log if there's no data."""
    message = '[Log sensor data] No data available for pin {}.'.format(PIN)
    wrapped_message = {
        'kind': 'send_message',
        'args': {
            'message_type': 'error',
            'message': message}}
    post(wrapped_message)

def get_pin_data(pin):
    """Get existing historical pin data."""
    data = json.loads(os.getenv('pin_data_' + str(pin), '[]'))
    if len(data) < 1:
        no_data_error()
        sys.exit(0)
    else:
        return data

def log_data():
    """Send data."""
    message = '[Log sensor data]  data available for pin {} is {}.'.format(PIN,d)
    wrapped_message = {
        'kind': 'send_message',
        'args': {
            'message_type': 'log',
            'message': message}}
    post(wrapped_message)




if __name__ == '__main__':
    PIN = get_env('pin')
    d= get_pin_data(PIN)
    log_data()