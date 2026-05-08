#!/usr/bin/env bash
# Render Build Script - Runs on every deployment
# exit on error
set -o errexit

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🔄 Running database migrations..."
python manage.py migrate --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "⚙️ Setting up platform settings..."
python manage.py setup_platform_settings || true

echo "💰 Setting up crypto prices..."
python manage.py setup_crypto_prices || true

echo "✅ Build completed successfully!"
