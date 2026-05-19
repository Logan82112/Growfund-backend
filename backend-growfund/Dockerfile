# Use official Python runtime as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install system dependencies including bash
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files (no database access needed here)
RUN python manage.py collectstatic --noinput --clear || true

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "🔄 Running database migrations..."\n\
python manage.py migrate --noinput\n\
echo "⚙️ Setting up platform settings..."\n\
python manage.py setup_platform_settings || true\n\
echo "💰 Setting up crypto prices..."\n\
python manage.py setup_crypto_prices || true\n\
echo "🚀 Starting Gunicorn server..."\n\
exec gunicorn growfund.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 4 --timeout 120\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Expose port (Render will override with $PORT)
EXPOSE 8000

# Run entrypoint script
CMD ["/app/entrypoint.sh"]
