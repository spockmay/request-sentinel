# --- Build stage ---
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt


# --- Runtime stage ---
FROM python:3.12-slim

WORKDIR /app

# Install libpq for psycopg2 runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Don't run as root
RUN useradd appuser && chown -R appuser /app
RUN mkdir -p /home/appuser && chown -R appuser:appuser /home/appuser
USER appuser

EXPOSE 5000

ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--timeout", "60", "run:app"]
