from pyzabbix import ZabbixAPI
import json
from settings import config

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
print("%s/data.json" % dir_path)
print(config.get('Zabbix','api_url'))

zapi = ZabbixAPI(config.get('Zabbix','api_url'))
zapi.login(config.get('Zabbix','api_username'),config.get('Zabbix','api_password'))

hosts = zapi.host.get(withInventory=True,selectInventory=['location_lon','location_lat'],output="extend",filter={"status":0})
to_json_blob = []
hosts_to_filter = []

print(hosts)
for host in hosts:
    if host["inventory"]["location_lon"] and host["inventory"]["location_lat"]:
        hosts_to_filter.append(host["hostid"])
        to_json_blob.append(
            {"key":host["hostid"],
            "latitude":host["inventory"]["location_lat"],
            "longitude":host["inventory"]["location_lon"],
            "name":host["host"]})

items = zapi.item.get(output="extend",filter={'key_':'net.wan.status'},hostids=hosts_to_filter)
items += zapi.item.get(output="extend",filter={'key_':'icmpping'},hostids=hosts_to_filter)
items += zapi.item.get(output="extend",filter={'key_':'icmpping[,,,,]'},hostids=hosts_to_filter)

# with open("%s%s" % (config.get('App','file_write_path'), 'locations.json'),'w') as f:
with open("%s/locations.json" % dir_path ,'w') as f:
    json.dump(to_json_blob,f)

to_json_blob = []
consumed_host_ids = set()
for item in items:
    if item['hostid'] in consumed_host_ids:
        continue
    to_json_blob.append(
        {
            "target":item["hostid"],
            "datapoints":[[int(item["lastvalue"]),int(item["lastclock"])]]
        }
    )
    consumed_host_ids.add(item['hostid'])

# with open("%s%s" % (config.get('App','file_write_path'), 'data.json'),'w') as f:
with open("%s/data.json" % dir_path,'w') as f:
    print(to_json_blob)
    json.dump(to_json_blob,f)
