[supervisord]
nodaemon=true

[program:celery-worker]
command=celery -A core worker --loglevel=INFO -P eventlet
directory=/
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/celery-worker.log

[program:django-app]
command=python manage.py runserver 0.0.0.0:8000
directory=/
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/django-app.log
