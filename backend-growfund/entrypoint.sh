#!/bin/bash
set -e

echo "🔄 Running database migrations..."
python manage.py migrate --noinput

echo "⚙️ Setting up platform settings..."
python manage.py setup_platform_settings || true

echo "💰 Setting up crypto prices..."
python manage.py setup_crypto_prices || true

echo "👤 Creating admin users..."
python create_tabby_admin.py || true
python create_new_admin.py || true

echo "🚀 Starting Gunicorn server..."
exec gunicorn growfund.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 4 --timeout 120
