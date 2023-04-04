#!/bin/bash
python manage.py makrmigrations
python manage.py migrate 
python manage.py collectstatic 
gunicorn core.wsgi
python manage.py runserver 
