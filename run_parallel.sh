#!/bin/bash
while true; do
    ls images | parallel --lb --delay 10 -j 4 ./detect_cars.py {}
    echo done
done
