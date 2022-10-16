#!/bin/bash
cd /home/ec2-user/acg-ocr
~/.local/bin/gunicorn --workers=2 --bind 0.0.0.0:5000 app:app