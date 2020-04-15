#!/bin/bash
parallel --lb --delay 10 --bar -j 8 ./detect_cars.py {}