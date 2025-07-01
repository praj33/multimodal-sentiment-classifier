# 📚 API Reference Documentation - Day 3 Complete

## 📋 **Overview**

Complete API reference for the **Multimodal Sentiment Analysis API** with Day 3 enhancements including model versioning, enhanced validation, and team-specific configurations.

**Base URL**: `http://localhost:8000`  
**API Version**: `v2.0` (Day 3)  
**Authentication**: Optional (configurable)

---

## 🔗 **Interactive Documentation**

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 🎯 **Core Prediction Endpoints**

### **POST /predict/text**
Analyze sentiment from text input with enhanced Day 3 validation.

**Request:**
```http
POST /predict/text
Content-Type: application/json

{
  "text": "I absolutely love this amazing product!"
}
```

**Request Schema:**
```json
{
  "text": {
    "type": "string",
    "minLength": 1,
    "maxLength": 10000,
    "description": "Text content to analyze (1-10,000 characters)"
  }
}
```

**Response (Day 3 Format):**
```json
{
  "sentiment": "positive",
  "confidence": 0.95,
  "model_version": {
    "text": "v1.0"
  },
  "prediction_id": "text_1703123456",
  "processing_time": 0.087
}
```

**Response Schema:**
```json
{
  "sentiment": {
    "type": "string",
    "enum": ["positive", "negative", "neutral"]
  },
  "confidence": {
    "type": "number",
    "minimum": 0.0,
    "maximum": 1.0
  },
  "model_version": {
    "type": "object",
    "properties": {
      "text": {"type": "string"}
    }
  },
  "prediction_id": {"type": "string"},
  "processing_time": {"type": "number"}
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid input (text too long, empty, or malicious content)
- `422`: Validation error
- `429`: Rate limit exceeded
- `500`: Internal server error

---

### **POST /predict/audio**
Analyze sentiment from audio files with Day 3 enhanced validation.

**Request:**
```http
POST /predict/audio
Content-Type: multipart/form-data

file: [audio file]
```

**Supported Formats**: WAV, MP3, OGG, M4A  
**File Size Limit**: 50MB  
**Validation**: Magic number verification, file header validation

**Response (Day 3 Format):**
```json
{
  "sentiment": "positive",
  "confidence": 0.82,
  "model_version": {
    "audio": "v1.0"
  },
  "prediction_id": "audio_1703123456",
  "processing_time": 0.544,
  "file_info": {
    "filename": "audio_sample.wav",
    "size": 1024000
  }
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid file format or corrupted file
- `413`: File too large (>50MB)
- `415`: Unsupported media type
- `422`: File validation failed

---

### **POST /predict/video**
Analyze sentiment from video files with Day 3 enhanced validation.

**Request:**
```http
POST /predict/video
Content-Type: multipart/form-data

file: [video file]
```

**Supported Formats**: MP4, MOV, AVI  
**File Size Limit**: 50MB  
**Validation**: Magic number verification, file header validation

**Response (Day 3 Format):**
```json
{
  "sentiment": "neutral",
  "confidence": 0.78,
  "model_version": {
    "video": "v1.0"
  },
  "prediction_id": "video_1703123456",
  "processing_time": 1.247,
  "file_info": {
    "filename": "video_sample.mp4",
    "size": 5120000
  }
}
```

---

### **POST /predict/multimodal**
Comprehensive multimodal analysis with advanced fusion.

**Request:**
```http
POST /predict/multimodal
Content-Type: multipart/form-data

file: [audio or video file]
```

**Response (Day 3 Format with Complete Versioning):**
```json
{
  "fused_sentiment": "positive",
  "confidence": 0.87,
  "individual": [
    {"modality": "audio", "sentiment": "positive", "confidence": 0.85},
    {"modality": "video", "sentiment": "neutral", "confidence": 0.72},
    {"modality": "text", "sentiment": "positive", "confidence": 0.93}
  ],
  "model_version": {
    "text": "v1.0",
    "audio": "v1.0",
    "video": "v1.0",
    "fusion": "v1.0"
  },
  "prediction_id": "multimodal_1703123456",
  "processing_time": 1.457
}
```

---

## 🏥 **System Endpoints**

### **GET /health**
System health check with Day 3 version information.

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running",
  "version_info": {
    "model_versions": {
      "text": "v1.0",
      "audio": "v1.0",
      "video": "v1.0",
      "fusion": "v1.0"
    },
    "system_info": {
      "api_version": "v2.0",
      "last_updated": "2025-06-24T11:30:00Z",
      "validation_enhanced": true,
      "features": [
        "enhanced_file_validation",
        "magic_number_verification",
        "strict_size_limits",
        "comprehensive_sanitization"
      ]
    }
  },
  "validation": {
    "enhanced_file_validation": true,
    "magic_number_verification": true,
    "strict_size_limits": true,
    "comprehensive_sanitization": true
  }
}
```

### **GET /**
Root endpoint with API information.

**Response:**
```json
{
  "message": "Multimodal Sentiment Classifier API is running.",
  "version": "v2.0",
  "documentation": "/docs",
  "health": "/health"
}
```

---

## 🌐 **Web Interface Endpoints**

### **GET /dashboard**
Enhanced multimodal dashboard interface.

**Response**: HTML dashboard with file upload capabilities

**Features:**
- Drag & drop file upload
- Real-time processing indicators
- Multimodal result visualization
- Team-specific configuration options

### **GET /docs**
Interactive Swagger UI documentation.

### **GET /redoc**
Alternative ReDoc documentation interface.

---

## 📡 **Streaming Endpoints**

### **GET /stream/text**
Server-Sent Events for real-time text analysis.

**Request:**
```http
GET /stream/text?text=Your%20text%20here
```

**Response**: SSE stream with incremental results

### **WebSocket /ws/realtime/{client_id}**
Bidirectional real-time processing.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/realtime/client_123');
```

