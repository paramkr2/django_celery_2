#!/bin/sh

# python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"

#git key 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