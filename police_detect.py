#!/usr/bin/env python3

import json
import datetime
import requests
import time
import ast
from datetime import datetime

print("[*] AUCKLAND POLICE FEED v1.1a by ezy\n")

def get_location_mapbox(lats,longs):
    r = requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{longs},{lats}.json?access_token=pk.eyJ1IjoibGljZW5zaW5nYXQiLCJhIjoiY2wyZm50NzZqMGNmaTNqbzV6c2hlbTBrcCJ9.LNu9kX6HGQ6WPVk8zoDELQ')
    if r.status_code == 200:
        data = r.json()
        address = data["features"][0]["place_name"]
        return address
    else:
        print("Error:", r.status_code)

def send_data(message):
    webhook_url = 'https://forum/chat/hooks/236a03961f65260705852c07.json'
    payload = {
        'text': '{}'.format(message),
        'username' : 'alert'
    }
    try:
        requests.post(webhook_url, data=payload)
    except:
        pass

def get_time():
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    return(current_time)

def get_police_coordinates_from_waze():
    headers = {
        "referer": "https://www.waze.com/livemap",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    }

    r = requests.get("https://www.waze.com/row-rtserver/web/TGeoRSS?bottom=-37.67228792679098&left=173.94859313964847&ma=800&mj=200&mu=20&right=175.53886413574222&top=-36.453295713273015&types=alerts%2Ctraffic%2Cusers", headers=headers)
    r.raise_for_status()
    alerts = r.json().get('alerts', [])
    alerts = filter(lambda x: x['type'] == 'POLICE', alerts)
    locations = map(lambda x: dict(lat=x['location']['y'], long=x['location']['x']), alerts)
    # locations = map(lambda x: dict(lat=x['location']['y'], long=x['location']['x'], street=x['street'],score=x['reliability']), alerts)
    locations = list(locations)
    ret = []
    for location in locations:
        ret.append(get_location_mapbox(location['lat'],location['long']))
    return ret

filename = "police_coordinates.log"
last_content = ""

while True:
    content = json.dumps(get_police_coordinates_from_waze())
    with open(filename, "w") as f:
        f.write('{}\n'.format(content))
    with open(filename, "r") as f:
        content = f.read()
    if content != last_content:
        added_content = content.replace(last_content, "")
        try:
            new_array = ast.literal_eval(added_content)
            old_array = ast.literal_eval(last_content)
            old_set = set(old_array)
            new_set = set(new_array)

            added = new_set - old_set
            removed = old_set - new_set

            for item in added:
                # send_data("[x] POLICE DETECTED! [x]: \n{}".format(item))
                print("\n[{}] POLICE DETECTED! : \n{}".format(get_time(),item))

            for item in removed:
                # send_data("[-] Removed Detection [-]: \n{}".format(item))
                print("[-] Removed Detection [-]: \n{}".format(item))
        except:
            pass
        last_content = content
    time.sleep(10)