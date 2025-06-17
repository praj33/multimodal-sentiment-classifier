# Dockerfile - Production-ready multimodal sentiment analysis system
# Multi-stage build for optimized production deployment

# Build stage
FROM python:3.9-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    DEVICE=cpu \
    ENABLE_GPU=false

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    libsndfile1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs models config dev

# Copy configuration files
COPY config/ config/
COPY .env .env

# Set proper permissions
RUN chmod +x *.py

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Default command - can be overridden for GPU support
CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# GPU-enabled stage (optional)
FROM production as gpu

# Install CUDA dependencies (if needed)
USER root
RUN apt-get update && apt-get install -y \
    nvidia-cuda-toolkit \
    && rm -rf /var/lib/apt/lists/*

USER app

# Set GPU environment
ENV DEVICE=cuda
ENV ENABLE_GPU=true
ENV CUDA_VISIBLE_DEVICES=0

# GPU command
CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
