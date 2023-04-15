#!/bin/bash
python manage.py makemigrations
python manage.py migrate 
python manage.py collectstatic 

celery --app=core worker --loglevel=info --concurrency 4 -P eventlet &

gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --log-level=info --log-file=-

#celery flower -A core --port=5555 --broker=redis://default:xP6JtBIJS2MAPfoLMxZS@containers-us-west-48.railway.app:7317
