#!/bin/bash
python manage.py makemigrations
python manage.py migrate 
python manage.py collectstatic 
gunicorn --daemon core.wsgi 
celery --app=core worker --loglevel=info  -P eventlet --uid=0 --gid=0 &

#celery flower -A core --port=5555 --broker=redis://default:xP6JtBIJS2MAPfoLMxZS@containers-us-west-48.railway.app:7317
