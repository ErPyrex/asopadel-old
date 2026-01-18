# === Build Stage ===
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Set working directory
WORKDIR /app

# Install system dependencies (essential for psycopg2 and other tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
# Note: .dockerignore takes care of what NOT to copy
COPY . /app/

# Make scripts executable
RUN chmod +x /app/entrypoint.sh /app/build.sh

# Entrypoint will handle migrations and starting the server
ENTRYPOINT ["/app/entrypoint.sh"]

# Default port for the app
EXPOSE 8000