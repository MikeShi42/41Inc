#!/bin/bash

./manage.py makemigrations --merge

./manage.py loaddata user
./manage.py loaddata sites
./manage.py loaddata series

./manage.py migrate


