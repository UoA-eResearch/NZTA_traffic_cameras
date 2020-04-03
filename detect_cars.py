#!/usr/bin/env python3

from imageai.Detection import ObjectDetection

detector = ObjectDetection()

model_path = "./models/resnet50_coco_best_v2.0.1.h5"
input_path = "./images/709/2020-04-03-015043.jpg"
output_path = "./test.jpg"

detector.setModelTypeAsRetinaNet()
detector.setModelPath(model_path)
detector.loadModel()
custom_objects = detector.CustomObjects(car=True, motorcycle=True, bus=True, truck=True)
detection = detector.detectCustomObjectsFromImage(custom_objects=custom_objects, input_image=input_path, output_image_path=output_path, minimum_percentage_probability=30)

for eachItem in detection:
    print(eachItem["name"] , " : ", eachItem["percentage_probability"])