**Message Format:**
```json
{
  "type": "text_analysis",
  "text": "Text to analyze",
  "timestamp": 1703123456
}
```

---

## 📊 **Analytics Endpoints**

### **GET /analytics/stats**
Prediction statistics and performance metrics.

**Response:**
```json
{
  "total_predictions": 1250,
  "predictions_by_type": {
    "text": 800,
    "audio": 250,
    "video": 150,
    "multimodal": 50
  },
  "average_confidence": 0.82,
  "processing_times": {
    "text_avg": 0.087,
    "audio_avg": 0.544,
    "video_avg": 1.247,
    "multimodal_avg": 1.457
  },
  "success_rate": 0.98
}
```

### **GET /analytics/predictions**
Recent predictions with filtering options.

**Query Parameters:**
- `limit`: Number of results (default: 50, max: 100)
- `mode`: Filter by prediction type (text, audio, video, multimodal)
- `sentiment`: Filter by sentiment (positive, negative, neutral)
- `min_confidence`: Minimum confidence threshold

**Response:**
```json
{
  "predictions": [
    {
      "id": "pred_123",
      "type": "text",
      "sentiment": "positive",
      "confidence": 0.95,
      "timestamp": "2025-06-24T11:30:00Z"
    }
  ],
  "total": 1250,
  "filtered": 50
}
```

---

## 🔧 **Configuration Endpoints (Day 3)**

### **GET /config/fusion**
Get current fusion configuration.

**Response:**
```json
{
  "method": "confidence_weighted",
  "weights": {
    "text": 0.5,
    "audio": 0.25,
    "video": 0.25
  },
  "confidence_threshold": 0.7,
  "team_preset": null
}
```

### **POST /config/fusion/weights**
Update fusion weights at runtime.

**Request:**
```json
{
  "text": 0.6,
  "audio": 0.3,
  "video": 0.1
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Fusion weights updated successfully",
  "new_weights": {"text": 0.6, "audio": 0.3, "video": 0.1},
  "timestamp": 1719840000.0
}
```

### **POST /config/fusion/method**
Change fusion algorithm at runtime.

**Request:**
```json
{
  "method": "confidence_weighted"
}
```

**Available Methods:**
- `simple`: Basic weighted average
- `confidence_weighted`: Dynamic confidence-based weighting
- `adaptive`: Adaptive learning-based fusion

**Response:**
```json
{
  "status": "success",
  "message": "Fusion method updated to 'confidence_weighted'",
  "new_method": "confidence_weighted",
  "timestamp": 1719840000.0
}
```

### **POST /config/fusion/preset/{team_name}**
Apply team-specific configuration preset.

**Path Parameters:**
- `team_name`: One of `gandhar_avatar_emotions`, `vedant_teacher_scoring`, `shashank_content_moderation`

**Response:**
```json
{
  "status": "success",
  "message": "Applied configuration preset for team 'gandhar_avatar_emotions'",
  "team": "gandhar_avatar_emotions",
  "applied_config": {
    "method": "confidence_weighted",
    "weights": {"text": 0.3, "audio": 0.4, "video": 0.3},
    "confidence_threshold": 0.8
  },
  "timestamp": 1719840000.0
}
```

