#!/bin/bash

# Install some stuff
cd /home/ec2-user/acg-ocr
sudo cp nginx.conf /etc/nginx/nginx.conf

python3 -m pip install -r /home/ec2-user/acg-ocr/requirements.txt

# Create and Enable the Service
sudo cp acg-ocr.service /etc/systemd/system/acg-ocr.service
sudo systemctl daemon-reload
sudo systemctl start acg-ocr.service

# Get the webserver pointing at the new service
sudo systemctl restart nginx
