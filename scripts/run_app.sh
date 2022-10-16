#!/bin/bash
cd /home/ec2-user/acg-ocr
gunicorn --workers=2 --bind 0.0.0.0:5000 app:app