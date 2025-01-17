#!/bin/bash

# Wait for postgres to be ready
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Start gunicorn
exec gunicorn --bind 0.0.0.0:8000 drivolution.wsgi:application