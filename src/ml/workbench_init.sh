#!/bin/bash
PROJECT_ID=""

cd /home/jupyter
sudo -H -u jupyter gsutil cp gs://${PROJECT_ID}-bucket/notebooks/* .
sudo -H -u jupyter rm -f notebook_template.ipynb