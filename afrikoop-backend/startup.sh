#!/bin/bash
# Azure App Service startup script for Django
# This script runs database migrations and collects static files before starting Gunicorn

set -e  # Exit on error

echo "==> Starting Django application on Azure App Service"

# Ensure /home/site directory exists (Azure persistent storage)
mkdir -p /home/site/media

# Set Django settings module
export DJANGO_SETTINGS_MODULE=afrikoop.settings_prod

# Run database migrations
echo "==> Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "==> Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist (only for initial setup)
# Uncomment and set credentials via environment variables if needed
# python manage.py shell -c "
# from django.contrib.auth import get_user_model;
# User = get_user_model();
# if not User.objects.filter(username='admin').exists():
#     User.objects.create_superuser('admin', 'admin@example.com', '$ADMIN_PASSWORD')
# "

# Start Gunicorn
echo "==> Starting Gunicorn server..."
exec gunicorn afrikoop.wsgi:application \
    --bind=0.0.0.0:8000 \
    --workers=2 \
    --threads=4 \
    --worker-class=gthread \
    --worker-tmp-dir=/dev/shm \
    --timeout=120 \
    --access-logfile=- \
    --error-logfile=- \
    --log-level=info

