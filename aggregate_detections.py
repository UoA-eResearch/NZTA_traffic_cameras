#!/usr/bin/env python3

import json
import os

with open("cameras.json") as f:
    cameras = json.load(f)

for i,c in enumerate(cameras["features"]):
    camId = c["properties"]["id"]
    if not camId in os.listdir("annotations"):
        continue
    annotations = os.listdir(f"annotations/{camId}/")
    detections = {}
    for annotation_path in annotations:
        with open(f"annotations/{camId}/{annotation_path}") as f:
            a = json.load(f)
        dt = annotation_path.split(".")[0]
        vehicleSummary = {}
        for vehicle in a:
            vehicleSummary[vehicle["name"]] = vehicleSummary.get(vehicle["name"], 0) + 1
        detections[dt] = vehicleSummary
    cameras["features"][i]["detections"] = detections

with open("cameras_with_detections.json", "w") as f:
    json.dump(cameras, f, indent=4, sort_keys=True)
