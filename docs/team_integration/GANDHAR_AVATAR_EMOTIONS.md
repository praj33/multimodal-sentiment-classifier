# 🎭 Gandhar's Team: Avatar Emotion Integration Guide

## 📋 **Overview**

This guide provides **Gandhar** and **Karthikeya** with everything needed to integrate the Multimodal Sentiment Analysis API for **avatar emotion detection**. The system is optimized for detecting emotional nuances from facial expressions, vocal tone, and contextual text.

---

## 🎯 **Use Case: Avatar Emotion Detection**

**Goal**: Analyze user input (video/audio) to determine emotional state for avatar expression control.

**Key Requirements:**
- **High accuracy** for emotional nuance detection
- **Real-time processing** for interactive avatars
- **Multimodal fusion** combining facial, vocal, and textual cues
- **Confidence scoring** for emotion reliability

---

## ⚙️ **Optimal Configuration**

### **Fusion Settings (Pre-configured)**
```yaml
# config/fusion_config.yaml
fusion:
  method: "confidence_weighted"  # Best for emotional nuance
  confidence_threshold: 0.8      # Higher threshold for emotion accuracy
  consensus_boost: 0.2          # Boost when all modalities agree

weights:
  text: 0.3    # Context and emotional words
  audio: 0.4   # Vocal tone, pitch, intensity
  video: 0.3   # Facial expressions, micro-expressions

# Avatar-specific settings
modalities:
  audio:
    min_confidence: 0.2
    weight_range: [0.2, 0.6]  # Allow higher audio weight for vocal emotions
  
  video:
    min_confidence: 0.2
    weight_range: [0.2, 0.6]  # Allow higher video weight for facial emotions
```

### **Apply Configuration**
```python
from fusion_config_manager import get_fusion_config_manager

# Apply Gandhar's preset
manager = get_fusion_config_manager()
success = manager.apply_team_preset('gandhar_avatar_emotions')
print(f"Avatar emotion config applied: {success}")
```

---

## 🚀 **Integration Examples**

### **Basic Avatar Emotion Detection**
```python
from sdk.python.sentiment_client import SentimentClient

# Initialize client
client = SentimentClient(base_url="http://localhost:8000")

def detect_avatar_emotion(media_file_path):
    """Detect emotion for avatar expression"""
    
    # Analyze multimodal input
    result = client.analyze_multimodal(media_file_path)
    
    # Extract emotion data
    emotion_data = {
        'primary_emotion': result['fused_sentiment'],
        'confidence': result['confidence'],
        'intensity': calculate_intensity(result['confidence']),
        
        # Individual modality emotions
        'facial_emotion': get_modality_result(result, 'video'),
        'vocal_emotion': get_modality_result(result, 'audio'),
        'context_emotion': get_modality_result(result, 'text'),
        
        # Metadata
        'processing_time': result['processing_time'],
        'model_versions': result['model_version']
    }
    
    return emotion_data

def get_modality_result(result, modality):
    """Extract specific modality result"""
    for item in result['individual']:
        if item['modality'] == modality:
            return {
                'emotion': item['sentiment'],
                'confidence': item['confidence']
            }
    return None

def calculate_intensity(confidence):
    """Convert confidence to emotion intensity"""
    if confidence >= 0.9:
        return 'very_high'
    elif confidence >= 0.8:
        return 'high'
    elif confidence >= 0.6:
        return 'medium'
    elif confidence >= 0.4:
        return 'low'
    else:
        return 'very_low'

# Example usage
emotion_data = detect_avatar_emotion("user_video.mp4")
print(f"Avatar should express: {emotion_data['primary_emotion']} "
      f"with {emotion_data['intensity']} intensity")
```

