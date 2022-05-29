#!/bin/sh

Python3 -m venv django_venv
. django_venv/bin/activate
python3 -m pip install -r requirement.txt