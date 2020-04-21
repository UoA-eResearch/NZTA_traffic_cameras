#!/bin/bash
git pull
./run_parallel.sh
./aggregate_detections.py
./sample_annotations.py > sample_annotations.json
git commit -am "auto update"
git push
