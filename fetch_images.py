#!/usr/bin/env python3

import os
import json
import pprint
import requests
from dateutil.parser import parse as parsedate

with open("cameras.json") as f:
    cameras = json.load(f)
with open("unavailable.jpg", "rb") as f:
    unavailable = f.read()

camIds = sorted([int(c["properties"]["id"]) for c in cameras["features"]])
while True: # It takes about 30 seconds to download all 286 images, by which time it's time to do it again
    for camId in camIds:
        path = f"images/{camId}/"
        os.makedirs(path, exist_ok=True)
        imageUrl = f"https://www.trafficnz.info/camera/{camId}.jpg"
        try:
            r = requests.get(imageUrl, timeout=5)
            if r.content == unavailable:
                print(camId, "unavailable")
                continue
            lastModified = r.headers["Last-Modified"]
            lastModified = parsedate(lastModified).strftime("%Y-%m-%d-%H%M%S")
            print(camId, lastModified)
            with open(path + lastModified + ".jpg", "wb") as f:
                f.write(r.content)
        except Exception as e:
            print(camId, e)