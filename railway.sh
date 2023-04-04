#!/bin/bash
python manage.py makrmigrations
python manage.py migrate 
python manage.py collectstatic 
gunicorn locallibrary.wsgi
python manage.py runserver 
