#!/usr/bin/env python3

import requests
import argparse
import json
import time
import signal
import sys

def signal_handler(sig, frame):
  towerSession.close()
  quoteSession.close()
  sys.exit(0) 

signal.signal(signal.SIGINT, signal_handler)

def translate(message):
  message = json.JSONEncoder().encode({'message': f'{quote}'})
  extra_vars = json.JSONEncoder().encode({'extra_vars': f'{message}'})
  
  env = "k8s"
  retries = 0
  elapsed = '0.0'


  response = towerSession.put(url, data=extra_vars, verify=False)
  elapsed = response.headers['X-Kong-Upstream-Latency']

  begin = response.text.find("response.stdout")
  end = response.text.find("}")
  pigLatin = response.text[begin:end]

  # now strip the semicolon and trailing space
  begin = pigLatin.find(": ")+3
  end = pigLatin.find("}")
  pigLatin = pigLatin[begin:end]

  # finally, strip the last double quote
  begin = 0
  end = pigLatin.find('\"')
  pigLatin = pigLatin[begin:end]

  print(f'{pigLatin}')
  print(f'Time to translate from {env}: {elapsed}\n\n')


# no pesky SSL warnings, please
requests.packages.urllib3.disable_warnings() 

url = f'http://automation.kong-sales-engineering.com/camel/translate'
print('Using ' + url + ' to translate request...')
print('Here we go!\n')

# grab random quote so we can translate it
quoteSession = requests.Session()
quoteSession.headers.update({'content-type': 'application/json'})

# this is for Ansible Tower
towerSession = requests.Session()
towerSession.headers.update({'content-type': 'application/json'})

quote = None
retries = 0

# give it 3 seconds to failover
while retries < 3:
  if quote == None:
    response = quoteSession.get('https://zenquotes.io/api/random/')
    jsonResponse = json.JSONDecoder().decode(response.text)[0]
    quote = jsonResponse['q']
    author = jsonResponse['a']
    print(f'{quote} --{author}')
  else:
    retries += 1

  try:
    translate(quote)
    time.sleep(5.0)
    quote = None
    retries = 0
  except Exception:
    time.sleep(0.5)
    pass

if retries==3:
  print('Could not connect to k8s upstream services')