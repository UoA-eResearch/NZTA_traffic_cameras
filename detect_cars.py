#!/usr/bin/env python3

from imageai.Detection import ObjectDetection
import os
import json
from tqdm.auto import tqdm

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath("./models/resnet50_coco_best_v2.0.1.h5")
detector.loadModel()
print("Detector ready")
custom_objects = detector.CustomObjects(car=True, motorcycle=True, bus=True, truck=True)

camIds = os.listdir("images")

for camId in tqdm(camIds):
    os.makedirs(f"annotations/{camId}", exist_ok = True)
    images = os.listdir(f"images/{camId}/")
    for image in tqdm(images):
        if not image.endswith(".jpg"):
            continue
        image_path = f"images/{camId}/{image}"
        output_path = f"annotations/{camId}/{image}.json"
        if os.path.isfile(output_path): # skip done
            continue
        detected_image_array, detections = detector.detectCustomObjectsFromImage(output_type="array", custom_objects=custom_objects, input_image=image_path, minimum_percentage_probability=30)
        with open(output_path, "w") as f:
            json.dump(detections, f)