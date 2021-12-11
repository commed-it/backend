#!/usr/bin/env bash

python3 manage.py collectstatic --no-input

python3 manage.py flush --no-input

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py createdb

python3 manage.py initadmin

python3 server.py
