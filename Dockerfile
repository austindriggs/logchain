# --- Stage 1: Build Stage ---
FROM debian:bookworm-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY requirements.txt .

# Install dependencies to a local prefix
RUN pip install --no-cache-dir --break-system-packages --prefix=/install -r requirements.txt


# --- Stage 2: Runtime Stage ---
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the installed packages from the builder
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source and config
COPY src/ ./src/

EXPOSE 5000

# Run directly with Python
CMD ["python", "src/app.py"]
