#!/usr/bin/env python3

import os
import random
import json
import mysql.connector
import config
import datetime

db = mysql.connector.connect(
  host="localhost",
  user=config.user,
  passwd=config.passwd,
  database="car"
)
cur = db.cursor()

random.seed(9001)

if os.path.isfile("dts_per_camID.json"):
    with open("dts_per_camID.json") as f:
        dts_per_camID = json.load(f)
else:
    cur.execute("SELECT camID, datetime FROM `detections`")
    camIDs_and_datetimes = cur.fetchall()
    dts_per_camID = {}
    for camID, dt in camIDs_and_datetimes:
        if camID not in dts_per_camID:
            dts_per_camID[camID] = {}
        date_str = str(dt.date())
        if date_str not in dts_per_camID[camID]:
            dts_per_camID[camID][date_str] = []
        dts_per_camID[camID][date_str].append(str(dt))

    with open("dts_per_camID.json", "w") as f:
        json.dump(dts_per_camID, f)

where = []
for camID in dts_per_camID:
    dts_for_camID = []
    for day, dts in dts_per_camID[camID].items():
        if len(dts) > 2:
            dts = random.sample(dts, 2)
        for dt in dts:
            where.append(f"({camID},'{str(dt)}')")

where = ",".join(where)
sql = f"SELECT camID,datetime,detections FROM detections WHERE (camID,datetime) IN ({where})"
cur.execute(sql)
detections = cur.fetchall()

results = {}

for row in detections:
    if row[0] not in results:
        results[row[0]] = {}
    data = json.loads(row[2])
    for d in data:
        d["percentage_probability"] = round(d["percentage_probability"], 2)
    date_str = row[1].strftime("%Y-%m-%d-%H%M%S")
    results[row[0]][date_str] = data

print(json.dumps(results))