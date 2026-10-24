# Production Dockerfile for Face Recognition Web System on Render / Cloud
FROM python:3.10-slim

# Install system libraries needed by OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Render dynamically sets $PORT (defaults to 10000 if not set)
ENV PORT=10000
EXPOSE $PORT

# Run Gunicorn WSGI server hosting the Pink UI Web App
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-10000} --workers 2 --timeout 120"]
