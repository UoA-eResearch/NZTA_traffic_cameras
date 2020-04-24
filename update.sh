#!/bin/bash
git pull
./run_parallel.sh
echo "starting aggregation"
./aggregate_detections.py
echo "sampling"
./sample_annotations.py > sample_annotations.json
git commit -am "auto update"
git push
