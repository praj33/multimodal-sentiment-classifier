# 🐳 Docker Deployment Guide - Day 3 Complete

## 📋 **Overview**

This comprehensive guide covers **Docker deployment** for the Multimodal Sentiment Analysis API, including production configurations, scaling strategies, troubleshooting, and team-specific deployment scenarios.

---

## 🚀 **Quick Start Deployment**

### **Option 1: Docker Compose (Recommended)**
```bash
# 1️⃣ Clone the repository
git clone https://github.com/praj33/multimodal-sentiment-classifier.git
cd multimodal-sentiment-classifier

# 2️⃣ Start with Docker Compose
docker-compose up --build -d

# 3️⃣ Verify deployment
curl http://localhost:8000/health

# 4️⃣ Access dashboard
open http://localhost:8000/dashboard
```

### **Option 2: Manual Docker Build**
```bash
# Build the image
docker build -t multimodal-sentiment:latest .

# Run the container
docker run -d \
  --name sentiment-api \
  -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/config:/app/config \
  --restart unless-stopped \
  multimodal-sentiment:latest
```

---

## 🏗️ **Production Deployment**

### **Production Docker Compose**
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  sentiment-api:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
      - FUSION_HOT_RELOAD=false
      - LOG_LEVEL=INFO
      - MAX_WORKERS=4
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config:ro
      - ./data:/app/data:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - sentiment-api
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    command: redis-server --appendonly yes

volumes:
  redis_data:
```

### **Production Environment Variables**
```bash
# .env.production
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# API Configuration
MAX_WORKERS=4
WORKER_TIMEOUT=120
KEEP_ALIVE=2

# Fusion Configuration
FUSION_HOT_RELOAD=false
FUSION_METHOD=confidence_weighted
FUSION_TEXT_WEIGHT=0.5
FUSION_AUDIO_WEIGHT=0.25
FUSION_VIDEO_WEIGHT=0.25

# Security
CORS_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
RATE_LIMIT_PER_MINUTE=100

# Model Versions
TEXT_MODEL_VERSION=v1.0
AUDIO_MODEL_VERSION=v1.0
VIDEO_MODEL_VERSION=v1.0
FUSION_MODEL_VERSION=v1.0

# Database (if using)
DATABASE_URL=postgresql://user:pass@db:5432/sentiment
REDIS_URL=redis://redis:6379/0
```

---

## ⚙️ **Configuration Management**

### **Team-Specific Configurations**

**Gandhar's Avatar Deployment:**
```yaml
# docker-compose.gandhar.yml
version: '3.8'

services:
  sentiment-api:
    build: .
    environment:
      - TEAM_PRESET=gandhar_avatar_emotions
      - FUSION_METHOD=confidence_weighted
      - FUSION_TEXT_WEIGHT=0.3
      - FUSION_AUDIO_WEIGHT=0.4
      - FUSION_VIDEO_WEIGHT=0.3
      - CONFIDENCE_THRESHOLD=0.8
    ports:
      - "8000:8000"
    volumes:
      - ./config/gandhar_config.yaml:/app/config/fusion_config.yaml:ro
```

**Vedant/Rishabh's Education Deployment:**
```yaml
# docker-compose.education.yml
version: '3.8'

services:
  sentiment-api:
    build: .
    environment:
      - TEAM_PRESET=vedant_teacher_scoring
      - FUSION_METHOD=adaptive
      - FUSION_TEXT_WEIGHT=0.6
      - FUSION_AUDIO_WEIGHT=0.3
      - FUSION_VIDEO_WEIGHT=0.1
      - CONFIDENCE_THRESHOLD=0.75
    ports:
      - "8000:8000"
```

**Shashank's Moderation Deployment:**
```yaml
# docker-compose.moderation.yml
version: '3.8'

services:
  sentiment-api:
    build: .
    environment:
      - TEAM_PRESET=shashank_content_moderation
      - FUSION_METHOD=simple
      - FUSION_TEXT_WEIGHT=0.7
      - FUSION_AUDIO_WEIGHT=0.2
      - FUSION_VIDEO_WEIGHT=0.1
      - CONFIDENCE_THRESHOLD=0.9
    ports:
      - "8000:8000"
```

### **Multi-Environment Setup**
```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Staging
docker-compose -f docker-compose.yml -f docker-compose.staging.yml up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## 📈 **Scaling & Load Balancing**

### **Horizontal Scaling**
```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  sentiment-api:
    build: .
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    environment:
      - ENVIRONMENT=production
    networks:
      - sentiment_network

  load-balancer:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/load-balancer.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - sentiment-api
    networks:
      - sentiment_network

networks:
  sentiment_network:
    driver: overlay
```

### **Nginx Load Balancer Configuration**
```nginx
# nginx/load-balancer.conf
upstream sentiment_backend {
    least_conn;
    server sentiment-api_1:8000 max_fails=3 fail_timeout=30s;
    server sentiment-api_2:8000 max_fails=3 fail_timeout=30s;
    server sentiment-api_3:8000 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://sentiment_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # File upload size
        client_max_body_size 50M;
    }

    location /health {
        access_log off;
        proxy_pass http://sentiment_backend;
    }
}
```

