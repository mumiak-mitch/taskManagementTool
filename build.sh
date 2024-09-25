#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies using Pipenv
pipenv install --deploy --ignore-pipfile

# Collect static files to the specified directory for serving in production
python manage.py collectstatic --no-input

# Create new migrations based on the changes detected in the models
python manage.py makemigrations

# Apply migrations to set up the PostgreSQL database schema
python manage.py migrate

# Create a superuser if the environment variable is set
if [[ $CREATE_SUPERUSER ]]; then
  python manage.py createsuperuser --no-input --email "$DJANGO_SUPERUSER_EMAIL"
fi
