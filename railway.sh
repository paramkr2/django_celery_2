#!/bin/bash
python manage.py makrmigrations
python manage.py migrate 
python manage.py collectstatic 
gunicorn locallibrary.wsgi
celery --app=core worker --loglevel=info --logfile=logs/celery.log -P eventlet
celery flower -A core --port=5555 --broker=redis://default:xP6JtBIJS2MAPfoLMxZS@containers-us-west-48.railway.app:7317
python manage.py runserver 