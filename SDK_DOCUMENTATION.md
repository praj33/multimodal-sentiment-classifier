# 📦 Python SDK Documentation - Day 3 Complete

## 📋 **Overview**

The **Multimodal Sentiment Analysis Python SDK** provides a simple, powerful interface for integrating sentiment analysis into your applications. This Day 3 documentation includes comprehensive examples, integration patterns, and team-specific usage guides.

---

## 🚀 **Quick Installation**

### **From Source (Current)**
```bash
# Clone the repository
git clone https://github.com/praj33/multimodal-sentiment-classifier.git
cd multimodal-sentiment-classifier

# Install SDK in development mode
pip install -e ./sdk/python

# Or install dependencies directly
pip install requests websockets asyncio
```

### **Direct Import (Alternative)**
```python
# Add to your Python path
import sys
sys.path.append('./sdk/python')

from sentiment_client import SentimentClient
```

---

## 🎯 **Basic Usage**

### **Initialize Client**
```python
from sdk.python.sentiment_client import SentimentClient

# Basic initialization
client = SentimentClient(base_url="http://localhost:8000")

# Advanced initialization with configuration
client = SentimentClient(
    base_url="http://localhost:8000",
    timeout=30,                    # Request timeout in seconds
    retry_attempts=3,              # Number of retry attempts
    retry_delay=1.0,              # Delay between retries
    api_key=None,                 # API key if authentication enabled
    verify_ssl=True,              # SSL certificate verification
    user_agent="MyApp/1.0"        # Custom user agent
)
```

### **Text Analysis**
```python
# Simple text analysis
result = client.analyze_text("I absolutely love this amazing product!")

print(f"Sentiment: {result['sentiment']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Model Version: {result['model_version']['text']}")

# Output:
# Sentiment: positive
# Confidence: 95.30%
# Model Version: v1.0
```

### **Audio Analysis**
```python
# Analyze audio file
result = client.analyze_audio("path/to/audio.wav")

print(f"Audio Sentiment: {result['sentiment']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Processing Time: {result['processing_time']:.3f}s")
print(f"File Size: {result['file_info']['size']} bytes")
```

### **Video Analysis**
```python
# Analyze video file
result = client.analyze_video("path/to/video.mp4")

print(f"Video Sentiment: {result['sentiment']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Model Version: {result['model_version']['video']}")
```

### **Multimodal Analysis**
```python
# Comprehensive multimodal analysis
result = client.analyze_multimodal("path/to/media.mp4")

print(f"Fused Sentiment: {result['fused_sentiment']}")
print(f"Overall Confidence: {result['confidence']:.2%}")

print("\nIndividual Results:")
for item in result['individual']:
    print(f"  {item['modality']}: {item['sentiment']} ({item['confidence']:.1%})")

print(f"\nModel Versions: {result['model_version']}")
```

---

## 🔧 **Advanced Features**

### **Batch Processing**
```python
# Batch text analysis
texts = [
    "I love this product!",
    "This is terrible quality.",
    "It's okay, nothing special.",
    "Absolutely fantastic experience!"
]

results = client.batch_analyze_text(texts)

for i, result in enumerate(results):
    print(f"Text {i+1}: {result['sentiment']} ({result['confidence']:.1%})")
```

### **Asynchronous Processing**
```python
import asyncio

async def async_analysis_example():
    """Example of asynchronous sentiment analysis"""
    
    # Async text analysis
    result = await client.analyze_text_async("Sample text for analysis")
    print(f"Async result: {result['sentiment']}")
    
    # Concurrent analysis of multiple files
    files = ["audio1.wav", "audio2.wav", "audio3.wav"]
    tasks = [client.analyze_audio_async(file) for file in files]
    results = await asyncio.gather(*tasks)
    
    for i, result in enumerate(results):
        print(f"File {i+1}: {result['sentiment']}")

# Run async example
# asyncio.run(async_analysis_example())
```

### **Streaming Analysis**
```python
# Stream analysis for long text
def stream_text_analysis(long_text, chunk_size=1000):
    """Stream analysis for long text content"""
    
    chunks = [long_text[i:i+chunk_size] for i in range(0, len(long_text), chunk_size)]
    results = []
    
    for i, chunk in enumerate(chunks):
        result = client.analyze_text(chunk)
        results.append({
            'chunk_id': i,
            'sentiment': result['sentiment'],
            'confidence': result['confidence'],
            'text_preview': chunk[:50] + "..."
        })
        
        print(f"Chunk {i+1}/{len(chunks)}: {result['sentiment']} ({result['confidence']:.1%})")
    
    return results

# Usage
long_text = "Your very long text content here..." * 100
stream_results = stream_text_analysis(long_text)
```