### **GET /config/fusion/presets**
List all available team configuration presets.

**Response:**
```json
{
  "status": "success",
  "presets": {
    "gandhar_avatar_emotions": {
      "method": "confidence_weighted",
      "weights": {"text": 0.3, "audio": 0.4, "video": 0.3},
      "confidence_threshold": 0.8,
      "focus": "emotional_nuance"
    },
    "vedant_teacher_scoring": {
      "method": "adaptive",
      "weights": {"text": 0.6, "audio": 0.3, "video": 0.1},
      "confidence_threshold": 0.75,
      "focus": "content_accuracy"
    },
    "shashank_content_moderation": {
      "method": "simple",
      "weights": {"text": 0.7, "audio": 0.2, "video": 0.1},
      "confidence_threshold": 0.9,
      "focus": "safety_detection"
    }
  },
  "count": 3,
  "timestamp": 1719840000.0
}
```

### **POST /config/fusion/reload**
Manually reload configuration from file.

**Response:**
```json
{
  "status": "success",
  "message": "Fusion configuration reloaded successfully",
  "config_timestamp": 1719840000.0,
  "current_method": "confidence_weighted",
  "current_weights": {"text": 0.5, "audio": 0.25, "video": 0.25}
}
```

---

## 🧪 **Testing & Benchmarking**

### **GET /benchmark/run**
Run performance benchmark suite.

**Response:**
```json
{
  "benchmark_results": {
    "text_analysis": {
      "avg_latency": 87.3,
      "throughput": 11.5,
      "success_rate": 1.0
    },
    "audio_analysis": {
      "avg_latency": 544.2,
      "throughput": 1.8,
      "success_rate": 0.98
    },
    "memory_usage": "2.1GB",
    "cpu_usage": "45%"
  }
}
```

### **GET /streaming/test**
Streaming functionality test page.

**Response**: HTML test interface for WebSocket connections

---

## ⚠️ **Error Responses**

### **Standard Error Format (Day 3)**
```json
{
  "error": "Detailed error message",
  "error_code": "VALIDATION_ERROR_400",
  "details": {
    "endpoint": "/predict/text",
    "method": "POST",
    "processing_time": 0.001,
    "timestamp": 1703123456
  },
  "system_version": {
    "api": "v2.0",
    "validation": "enhanced"
  }
}
```

### **Common Error Codes**
- `VALIDATION_ERROR_400`: Input validation failed
- `FILE_SIZE_ERROR_413`: File exceeds 50MB limit
- `RATE_LIMIT_ERROR_429`: Too many requests
- `INTERNAL_SERVER_ERROR`: Unexpected server error

---

## 🔒 **Security & Rate Limiting**

### **Rate Limits (Day 3)**
- **Default**: 100 requests per minute per IP
- **File uploads**: 10 requests per minute per IP
- **Streaming**: 5 concurrent connections per IP

### **Request Validation**
- **File size**: Maximum 50MB
- **Text length**: 1-10,000 characters
- **File types**: Strict validation with magic numbers
- **Content sanitization**: XSS and injection protection

### **Security Headers**
```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
```

---

## 📝 **Request/Response Examples**

### **cURL Examples**

**Text Analysis:**
```bash
curl -X POST "http://localhost:8000/predict/text" \
     -H "Content-Type: application/json" \
     -d '{"text": "I love this product!"}'
```

**Audio Analysis:**
```bash
curl -X POST "http://localhost:8000/predict/audio" \
     -F "file=@audio_sample.wav"
```

**Health Check:**
```bash
curl -X GET "http://localhost:8000/health"
```

### **Python SDK Examples**
```python
from sdk.python.sentiment_client import SentimentClient

client = SentimentClient(base_url="http://localhost:8000")

# Text analysis
result = client.analyze_text("Sample text")

# Audio analysis
result = client.analyze_audio("audio.wav")

# Multimodal analysis
result = client.analyze_multimodal("video.mp4")
```

---

## 📞 **Support & Resources**

- **Interactive Docs**: http://localhost:8000/docs
- **Health Status**: http://localhost:8000/health
- **Team Integration**: [docs/team_integration/](docs/team_integration/)
- **SDK Documentation**: [SDK_DOCUMENTATION.md](SDK_DOCUMENTATION.md)
- **Deployment Guide**: [DOCKER_DEPLOYMENT_GUIDE.md](DOCKER_DEPLOYMENT_GUIDE.md)

**🚀 Complete API reference for Day 3 integration!**
