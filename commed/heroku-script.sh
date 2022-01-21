#!/usr/bin/env bash

python3 commed/manage.py collectstatic --no-input && python3 commed/manage.py flush --no-input && python3 commed/manage.py makemigrations && python3 commed/manage.py migrate && python3 commed/manage.py createdb && python3 commed/manage.py initadmin && python3 commed/server.py
