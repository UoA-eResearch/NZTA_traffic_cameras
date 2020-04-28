#!/bin/bash
git pull
echo "starting aggregation"
./aggregate_detections.py
echo "sampling"
rm dts_per_camID.json
./sample_annotations.py > sample_annotations.json
git commit -am "auto update"
git push
