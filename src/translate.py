import argparse
import os
import uuid

import requests

parcer = argparse.ArgumentParser(description='Translate with MS Azure')
parcer.add_argument('data', type=str, nargs='+', help='Text to translate (you can specify more than one word) ')
parcer.add_argument('--fl', type=str, default='ru', help='From Language')
parcer.add_argument('--tl', type=str, default='en', help='To Language')
args = parcer.parse_args()
print(args)
key_var_name = 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY'
if key_var_name in os.environ:
    subscription_key = os.environ[key_var_name]
else:
    raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
print(subscription_key)
endpoint_var_name = 'TRANSLATOR_TEXT_ENDPOINT'
if endpoint_var_name in os.environ:
    endpoint = os.environ[endpoint_var_name]
else:
    endpoint = 'https://api.cognitive.microsofttranslator.com/'

path = '/translate?api-version=3.0'
params = f'&from={args.fl}&to={args.tl}'
constructed_url = endpoint + path + params

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': 'eastasia',
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4()),
}
body = []
for item in args.data:
    item_string = {'text': item}
    body.append(item_string)
request = requests.post(constructed_url, headers=headers, json=body)
response = request.json()
for item in response:
    translate = item['translations']
    mess = translate[0]['text']
    print(type(mess), mess)
