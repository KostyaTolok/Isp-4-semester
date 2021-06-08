#!/bin/bash

host="eshopdb"
port="3306"

echo "Waiting for database start"
until curl http://"$host":"$port"; do
  sleep 1
done

echo "Applying database migrations"
python manage.py migrate

echo "Creating superuser"
python manage.py createsuperuser --noinput


echo "Starting server on 0.0.0.0:8000"
python manage.py runserver 0.0.0.0:8000
