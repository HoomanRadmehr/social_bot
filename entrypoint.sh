#!/bin/bash

echo "🔧 Making migrations..."
python manage.py makemigrations --noinput

echo "🗃️  Applying migrations..."
python manage.py migrate --noinput

echo "🧬 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting server..."
exec python manage.py runserver 0.0.0.0:8000
