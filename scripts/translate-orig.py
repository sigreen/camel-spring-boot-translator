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
  response = towerSession.post(url, data=extra_vars, verify=False)

    # let's wait until the job is done 
  jobId = response.json()['id']
  env = response.headers['x-machine']
  retries = 0

  # give the job 8 seconds to complete
  while retries < 8:
    job = f'http://automation.kong-sales-engineering.com/api/v2/jobs/{jobId}/'
    response = towerSession.get(job, verify=False)
    jobDone = response.json()['status'] == 'successful'
    elapsed = response.json()['elapsed']
    retries += 1
    time.sleep(0.5)

  job = f'http://automation.kong-sales-engineering.com/api/v2/jobs/{jobId}/stdout/?format=txt'
  response = towerSession.get(job, verify=False)

  # strip the junk from up front all the way to PLAY RECAP
  # (I am sure there is a better way to do this)
  begin = response.text.find("response.stdout")
  end = response.text.find("PLAY RECAP")
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

url = f'http://automation.kong-sales-engineering.com/api/v2/job_templates/11/launch/'
print('Using ' + url + ' to translate request...')
print('Here we go!\n')

# grab random quote so we can translate it
quoteSession = requests.Session()
quoteSession.headers.update({'content-type': 'application/json'})

# this is for Ansible Tower
towerSession = requests.Session()
towerSession.headers.update({'Authorization': 'Bearer vJN3QjZEyJiun3Ks5DEEGGmabJloEk'})
#towerSession.headers.update({'Authorization': ''})
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
    quote = None
    retries = 0
  except Exception:
    time.sleep(0.5)
    pass

if retries==3:
  print('Could not connect to Tower upstream services')