### **Real-time WebSocket Analysis**
```python
import asyncio
import websockets
import json

async def realtime_analysis(websocket_url, client_id="python_sdk"):
    """Real-time sentiment analysis via WebSocket"""
    
    uri = f"{websocket_url}/ws/realtime/{client_id}"
    
    async with websockets.connect(uri) as websocket:
        
        # Send analysis request
        await websocket.send(json.dumps({
            'type': 'text_analysis',
            'text': 'Real-time sentiment analysis test',
            'timestamp': time.time()
        }))
        
        # Receive result
        response = await websocket.recv()
        result = json.loads(response)
        
        print(f"Real-time result: {result}")
        
        return result

# Usage
# result = asyncio.run(realtime_analysis("ws://localhost:8000", "my_client"))
```

---

## 👥 **Team-Specific SDK Usage**

### **Gandhar's Team (Avatar Emotions)**
```python
class AvatarEmotionSDK:
    """SDK wrapper optimized for avatar emotion detection"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.client = SentimentClient(base_url)
        # Apply Gandhar's configuration
        self._configure_for_avatars()
    
    def _configure_for_avatars(self):
        """Configure SDK for avatar emotion detection"""
        # This would typically call the configuration API
        # For now, we'll document the expected behavior
        pass
    
    def detect_avatar_emotion(self, media_file):
        """Detect emotion for avatar expression"""
        result = self.client.analyze_multimodal(media_file)
        
        return {
            'primary_emotion': result['fused_sentiment'],
            'confidence': result['confidence'],
            'facial_emotion': self._extract_modality(result, 'video'),
            'vocal_emotion': self._extract_modality(result, 'audio'),
            'context_emotion': self._extract_modality(result, 'text'),
            'intensity': self._calculate_intensity(result['confidence']),
            'model_versions': result['model_version']
        }
    
    def _extract_modality(self, result, modality):
        """Extract specific modality result"""
        for item in result['individual']:
            if item['modality'] == modality:
                return {
                    'emotion': item['sentiment'],
                    'confidence': item['confidence']
                }
        return None
    
    def _calculate_intensity(self, confidence):
        """Calculate emotion intensity"""
        if confidence >= 0.9: return 'very_high'
        elif confidence >= 0.8: return 'high'
        elif confidence >= 0.6: return 'medium'
        elif confidence >= 0.4: return 'low'
        else: return 'very_low'

# Usage for Gandhar's team
avatar_sdk = AvatarEmotionSDK()
emotion_data = avatar_sdk.detect_avatar_emotion("user_video.mp4")
print(f"Avatar should express: {emotion_data['primary_emotion']} "
      f"with {emotion_data['intensity']} intensity")
```

### **Vedant/Rishabh's Team (AI Teacher)**
```python
class AITeacherSDK:
    """SDK wrapper optimized for educational scoring"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.client = SentimentClient(base_url)
        self._configure_for_education()
    
    def _configure_for_education(self):
        """Configure SDK for educational content analysis"""
        pass
    
    def score_student_response(self, response_file, question_context=None):
        """Score student response comprehensively"""
        result = self.client.analyze_multimodal(response_file)
        
        return {
            'overall_score': self._calculate_score(result),
            'content_analysis': self._analyze_content(result),
            'engagement_level': self._analyze_engagement(result),
            'feedback': self._generate_feedback(result),
            'model_versions': result['model_version']
        }
    
    def _calculate_score(self, result):
        """Calculate educational score from sentiment analysis"""
        # Simplified scoring logic
        confidence = result['confidence']
        sentiment = result['fused_sentiment']
        
        base_score = 70  # Base score
        if sentiment == 'positive':
            base_score += 20
        elif sentiment == 'neutral':
            base_score += 10
        
        # Adjust by confidence
        final_score = base_score + (confidence - 0.5) * 20
        return max(0, min(100, final_score))
    
    def batch_score_classroom(self, response_files):
        """Score multiple student responses"""
        results = []
        for file in response_files:
            score_result = self.score_student_response(file)
            results.append(score_result)
        return results

# Usage for Vedant/Rishabh's team
teacher_sdk = AITeacherSDK()
score_result = teacher_sdk.score_student_response("student_response.mp4")
print(f"Student Score: {score_result['overall_score']}/100")
```

