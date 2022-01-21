#!/usr/bin/env bash

python3 commed/manage.py migrate && python3 commed/manage.py createdb && python3 commed/manage.py initadmin && python3 commed/server.py