### **Auto-Scaling with Docker Swarm**
```bash
# Initialize swarm
docker swarm init

# Deploy stack with auto-scaling
docker stack deploy -c docker-compose.scale.yml sentiment-stack

# Scale services
docker service scale sentiment-stack_sentiment-api=5

# Monitor services
docker service ls
docker service ps sentiment-stack_sentiment-api
```

---

## 🔧 **Advanced Configuration**

### **GPU Support**
```yaml
# docker-compose.gpu.yml
version: '3.8'

services:
  sentiment-api-gpu:
    build:
      context: .
      dockerfile: Dockerfile.gpu
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - CUDA_VISIBLE_DEVICES=0
      - USE_GPU=true
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### **Multi-Stage Build Optimization**
```dockerfile
# Dockerfile.optimized
FROM python:3.9-slim as base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base as development
COPY . .
ENV ENVIRONMENT=development
CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM base as production
COPY . .
RUN pip install gunicorn
ENV ENVIRONMENT=production
EXPOSE 8000
CMD ["gunicorn", "api:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### **Health Checks & Monitoring**
```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  sentiment-api:
    build: .
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  grafana_data:
```

---

## 🔍 **Troubleshooting**

### **Common Issues & Solutions**

**Container Won't Start:**
```bash
# Check logs
docker logs sentiment-api

# Check container status
docker ps -a

# Inspect container
docker inspect sentiment-api

# Common fixes:
# 1. Port already in use
docker ps | grep 8000
sudo lsof -i :8000

# 2. Permission issues
sudo chown -R $USER:$USER ./logs ./config

# 3. Memory issues
docker stats
```

**Performance Issues:**
```bash
# Monitor resource usage
docker stats sentiment-api

# Check API performance
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health

# Scale if needed
docker-compose up --scale sentiment-api=3
```

**File Upload Issues:**
```bash
# Check nginx configuration
docker exec nginx nginx -t

# Increase upload limits
# In nginx.conf: client_max_body_size 50M;

# Check disk space
df -h
docker system df
```

### **Debugging Commands**
```bash
# Enter container for debugging
docker exec -it sentiment-api bash

# Check environment variables
docker exec sentiment-api env

# Test API endpoints
docker exec sentiment-api curl http://localhost:8000/health

# Check configuration
docker exec sentiment-api cat /app/config/fusion_config.yaml

# Monitor logs in real-time
docker logs -f sentiment-api
```

### **Performance Optimization**
```bash
# Clean up unused resources
docker system prune -a

# Optimize image size
docker build --squash -t multimodal-sentiment:optimized .

# Use multi-stage builds
docker build --target production -t multimodal-sentiment:prod .

# Monitor memory usage
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

---

## 🔒 **Security Best Practices**

### **Production Security**
```yaml
# docker-compose.secure.yml
version: '3.8'

services:
  sentiment-api:
    build: .
    user: "1000:1000"  # Non-root user
    read_only: true
    tmpfs:
      - /tmp
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config:ro
    environment:
      - PYTHONDONTWRITEBYTECODE=1
      - PYTHONUNBUFFERED=1
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

### **SSL/TLS Configuration**
```nginx
# nginx/ssl.conf
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    location / {
        proxy_pass http://sentiment-api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 📊 **Monitoring & Logging**

### **Centralized Logging**
```yaml
# docker-compose.logging.yml
version: '3.8'

services:
  sentiment-api:
    build: .
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    environment:
      - LOG_LEVEL=INFO

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.14.0
    environment:
      - discovery.type=single-node
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:7.14.0
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline

  kibana:
    image: docker.elastic.co/kibana/kibana:7.14.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200

volumes:
  elasticsearch_data:
```

---

## ✅ **Deployment Checklist**

### **Pre-Deployment**
- [ ] Environment variables configured
- [ ] SSL certificates in place (production)
- [ ] Database connections tested
- [ ] Configuration files validated
- [ ] Resource limits set appropriately

### **Post-Deployment**
- [ ] Health checks passing
- [ ] API endpoints responding
- [ ] Logs being generated correctly
- [ ] Monitoring dashboards configured
- [ ] Backup procedures in place

### **Team-Specific Verification**
- [ ] **Gandhar**: Avatar emotion presets working
- [ ] **Vedant/Rishabh**: Educational scoring configured
- [ ] **Shashank**: Content moderation thresholds set
- [ ] **All Teams**: SDK integration tested

---

## 📞 **Support & Resources**

- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose Reference**: https://docs.docker.com/compose/
- **API Health Check**: http://localhost:8000/health
- **Container Logs**: `docker logs sentiment-api`
- **Team Integration Guides**: [docs/team_integration/](docs/team_integration/)

**🐳 Ready for production deployment with Docker!**
