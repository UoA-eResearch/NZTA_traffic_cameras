#!/bin/bash
ffmpeg -r 25 -pattern_type glob -i '/mnt/images/110/2020-04-2*.jpg' -c:v libx264 -pix_fmt yuv420p 2020-04-20-2020-04-30.mp4
