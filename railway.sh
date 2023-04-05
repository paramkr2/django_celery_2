#!/bin/bash
python manage.py makemigrations
python manage.py migrate 
python manage.py collectstatic 
gunicorn core.wsgi --daemon
celery --app=core worker --loglevel=info --concurrency 4 -P solo  --uid=0 --gid=0

#celery flower -A core --port=5555 --broker=redis://default:xP6JtBIJS2MAPfoLMxZS@containers-us-west-48.railway.app:7317
