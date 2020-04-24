#!/usr/bin/env python3

import os
from tqdm.auto import tqdm
import mysql.connector
import config
from datetime import datetime

db = mysql.connector.connect(
  host="localhost",
  user=config.user,
  passwd=config.passwd,
  database="car"
)
cur = db.cursor()

print(db)

camIds = os.listdir("annotations")

for camId in tqdm(camIds):
    annotations = os.listdir(f"annotations/{camId}/")
    for annotation_path in tqdm(annotations):
        with open(f"annotations/{camId}/{annotation_path}") as f:
            a = f.read()
        sql = "INSERT IGNORE INTO detections (camID, datetime, detections) VALUES (%s, %s, %s)"
        dt = datetime.strptime(annotation_path, "%Y-%m-%d-%H%M%S.jpg.json")
        val = (camId, dt, a)
        cur.execute(sql, val)
        db.commit()