### **Shashank's Team (Content Moderation)**
```python
class ContentModerationSDK:
    """SDK wrapper optimized for content moderation"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.client = SentimentClient(base_url)
        self._configure_for_moderation()
    
    def _configure_for_moderation(self):
        """Configure SDK for content moderation"""
        pass
    
    def moderate_content(self, content, content_type='text'):
        """Moderate content for safety"""
        if content_type == 'text':
            result = self.client.analyze_text(content)
        else:
            result = self.client.analyze_multimodal(content)
        
        return {
            'is_safe': self._determine_safety(result),
            'risk_level': self._calculate_risk(result),
            'action': self._determine_action(result),
            'confidence': result['confidence'],
            'reasoning': self._generate_reasoning(result),
            'model_versions': result['model_version']
        }
    
    def _determine_safety(self, result):
        """Determine if content is safe"""
        return not (result['sentiment'] == 'negative' and result['confidence'] > 0.9)
    
    def _calculate_risk(self, result):
        """Calculate risk level"""
        if result['sentiment'] == 'negative' and result['confidence'] > 0.95:
            return 'high'
        elif result['sentiment'] == 'negative' and result['confidence'] > 0.8:
            return 'medium'
        else:
            return 'low'
    
    def batch_moderate(self, content_items):
        """Moderate multiple content items"""
        results = []
        for item in content_items:
            mod_result = self.moderate_content(item['content'], item['type'])
            results.append({
                'item_id': item['id'],
                'moderation_result': mod_result
            })
        return results

# Usage for Shashank's team
moderation_sdk = ContentModerationSDK()
mod_result = moderation_sdk.moderate_content("User generated content here")
print(f"Content is safe: {mod_result['is_safe']}")
print(f"Action: {mod_result['action']}")
```

---

## 🔧 **Configuration & Customization**

### **Custom Configuration**
```python
# Configure client with custom settings
client = SentimentClient(
    base_url="http://localhost:8000",
    default_timeout=60,           # Longer timeout for large files
    max_file_size=50 * 1024 * 1024,  # 50MB limit
    supported_formats={
        'audio': ['.wav', '.mp3', '.ogg', '.m4a'],
        'video': ['.mp4', '.mov', '.avi']
    }
)
```

### **Error Handling**
```python
from sdk.python.exceptions import (
    SentimentAnalysisError,
    FileValidationError,
    APIConnectionError
)

try:
    result = client.analyze_text("Sample text")
except FileValidationError as e:
    print(f"File validation failed: {e}")
except APIConnectionError as e:
    print(f"API connection failed: {e}")
except SentimentAnalysisError as e:
    print(f"Analysis failed: {e}")
```

### **Logging Configuration**
```python
import logging

# Configure SDK logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('sentiment_sdk')

# Enable debug logging for troubleshooting
client = SentimentClient(
    base_url="http://localhost:8000",
    debug=True,
    log_requests=True
)
```

---

## 📊 **Performance & Monitoring**

### **Performance Monitoring**
```python
# Monitor SDK performance
performance_stats = client.get_performance_stats()
print(f"Average response time: {performance_stats['avg_response_time']:.3f}s")
print(f"Success rate: {performance_stats['success_rate']:.1%}")
print(f"Total requests: {performance_stats['total_requests']}")
```

### **Health Checks**
```python
# Check API health
health_status = client.check_health()
print(f"API Status: {health_status['status']}")
print(f"Version: {health_status['version_info']}")
```

---

## 🔍 **Troubleshooting**

### **Common Issues**

**Connection Errors:**
```python
# Retry with exponential backoff
import time

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except APIConnectionError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
```

**File Size Issues:**
```python
# Check file size before upload
import os

def safe_file_analysis(file_path, max_size=50*1024*1024):
    file_size = os.path.getsize(file_path)
    if file_size > max_size:
        raise ValueError(f"File too large: {file_size} bytes (max: {max_size})")
    
    return client.analyze_multimodal(file_path)
```

---

## ✅ **Best Practices**

1. **Always handle exceptions** for robust applications
2. **Use batch processing** for multiple items
3. **Implement retry logic** for network issues
4. **Monitor performance** in production
5. **Cache results** when appropriate
6. **Use team-specific configurations** for optimal results

---

## 📞 **Support**

- **Documentation**: [README.md](../README.md)
- **API Reference**: http://localhost:8000/docs
- **Team Guides**: [docs/team_integration/](../docs/team_integration/)
- **Issues**: GitHub repository issues

**🎉 Ready to integrate sentiment analysis into your application!**
