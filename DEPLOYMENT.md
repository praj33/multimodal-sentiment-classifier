# Deployment Guide - Multimodal Sentiment Analysis System

## Overview

This guide covers deployment options for the multimodal sentiment analysis system using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 4GB RAM (8GB recommended for GPU deployment)
- 10GB free disk space

## Quick Start

### CPU-Only Deployment (Recommended for most users)

```bash
# Clone the repository
git clone <repository-url>
cd multimodal_sentiment

# Start the CPU-based service
docker-compose --profile cpu up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f multimodal-sentiment-api
```

The API will be available at `http://localhost:8000`

### GPU-Enabled Deployment (For CUDA-capable systems)

```bash
# Ensure NVIDIA Docker runtime is installed
# Install nvidia-docker2 package first

# Start the GPU-enabled service
docker-compose --profile gpu up -d

# Check GPU utilization
docker exec -it multimodal_sentiment_multimodal-sentiment-api-gpu_1 nvidia-smi
```

### Development Environment

```bash
# Start development environment with hot reload
docker-compose --profile dev up -d

# Access development API at http://localhost:8001
```

## Configuration Options

### Environment Variables

Key environment variables in `.env`:

```bash
# Device Configuration
DEVICE=cpu                    # cpu or cuda
ENABLE_GPU=false             # true for GPU acceleration

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4                # Reduce to 2 for GPU deployment

# File Size Limits (50MB as per requirements)
MAX_FILE_SIZE_AUDIO=52428800
MAX_FILE_SIZE_VIDEO=52428800

# Model Versions
TEXT_MODEL_VERSION=v2.0
AUDIO_MODEL_VERSION=v1.0
VIDEO_MODEL_VERSION=v1.0
FUSION_MODEL_VERSION=v1.0

# Logging
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### Docker Compose Profiles

- `cpu`: CPU-only deployment (default)
- `gpu`: GPU-accelerated deployment
- `dev`: Development environment with hot reload
- `production`: Full production stack with nginx

## Production Deployment

### With Nginx Reverse Proxy

```bash
# Generate SSL certificates (replace with your domain)
mkdir -p ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem -out ssl/cert.pem

# Start full production stack
docker-compose --profile production --profile cpu up -d
```

Access via:
- HTTP: `http://localhost` (redirects to HTTPS)
- HTTPS: `https://localhost`

### Health Monitoring

```bash
# Check health status
curl http://localhost:8000/health

# Monitor container health
docker-compose ps
docker stats
```

## Scaling and Performance

### Horizontal Scaling

```bash
# Scale API service
docker-compose --profile cpu up -d --scale multimodal-sentiment-api=3

# Use nginx load balancer
docker-compose --profile production up -d
```

### Resource Limits

Current resource limits:
- CPU deployment: 2 CPU cores, 4GB RAM
- GPU deployment: 4 CPU cores, 8GB RAM, 1 GPU

Adjust in `docker-compose.yml` as needed.

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Change port in docker-compose.yml or stop conflicting service
   sudo lsof -i :8000
   ```

2. **Out of memory**
   ```bash
   # Reduce API workers or increase system memory
   # Edit API_WORKERS in .env
   ```

3. **GPU not detected**
   ```bash
   # Install nvidia-docker2
   sudo apt-get install nvidia-docker2
   sudo systemctl restart docker
   ```

4. **File upload fails**
   ```bash
   # Check file size limits (50MB max)
   # Verify file format (WAV, MP3, OGG, M4A for audio; MP4, MOV, AVI for video)
   ```

### Logs and Debugging

```bash
# View all logs
docker-compose logs

# Follow specific service logs
docker-compose logs -f multimodal-sentiment-api

# Debug container
docker exec -it <container_name> /bin/bash

# Check disk usage
docker system df
docker system prune  # Clean up unused resources
```

## Security Considerations

1. **SSL/TLS**: Always use HTTPS in production
2. **File validation**: System validates file types and sizes
3. **Rate limiting**: Nginx provides API rate limiting
4. **Non-root user**: Containers run as non-root user
5. **Network isolation**: Services use isolated Docker network

## Backup and Maintenance

### Data Backup

```bash
# Backup logs and models
docker run --rm -v multimodal_sentiment_logs:/data -v $(pwd):/backup \
  alpine tar czf /backup/logs-backup.tar.gz /data

# Backup configuration
cp -r config/ config-backup/
cp .env .env.backup
```

### Updates

```bash
# Pull latest images
docker-compose pull

# Restart with new images
docker-compose --profile cpu down
docker-compose --profile cpu up -d

# Clean old images
docker image prune
```

## API Endpoints

Once deployed, the following endpoints are available:

- `GET /health` - Health check
- `POST /predict/text` - Text sentiment analysis
- `POST /predict/audio` - Audio sentiment analysis  
- `POST /predict/video` - Video sentiment analysis
- `POST /predict/multimodal` - Combined multimodal analysis
- `POST /predict/batch` - Batch processing
- `GET /docs` - Interactive API documentation
- `GET /` - Web interface

## Support

For deployment issues:
1. Check logs: `docker-compose logs`
2. Verify configuration: `docker-compose config`
3. Test health endpoint: `curl http://localhost:8000/health`
4. Review resource usage: `docker stats`
