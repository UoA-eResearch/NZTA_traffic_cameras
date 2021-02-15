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

sql = f"SELECT camId,ANY_VALUE(datetime),ANY_VALUE(detections) FROM `detections` GROUP BY camId,DATE(datetime)"
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
