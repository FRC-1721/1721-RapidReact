#!/bin/bash 

cd /opt/dashboard/www && /opt/dashboard/dash_venv/bin/python -m pynetworktables2js --robot 10.17.21.2 --port=5800

# For testing
#cd /opt/dashboard/www && /opt/dashboard/dash_venv/bin/python -m pynetworktables2js --robot 10.17.21.235
