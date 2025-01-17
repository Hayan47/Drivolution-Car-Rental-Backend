FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=drivolution.settings.production

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create directory for media files
RUN mkdir -p /app/media /app/static

# copying the project files but before the user switch
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Create a non-root user and set permissions
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

# Command to run the application
ENTRYPOINT ["./entrypoint.sh"]