### **Real-time Avatar Emotion Streaming**
```python
import asyncio
import websockets
import json

async def stream_avatar_emotions(websocket_url, video_stream):
    """Stream real-time emotion detection for avatar"""
    
    async with websockets.connect(websocket_url) as websocket:
        
        # Send video frames for analysis
        for frame in video_stream:
            # Send frame data
            await websocket.send(json.dumps({
                'type': 'video_frame',
                'data': frame.to_base64(),
                'timestamp': frame.timestamp
            }))
            
            # Receive emotion result
            response = await websocket.recv()
            emotion_result = json.loads(response)
            
            # Update avatar expression
            update_avatar_expression(emotion_result)
            
            # Small delay for real-time processing
            await asyncio.sleep(0.1)

def update_avatar_expression(emotion_result):
    """Update avatar based on emotion result"""
    emotion = emotion_result.get('sentiment', 'neutral')
    confidence = emotion_result.get('confidence', 0.5)
    
    # Map emotions to avatar expressions
    expression_mapping = {
        'positive': 'happy',
        'negative': 'sad',
        'neutral': 'neutral'
    }
    
    avatar_expression = expression_mapping.get(emotion, 'neutral')
    
    # Apply expression with intensity based on confidence
    apply_avatar_expression(avatar_expression, confidence)

# Usage
# asyncio.run(stream_avatar_emotions("ws://localhost:8000/ws/realtime/avatar", video_stream))
```

### **Advanced Emotion Mapping**
```python
class AvatarEmotionMapper:
    """Advanced emotion mapping for avatar expressions"""
    
    def __init__(self):
        self.emotion_map = {
            # Primary emotions
            'positive': {
                'expressions': ['happy', 'excited', 'content'],
                'intensity_threshold': 0.7
            },
            'negative': {
                'expressions': ['sad', 'angry', 'frustrated'],
                'intensity_threshold': 0.6
            },
            'neutral': {
                'expressions': ['calm', 'thinking', 'attentive'],
                'intensity_threshold': 0.5
            }
        }
    
    def map_emotion_to_avatar(self, emotion_data):
        """Map detected emotion to avatar expression"""
        
        primary_emotion = emotion_data['primary_emotion']
        confidence = emotion_data['confidence']
        
        # Get facial and vocal emotions for nuance
        facial_emotion = emotion_data.get('facial_emotion', {})
        vocal_emotion = emotion_data.get('vocal_emotion', {})
        
        # Determine expression intensity
        intensity = self.calculate_expression_intensity(
            confidence, facial_emotion, vocal_emotion
        )
        
        # Select specific expression
        expression = self.select_expression(
            primary_emotion, facial_emotion, vocal_emotion
        )
        
        return {
            'expression': expression,
            'intensity': intensity,
            'duration': self.calculate_duration(confidence),
            'transition_speed': self.calculate_transition_speed(confidence)
        }
    
    def calculate_expression_intensity(self, confidence, facial, vocal):
        """Calculate expression intensity from multiple factors"""
        base_intensity = confidence
        
        # Boost intensity if facial and vocal agree
        if facial and vocal:
            if facial['emotion'] == vocal['emotion']:
                base_intensity += 0.1
        
        return min(1.0, base_intensity)
    
    def select_expression(self, primary, facial, vocal):
        """Select specific expression based on modality details"""
        
        # Use facial emotion if high confidence
        if facial and facial['confidence'] > 0.8:
            return self.map_sentiment_to_expression(facial['emotion'])
        
        # Use vocal emotion if high confidence
        if vocal and vocal['confidence'] > 0.8:
            return self.map_sentiment_to_expression(vocal['emotion'])
        
        # Fall back to primary emotion
        return self.map_sentiment_to_expression(primary)
    
    def map_sentiment_to_expression(self, sentiment):
        """Map sentiment to specific avatar expression"""
        mapping = {
            'positive': 'happy',
            'negative': 'sad',
            'neutral': 'calm'
        }
        return mapping.get(sentiment, 'neutral')

# Usage
mapper = AvatarEmotionMapper()
avatar_config = mapper.map_emotion_to_avatar(emotion_data)
```

---

## 🎛️ **Configuration Tuning**

### **For Different Emotion Types**

