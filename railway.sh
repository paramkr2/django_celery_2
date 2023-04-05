#!/bin/bash
python manage.py makemigrations
python manage.py migrate 
python manage.py collectstatic 
gunicorn core.wsgi --daemon
python manage.py runscript load_data
celery --app=core worker --loglevel=info --logfile=logs/celery.log -P eventlet
celery flower -A core --port=5555 --broker=redis://default:xP6JtBIJS2MAPfoLMxZS@containers-us-west-48.railway.app:7317
