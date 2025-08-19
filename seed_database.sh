#!/bin/bash

rm db.sqlite3
rm -rf ./tressreliefapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations tressreliefapi
python3 manage.py migrate tressreliefapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

