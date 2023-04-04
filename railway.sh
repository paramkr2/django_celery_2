#!/bin/bash
python manage.py migrate 
python manage.py collectstatic 
gunicorn core.wsgi
