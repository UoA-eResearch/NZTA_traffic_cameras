#!/bin/bash
git pull
./run_parallel.sh
./aggregate_detections.py
git commit -am "auto update"
git push
