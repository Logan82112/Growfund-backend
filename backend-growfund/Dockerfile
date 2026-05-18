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

# Expose port (Render will override with $PORT)
EXPOSE 8000

# Run migrations and start server
CMD python manage.py migrate --noinput && \
    python manage.py setup_platform_settings || true && \
    python manage.py setup_crypto_prices || true && \
    gunicorn growfund.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 4 --timeout 120
