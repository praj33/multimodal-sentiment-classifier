# Multimodal Sentiment Analysis SDK

A Python SDK for interacting with the Multimodal Sentiment Analysis API. This SDK provides easy-to-use interfaces for analyzing sentiment from text, audio, video, and multimodal inputs.

## Installation

### From Source
```bash
git clone <repository-url>
cd multimodal_sentiment/sdk/python
pip install -e .
```

### From PyPI (when published)
```bash
pip install multimodal-sentiment-sdk
```

## Quick Start

### Basic Usage

```python
from sentiment_sdk import SentimentAnalyzer

# Initialize the analyzer
analyzer = SentimentAnalyzer(api_url="http://localhost:8000")

# Analyze text
result = analyzer.analyze_text("I love this product!")
print(f"Sentiment: {result['sentiment']}, Confidence: {result['confidence']}")

# Analyze audio file
audio_result = analyzer.analyze_audio("path/to/audio.wav")
print(f"Audio Sentiment: {audio_result['sentiment']}")

# Analyze video file
video_result = analyzer.analyze_video("path/to/video.mp4")
print(f"Video Sentiment: {video_result['sentiment']}")

# Multimodal analysis
multimodal_result = analyzer.analyze_multimodal("path/to/media.mp4")
print(f"Fused Sentiment: {multimodal_result['fused_sentiment']}")
print(f"Individual Results: {multimodal_result['individual']}")
```

### Convenience Function

```python
from sentiment_sdk import analyze_sentiment

# Quick text analysis
result = analyze_sentiment("This is amazing!", mode="text")

# Quick audio analysis
result = analyze_sentiment("audio.wav", mode="audio")

# Quick video analysis
result = analyze_sentiment("video.mp4", mode="video")

# Quick multimodal analysis
result = analyze_sentiment("media.mp4", mode="multimodal")
```

## Advanced Features

### Session Management

```python
analyzer = SentimentAnalyzer()

# Start a session for tracking related predictions
session_id = analyzer.start_session(user_id="user123")

# Perform analyses within the session
# (predictions will be automatically associated with the session)

# End the session
analyzer.end_session(session_id)
```

### Analytics and Statistics

```python
# Get overall statistics
stats = analyzer.get_statistics()
print(f"Total predictions: {stats['total_predictions']}")
print(f"Sentiment distribution: {stats['sentiment_distribution']}")

# Get recent predictions
recent = analyzer.get_recent_predictions(limit=10, mode="text")
for prediction in recent:
    print(f"{prediction['timestamp']}: {prediction['sentiment']}")
```

### Error Handling

```python
try:
    result = analyzer.analyze_text("Sample text")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except Exception as e:
    print(f"API error: {e}")
```

### Health Check

```python
if analyzer.health_check():
    print("API is healthy")
else:
    print("API is not responding")
```

## API Response Format

### Text/Audio/Video Analysis
```json
{
    "sentiment": "positive",
    "confidence": 0.85,
    "prediction_id": "uuid-string",
    "processing_time": 0.123
}
```

### Multimodal Analysis
```json
{
    "fused_sentiment": "positive",
    "confidence": 0.82,
    "individual": [
        {"modality": "audio", "sentiment": "positive", "confidence": 0.75},
        {"modality": "video", "sentiment": "positive", "confidence": 0.89}
    ],
    "prediction_id": "uuid-string",
    "processing_time": 1.456
}
```

## Configuration

### Custom API URL
```python
analyzer = SentimentAnalyzer(api_url="https://your-api-domain.com")
```

### Custom Timeout
```python
analyzer = SentimentAnalyzer(timeout=60)  # 60 seconds timeout
```

## Supported File Formats

- **Audio**: WAV, MP3, M4A, FLAC
- **Video**: MP4, AVI, MOV, MKV

## Requirements

- Python 3.7+
- requests >= 2.25.0

## License

MIT License

## Support

For issues and questions, please visit our GitHub repository or contact support@sentiment.ai.
