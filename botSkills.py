import requests
import json
import routers
# Router Info 
device_address = routers.router1['host']
device_address2 = routers.router2['host']
device_username = routers.router2['username']
device_password = routers.router2['password']

    # RESTCONF Setup
port = '443'
url_base = "https://{h}/restconf".format(h=device_address)
headers = {'Content-Type': 'application/yang-data+json',
        'Accept': 'application/yang-data+json'}

def get_status(router):
    


    if router == "R1":
        url = "https://{h}/restconf".format(h=device_address) + "/data/Cisco-IOS-XE-nat-oper:nat-data"
        response = requests.get(url,
                                auth=(device_username, device_password),
                                headers=headers,
                                verify=False
                                )

    # return the json as text
        return response.json()["Cisco-IOS-XE-nat-oper:nat-data"]

    if router == "R2":
        url = "https://{h}/restconf".format(h=device_address2) + "/data/Cisco-IOS-XE-nat-oper:nat-data"
        response = requests.get(url,
                              auth=(device_username, device_password),
                              headers=headers,
                              verify=False
                              )
  # return the json as text
        return response.json()["Cisco-IOS-XE-nat-oper:nat-data"]
data = get_status("R1")

#print(type(data['ip-nat-statistics']['initialized'],data['ip-nat-statistics']['hits'],data['ip-nat-statistics']['misses']))
