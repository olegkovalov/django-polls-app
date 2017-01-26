#!/bin/sh

./manage.py collectstatic --noinput
./manage.py compilemessages

# In case when Postgres starts first time API container can make a requests before database would be created.
# To prevent this issue and run migrations and code properly we'll wait for Postgres.
# TODO: add some counter with max tries count and fail after reaching it's value.
until python manage.py migrate; do
  >&2 echo "Postgres database is unavailable - sleeping"
  sleep 1
done

gunicorn wsgi:application --workers $POLLS_GUNICORN_NUMBER_OF_WORKERS --bind :8000
