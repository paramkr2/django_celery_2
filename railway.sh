#!/bin/bash
python manage.py migrate appname createmodels
python manage.py migrate 
python manage.py collectstatic 
celery --app=core worker --loglevel=info  -P eventlet --uid=0 --gid=0 &
gunicorn --log-level=debug core.wsgi 
#celery flower -A core --port=5555 --broker=redis://default:xP6JtBIJS2MAPfoLMxZS@containers-us-west-48.railway.app:7317
