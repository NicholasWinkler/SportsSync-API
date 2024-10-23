#!/bin/bash

rm db.sqlite3
rm -rf ./SportsSync-API/migrations
python3 manage.py migrate
python3 manage.py makemigrations SportsSync-API
python3 manage.py migrate SportsSync-API
python3 manage.py loaddata users
python3 manage.py loaddata tokens

