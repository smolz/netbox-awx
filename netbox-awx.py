#!/usr/bin/env python

import json
import requests

# Netbox URL
URL = ''

# Netbox API Token
TOKEN = ''

headers = {
    'Accept': 'application/json ; indent=4',
    'Authorization': 'Token %s' % (TOKEN),
}

api_url = URL + '/api/dcim/devices/'
hosts_list = []
devices = []
sites = {}
racks = {}
platforms = {}
tenants = {}
tags = {}
inventory = {}
hostvars = {}

# Get data from netbox

while api_url:
    api_output = requests.get(api_url, headers=headers)
    api_output_data = api_output.json()

    if isinstance(api_output_data, dict) and "results" in api_output_data:
        hosts_list += api_output_data["results"]
        api_url = api_output_data["next"]

# Populate inventory

for i in devices:
    sites.setdefault(i['site']['slug'], {'hosts': []})['hosts'].append(i['name'])
    racks.setdefault(i['rack']['name'], {'hosts': []})['hosts'].append(i['name'])
    platforms.setdefault(i['platform']['slug'], {'hosts': []})['hosts'].append(i['name'])
    tenants.setdefault(i['tenant']['slug'], {'hosts': []})['hosts'].append(i['name'])
    for t in i['tags']:
        tags.setdefault(t, {'hosts': []})['hosts'].append(i['name'])
    if i['config_context']:
        hostvars.setdefault('_meta', {'hostvars': {}})['hostvars'][i['name']] = i['config_context']

inventory.update(sites)
inventory.update(racks)
inventory.update(platforms)
inventory.update(tenants)
inventory.update(tags)
inventory.update(hostvars)

print(json.dumps(inventory, indent=4))