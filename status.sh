#!/bin/bash
echo `sudo mysql car -Ne "SELECT COUNT(*) FROM detections"` images processed out of `find /mnt/images/ -type f|wc -l`
