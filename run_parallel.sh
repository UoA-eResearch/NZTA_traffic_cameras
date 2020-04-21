#!/bin/bash
ls images | parallel --lb --delay 10 -j 8 ./detect_cars.py {}
