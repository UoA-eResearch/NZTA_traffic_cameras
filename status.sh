#!/bin/bash
echo $(printf "%'d" $(sudo mysql car -Ne "SELECT COUNT(*) FROM detections")) images processed out of $(printf "%'d" $(find /mnt/images/ -type f|wc -l))
