#!/usr/bin/env python3

import json
import os
from tqdm.auto import tqdm
import mysql.connector
import config

with open("cameras.json") as f:
    cameras = json.load(f)

db = mysql.connector.connect(
  host="localhost",
  user=config.user,
  passwd=config.passwd,
  database="car"
)
cur = db.cursor()

sql = "SELECT camId,DATE(datetime),COUNT(*),SUM(JSON_LENGTH(detections)) FROM `detections` GROUP BY camID,DATE(datetime)"

cur.execute(sql)
results = cur.fetchall()

for result in results:
    print(result)
    for i,c in enumerate(cameras["features"]):
        camId = c["properties"]["id"]
        if int(camId) == result[0]:
            if "detections" not in cameras["features"][i]:
                cameras["features"][i]["detections"] = {}
            cameras["features"][i]["detections"][str(result[1])] = {
                "n_images": int(result[2]),
                "vehicles": int(result[3])
            }

with open("cameras_with_detections.json", "w") as f:
    json.dump(cameras, f, indent=2, sort_keys=True)
