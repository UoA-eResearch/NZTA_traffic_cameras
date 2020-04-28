#!/bin/bash
filename=`date +%Y-%m-%d-%H%M%S`.sql.gz
sudo mysqldump car | gzip > /mnt/mysqlbackups/$filename
