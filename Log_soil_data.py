#!/usr/bin/env python

import os
import requests
import json

headers = {
  'Authorization': 'bearer {}'.format(os.environ['FARMWARE_TOKEN']),
  'content-type': "application/json"}

FARMWARE_NAME = 'log_value'
HEADERS = {
    'Authorization': 'bearer {}'.format(os.environ['FARMWARE_TOKEN']),
'content-type': 'application/json'}


response = requests.get(os.environ['FARMWARE_URL'] + 'api/v1/bot/state',
              headers=headers)


def no_data(PIN,value):
    
    message = '[soil] Pin {} is {} .'.format(PIN,value)
    wrapped_message = {
        'kind': 'send_message',
        'args': {
            'message_type': 'info',
            'message': message}}
    post(wrapped_message)

def post(wrapped_data):
    
    payload = json.dumps(wrapped_data)
    requests.post(os.environ['FARMWARE_URL'] + 'api/v1/celery_script',
   data=payload, headers=HEADERS)


bot_state = response.json()
position_x = bot_state['location_data']['position']['x']
value = bot_state['pins']['64']['value']
PIN = 64

no_data(PIN,value)