**Happy/Excited Emotions:**
```python
# Boost audio weight for vocal excitement
manager.update_weights({
    'text': 0.2,
    'audio': 0.5,  # Higher for vocal cues
    'video': 0.3
})
```

**Sad/Melancholy Emotions:**
```python
# Boost video weight for facial expressions
manager.update_weights({
    'text': 0.2,
    'audio': 0.3,
    'video': 0.5   # Higher for facial cues
})
```

**Subtle/Complex Emotions:**
```python
# Balanced weights with high confidence threshold
manager.update_weights({
    'text': 0.35,
    'audio': 0.35,
    'video': 0.3
})
manager.config['fusion']['confidence_threshold'] = 0.85
```

### **Runtime Adjustments**
```python
# Adjust based on avatar context
def adjust_for_avatar_context(context_type):
    """Adjust configuration based on avatar usage context"""
    
    if context_type == 'gaming':
        # Gaming avatars need quick, obvious emotions
        manager.update_weights({'text': 0.2, 'audio': 0.4, 'video': 0.4})
        manager.config['fusion']['confidence_threshold'] = 0.7
        
    elif context_type == 'education':
        # Educational avatars need subtle, appropriate emotions
        manager.update_weights({'text': 0.4, 'audio': 0.3, 'video': 0.3})
        manager.config['fusion']['confidence_threshold'] = 0.8
        
    elif context_type == 'therapy':
        # Therapy avatars need highly accurate, empathetic emotions
        manager.update_weights({'text': 0.3, 'audio': 0.4, 'video': 0.3})
        manager.config['fusion']['confidence_threshold'] = 0.9
```

---

## 📊 **Performance Optimization**

### **Batch Processing for Multiple Avatars**
```python
def process_multiple_avatars(avatar_inputs):
    """Process emotions for multiple avatars efficiently"""
    
    results = []
    
    # Batch process for efficiency
    for batch in chunk_inputs(avatar_inputs, batch_size=5):
        batch_results = client.batch_analyze_multimodal(batch)
        
        for result in batch_results:
            emotion_data = extract_avatar_emotion_data(result)
            results.append(emotion_data)
    
    return results
```

### **Caching for Repeated Expressions**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_emotion_mapping(emotion, confidence_level):
    """Cache emotion mappings for performance"""
    return mapper.map_emotion_to_avatar({
        'primary_emotion': emotion,
        'confidence': confidence_level
    })
```

---

## 🔧 **Troubleshooting**

### **Common Issues**

**Low Confidence Scores:**
```python
# Check individual modality confidences
for item in result['individual']:
    if item['confidence'] < 0.5:
        print(f"Low confidence in {item['modality']}: {item['confidence']}")
        
# Adjust weights to favor higher-confidence modalities
```

**Inconsistent Emotions:**
```python
# Check for disagreement between modalities
emotions = [item['sentiment'] for item in result['individual']]
if len(set(emotions)) > 1:
    print("Modalities disagree - consider adjusting fusion method")
```

**Performance Issues:**
```python
# Monitor processing times
if result['processing_time'] > 2.0:  # 2 seconds
    print("Slow processing - consider optimizing input size")
```

---

## 📞 **Support & Resources**

- **Configuration File**: `config/fusion_config.yaml`
- **Team Preset**: `gandhar_avatar_emotions`
- **API Documentation**: http://localhost:8000/docs
- **Fusion Guide**: [FUSION_CONFIGURATION_GUIDE.md](../../FUSION_CONFIGURATION_GUIDE.md)

**Contact**: Development team for advanced customization needs.

---

## ✅ **Quick Checklist**

- [ ] Applied `gandhar_avatar_emotions` preset
- [ ] Tested with sample video/audio files
- [ ] Configured emotion-to-expression mapping
- [ ] Set up real-time streaming (if needed)
- [ ] Optimized for target avatar platform
- [ ] Implemented error handling and fallbacks

**🎉 Ready to bring avatars to life with emotion!**
