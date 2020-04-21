#!/usr/bin/env python3

import json
import os
from tqdm.auto import tqdm

with open("cameras.json") as f:
    cameras = json.load(f)

for i,c in enumerate(tqdm(cameras["features"])):
    camId = c["properties"]["id"]
    if not camId in os.listdir("annotations"):
        continue
    annotations = os.listdir(f"annotations/{camId}/")
    detections = {}
    for annotation_path in tqdm(annotations):
        with open(f"annotations/{camId}/{annotation_path}") as f:
            a = json.load(f)
        dt = annotation_path[:10]
        if dt not in detections:
            detections[dt] = {
                    "vehicles": 0,
                    "n_images": 0
            }
        detections[dt]["vehicles"] += len(a)
        detections[dt]["n_images"] += 1
    cameras["features"][i]["detections"] = detections

with open("cameras_with_detections.json", "w") as f:
    json.dump(cameras, f, indent=2, sort_keys=True)
