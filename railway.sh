#!/bin/bash
python manage.py makemigrations
python manage.py migrate 
python manage.py collectstatic 
gunicorn core.wsgi --daemon

celery --app=core worker --loglevel=info  -P eventlet --uid=nobody --gid=nogroup
#celery flower -A core --port=5555 --broker=redis://default:xP6JtBIJS2MAPfoLMxZS@containers-us-west-48.railway.app:7317
