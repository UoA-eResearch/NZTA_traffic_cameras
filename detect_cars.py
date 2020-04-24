#!/usr/bin/env python3

import balance_gpu

from imageai.Detection import ObjectDetection
import os
import json
import sys
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

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath("./models/resnet50_coco_best_v2.0.1.h5")
detector.loadModel()
print("Detector ready")
custom_objects = detector.CustomObjects(car=True, motorcycle=True, bus=True, truck=True)

if len(sys.argv) > 1:
    camIds = sys.argv[1:]
else:
    camIds = os.listdir("images")
print(camIds)


for camId in tqdm(camIds):
    os.makedirs(f"annotations/{camId}", exist_ok = True)
    images = os.listdir(f"images/{camId}/")
    sql = f"SELECT datetime FROM detections WHERE camID={camId}"
    cur.execute(sql)
    already_processed_images = cur.fetchall()
    images_to_process = [image for image in images if datetime.strptime(image, "%Y-%m-%d-%H%M%S.jpg") not in already_processed_images]
    for image in tqdm(images_to_process):
        if not image.endswith(".jpg"):
            continue
        image_path = f"images/{camId}/{image}"
        try:
            detected_image_array, detections = detector.detectCustomObjectsFromImage(output_type="array", custom_objects=custom_objects, input_image=image_path, minimum_percentage_probability=30)
            sql = "INSERT IGNORE INTO detections (camID, datetime, detections) VALUES (%s, %s, %s)"
            val = (camId, datetime.strptime(image, "%Y-%m-%d-%H%M%S.jpg"), json.dumps(detections))
            cur.execute(sql, val)
            db.commit()

        except Exception as e:
            print(image_path, e)
