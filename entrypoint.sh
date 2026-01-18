#!/bin/sh

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start server
if [ "$DEBUG" = "True" ]; then
    echo "Starting development server (runserver) with auto-reload..."
    python manage.py runserver 0.0.0.0:8000
else
    echo "Starting production server (gunicorn)..."
    gunicorn asopadel_barinas.wsgi:application --bind 0.0.0.0:8000
fi
