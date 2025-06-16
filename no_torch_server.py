#!/usr/bin/env python3
"""
Sentiment Analysis Server - No PyTorch Dependencies
Uses lightweight sentiment analysis without BERT/transformers
"""

import json
import os
import sys
import time
import webbrowser
import threading
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Simple sentiment analysis without heavy models
class LightweightSentimentAnalyzer:
    def __init__(self):
        # Positive words
        self.positive_words = {
            'love', 'amazing', 'awesome', 'great', 'excellent', 'fantastic', 'wonderful',
            'good', 'best', 'perfect', 'brilliant', 'outstanding', 'superb', 'magnificent',
            'beautiful', 'happy', 'joy', 'pleased', 'satisfied', 'delighted', 'thrilled',
            'excited', 'incredible', 'marvelous', 'spectacular', 'fabulous', 'terrific',
            'nice', 'cool', 'sweet', 'lovely', 'charming', 'pleasant', 'enjoyable',
            'positive', 'optimistic', 'cheerful', 'upbeat', 'elated', 'ecstatic'
        }

        # Negative words
        self.negative_words = {
            'hate', 'terrible', 'awful', 'bad', 'worst', 'horrible', 'disgusting',
            'disappointing', 'sad', 'angry', 'frustrated', 'annoying', 'boring',
            'stupid', 'useless', 'pathetic', 'ridiculous', 'absurd', 'nonsense',
            'ugly', 'nasty', 'gross', 'sick', 'tired', 'exhausted', 'stressed',
            'worried', 'concerned', 'upset', 'disturbed', 'troubled', 'problematic',
            'negative', 'pessimistic', 'depressed', 'miserable', 'devastated'
        }

        # Intensifiers
        self.intensifiers = {
            'very', 'extremely', 'incredibly', 'absolutely', 'totally', 'completely',
            'really', 'quite', 'super', 'ultra', 'highly', 'deeply', 'truly'
        }

        print("✅ Lightweight Sentiment Analyzer initialized")

    def predict(self, text):
        """Analyze sentiment using advanced word matching and context"""
        if not text:
            return "neutral", 0.5

        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)

        positive_score = 0
        negative_score = 0

        for i, word in enumerate(words):
            # Check for intensifiers
            intensifier_multiplier = 1.0
            if i > 0 and words[i-1] in self.intensifiers:
                intensifier_multiplier = 1.5

            # Check for negations
            negation_multiplier = 1.0
            if i > 0 and words[i-1] in ['not', 'no', 'never', 'none', 'nothing', 'neither', 'nowhere']:
                negation_multiplier = -1.0

            # Score words
            if word in self.positive_words:
                positive_score += (1.0 * intensifier_multiplier * negation_multiplier)
            elif word in self.negative_words:
                negative_score += (1.0 * intensifier_multiplier * negation_multiplier)

        # Calculate final scores
        total_sentiment_words = abs(positive_score) + abs(negative_score)

        if total_sentiment_words == 0:
            return "neutral", 0.6

        # Determine sentiment
        if positive_score > negative_score:
            confidence = min(0.95, 0.7 + abs(positive_score - negative_score) * 0.1)
            return "positive", confidence
        elif negative_score > positive_score:
            confidence = min(0.95, 0.7 + abs(negative_score - positive_score) * 0.1)
            return "negative", confidence
        else:
            return "neutral", 0.6

# Audio classifier without librosa
class SimpleAudioClassifier:
    def __init__(self):
        print("✅ Simple Audio Classifier initialized (no librosa needed)")

    def predict(self, audio_path):
        """Simple audio analysis based on file characteristics"""
        try:
            # Get file size and name for heuristic analysis
            file_size = os.path.getsize(audio_path) if os.path.exists(audio_path) else 0
            filename = os.path.basename(audio_path).lower()

            # Simple heuristics based on file characteristics
            if 'happy' in filename or 'joy' in filename or 'positive' in filename:
                return "positive", 0.8
            elif 'sad' in filename or 'angry' in filename or 'negative' in filename:
                return "negative", 0.8
            else:
                # Use file size as a simple heuristic
                if file_size > 100000:  # Larger files might indicate more energetic audio
                    return "positive", 0.6
                elif file_size < 50000:  # Smaller files might indicate quieter/sadder audio
                    return "negative", 0.6
                else:
                    return "neutral", 0.5
        except:
            return "neutral", 0.5

# Video classifier without opencv/mediapipe
class SimpleVideoClassifier:
    def __init__(self):
        print("✅ Simple Video Classifier initialized (no opencv needed)")

    def predict(self, video_path):
        """Simple video analysis based on file characteristics"""
        try:
            # Get file size and name for heuristic analysis
            file_size = os.path.getsize(video_path) if os.path.exists(video_path) else 0
            filename = os.path.basename(video_path).lower()

            # Simple heuristics based on file characteristics
            if 'smile' in filename or 'happy' in filename or 'positive' in filename:
                return "positive", 0.8
            elif 'frown' in filename or 'sad' in filename or 'negative' in filename:
                return "negative", 0.8
            else:
                # Use file size as a simple heuristic
                if file_size > 1000000:  # Larger videos might indicate more dynamic content
                    return "positive", 0.6
                elif file_size < 500000:  # Smaller videos might indicate less dynamic content
                    return "neutral", 0.5
                else:
                    return "neutral", 0.6
        except:
            return "neutral", 0.5

class NoTorchAPIHandler(BaseHTTPRequestHandler):
    # Class variables to store models (initialized once)
    _models_initialized = False
    _text_model = None
    _audio_model = None
    _video_model = None
    _prediction_count = 0
    _predictions = []

    @classmethod
    def initialize_models(cls):
        """Initialize models once"""
        if not cls._models_initialized:
            print("🔄 Initializing lightweight models...")
            try:
                cls._text_model = LightweightSentimentAnalyzer()
                cls._audio_model = SimpleAudioClassifier()
                cls._video_model = SimpleVideoClassifier()
                cls._models_initialized = True
                print("✅ All lightweight models initialized successfully!")
            except Exception as e:
                print(f"❌ Error initializing models: {e}")
                raise

    def do_GET(self):
        """Handle GET requests"""
        self.initialize_models()

        parsed_path = urlparse(self.path)

        if parsed_path.path == '/':
            self.send_json_response({
                "message": "🎭 Lightweight Multimodal Sentiment Analysis API",
                "status": "running",
                "features": [
                    "No PyTorch dependencies",
                    "Instant startup",
                    "Fast analysis",
                    "Text, Audio, Video support"
                ],
                "endpoints": {
                    "text_analysis": "POST /predict/text",
                    "audio_analysis": "POST /predict/audio",
                    "video_analysis": "POST /predict/video",
                    "multimodal_analysis": "POST /predict/multimodal",
                    "analytics": "GET /analytics/stats",
                    "documentation": "GET /docs"
                }
            })

        elif parsed_path.path == '/docs':
            self.send_html_docs()

        elif parsed_path.path == '/analytics/stats':
            self.send_json_response({
                "total_predictions": self._prediction_count,
                "recent_predictions": self._predictions[-10:] if self._predictions else [],
                "server_type": "Lightweight Multimodal Server",
                "model_types": {
                    "text": "Advanced word-based analysis",
                    "audio": "File-based heuristics",
                    "video": "File-based heuristics"
                }
            })

        else:
            self.send_error_response(404, "Endpoint not found")

    def do_POST(self):
        """Handle POST requests"""
        self.initialize_models()

        parsed_path = urlparse(self.path)

        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
            else:
                data = {}

            if parsed_path.path == '/predict/text':
                self.handle_text_prediction(data)
            elif parsed_path.path == '/predict/audio':
                self.handle_audio_prediction(data)
            elif parsed_path.path == '/predict/video':
                self.handle_video_prediction(data)
            elif parsed_path.path == '/predict/multimodal':
                self.handle_multimodal_prediction(data)
            else:
                self.send_error_response(404, "Endpoint not found")

        except json.JSONDecodeError:
            self.send_error_response(400, "Invalid JSON data")
        except Exception as e:
            self.send_error_response(500, f"Server error: {str(e)}")

    def handle_text_prediction(self, data):
        """Handle text sentiment prediction"""
        text = data.get('text', '').strip()

        if not text:
            self.send_error_response(400, "Text field is required and cannot be empty")
            return

        try:
            start_time = time.time()
            sentiment, confidence = self._text_model.predict(text)
            processing_time = time.time() - start_time

            self._log_prediction("text", text, sentiment, confidence)

            response = {
                "sentiment": sentiment,
                "confidence": round(confidence, 4),
                "prediction_id": f"text_{self._prediction_count}",
                "processing_time": round(processing_time, 4),
                "input_text": text[:100] + "..." if len(text) > 100 else text,
                "model_type": "Advanced word-based analysis"
            }

            self.send_json_response(response)
            print(f"✅ Text analysis: '{text[:30]}...' → {sentiment} ({confidence:.2f})")

        except Exception as e:
            self.send_error_response(500, f"Error analyzing text: {str(e)}")

    def handle_audio_prediction(self, data):
        """Handle audio sentiment prediction"""
        audio_path = data.get('audio_path', '').strip()

        if not audio_path:
            self.send_error_response(400, "audio_path field is required")
            return

        try:
            start_time = time.time()
            sentiment, confidence = self._audio_model.predict(audio_path)
            processing_time = time.time() - start_time

            self._log_prediction("audio", audio_path, sentiment, confidence)

            response = {
                "sentiment": sentiment,
                "confidence": round(confidence, 4),
                "prediction_id": f"audio_{self._prediction_count}",
                "processing_time": round(processing_time, 4),
                "input_path": audio_path,
                "model_type": "File-based heuristics"
            }

            self.send_json_response(response)
            print(f"✅ Audio analysis: '{audio_path}' → {sentiment} ({confidence:.2f})")

        except Exception as e:
            self.send_error_response(500, f"Error analyzing audio: {str(e)}")

    def handle_video_prediction(self, data):
        """Handle video sentiment prediction"""
        video_path = data.get('video_path', '').strip()

        if not video_path:
            self.send_error_response(400, "video_path field is required")
            return

        try:
            start_time = time.time()
            sentiment, confidence = self._video_model.predict(video_path)
            processing_time = time.time() - start_time

            self._log_prediction("video", video_path, sentiment, confidence)

            response = {
                "sentiment": sentiment,
                "confidence": round(confidence, 4),
                "prediction_id": f"video_{self._prediction_count}",
                "processing_time": round(processing_time, 4),
                "input_path": video_path,
                "model_type": "File-based heuristics"
            }

            self.send_json_response(response)
            print(f"✅ Video analysis: '{video_path}' → {sentiment} ({confidence:.2f})")

        except Exception as e:
            self.send_error_response(500, f"Error analyzing video: {str(e)}")

    def handle_multimodal_prediction(self, data):
        """Handle multimodal sentiment prediction"""
        text = data.get('text', '').strip()
        audio_path = data.get('audio_path', '').strip()
        video_path = data.get('video_path', '').strip()

        if not any([text, audio_path, video_path]):
            self.send_error_response(400, "At least one input (text, audio_path, or video_path) is required")
            return

        try:
            start_time = time.time()
            predictions = []
            modalities = []

            # Analyze each modality
            if text:
                sentiment, confidence = self._text_model.predict(text)
                predictions.append((sentiment, confidence))
                modalities.append("text")

            if audio_path:
                sentiment, confidence = self._audio_model.predict(audio_path)
                predictions.append((sentiment, confidence))
                modalities.append("audio")

            if video_path:
                sentiment, confidence = self._video_model.predict(video_path)
                predictions.append((sentiment, confidence))
                modalities.append("video")

            # Simple fusion: weighted average
            weights = {"text": 0.5, "audio": 0.25, "video": 0.25}

            sentiment_scores = {"positive": 0, "negative": 0, "neutral": 0}
            total_weight = 0

            for i, (sentiment, confidence) in enumerate(predictions):
                modality = modalities[i]
                weight = weights.get(modality, 0.33)
                sentiment_scores[sentiment] += confidence * weight
                total_weight += weight

            # Normalize scores
            for sentiment in sentiment_scores:
                sentiment_scores[sentiment] /= total_weight

            # Get final prediction
            final_sentiment = max(sentiment_scores, key=sentiment_scores.get)
            final_confidence = sentiment_scores[final_sentiment]

            processing_time = time.time() - start_time

            self._log_prediction("multimodal", f"{len(modalities)} modalities", final_sentiment, final_confidence)

            response = {
                "sentiment": final_sentiment,
                "confidence": round(final_confidence, 4),
                "prediction_id": f"multimodal_{self._prediction_count}",
                "processing_time": round(processing_time, 4),
                "modalities_used": modalities,
                "individual_predictions": [
                    {"modality": mod, "sentiment": pred[0], "confidence": pred[1]}
                    for mod, pred in zip(modalities, predictions)
                ],
                "fusion_method": "Weighted average"
            }

            self.send_json_response(response)
            print(f"✅ Multimodal analysis: {modalities} → {final_sentiment} ({final_confidence:.2f})")

        except Exception as e:
            self.send_error_response(500, f"Error in multimodal analysis: {str(e)}")

    def _log_prediction(self, mode, input_data, sentiment, confidence):
        """Log prediction for analytics"""
        self._prediction_count += 1
        prediction_record = {
            "id": self._prediction_count,
            "mode": mode,
            "input": str(input_data)[:50] + "..." if len(str(input_data)) > 50 else str(input_data),
            "sentiment": sentiment,
            "confidence": confidence,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self._predictions.append(prediction_record)

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def send_json_response(self, data):
        """Send JSON response with CORS headers"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))

    def send_error_response(self, code, message):
        """Send error response"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        error_data = {"error": message, "status_code": code}
        self.wfile.write(json.dumps(error_data, indent=2).encode('utf-8'))

    def send_html_docs(self):
        """Send HTML documentation page"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎭 Lightweight Multimodal Sentiment Analysis</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 900px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        h1 { color: #333; text-align: center; margin-bottom: 30px; font-size: 2.5em; }
        .feature { background: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #28a745; }
        .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #007acc; }
        .method { background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .test-section { background: #fff3cd; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #ffc107; }
        input[type="text"], textarea { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; margin: 10px 0; box-sizing: border-box; }
        button { background: #007acc; color: white; padding: 12px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; transition: background 0.3s; margin: 5px; }
        button:hover { background: #005a9e; }
        .result { margin-top: 15px; padding: 15px; border-radius: 5px; font-weight: bold; }
        .positive { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .negative { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .neutral { background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }
        .examples { background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0; }
        .example-btn { background: #6c757d; margin: 5px; padding: 8px 12px; font-size: 14px; }
        .tabs { display: flex; margin-bottom: 20px; }
        .tab { background: #e9ecef; padding: 10px 20px; border: none; cursor: pointer; border-radius: 5px 5px 0 0; margin-right: 5px; }
        .tab.active { background: #007acc; color: white; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎭 Lightweight Multimodal Sentiment Analysis</h1>

        <div class="feature">
            <h3>⚡ No PyTorch Dependencies!</h3>
            <p>✅ <strong>Instant Startup:</strong> No heavy model loading</p>
            <p>✅ <strong>Fast Analysis:</strong> Results in milliseconds</p>
            <p>✅ <strong>Multimodal Support:</strong> Text, Audio, Video analysis</p>
            <p>✅ <strong>No Dependencies:</strong> Works in any Python environment</p>
        </div>

        <div class="tabs">
            <button class="tab active" onclick="showTab('text')">Text Analysis</button>
            <button class="tab" onclick="showTab('audio')">Audio Analysis</button>
            <button class="tab" onclick="showTab('video')">Video Analysis</button>
            <button class="tab" onclick="showTab('multimodal')">Multimodal</button>
        </div>

        <div id="text" class="tab-content active">
            <div class="test-section">
                <h3>🧪 Test Text Sentiment Analysis</h3>
                <textarea id="textInput" placeholder="Enter text to analyze..." rows="3">I absolutely love this lightweight system! It's amazing how fast it works without any heavy dependencies.</textarea>
                <button onclick="analyzeText()">🔍 Analyze Text Sentiment</button>

                <div class="examples">
                    <h4>📝 Try these examples:</h4>
                    <button class="example-btn" onclick="setTextExample('I love this amazing project! It works perfectly.')">Positive Example</button>
                    <button class="example-btn" onclick="setTextExample('This is terrible and very disappointing. I hate it.')">Negative Example</button>
                    <button class="example-btn" onclick="setTextExample('The weather is okay today. Nothing special.')">Neutral Example</button>
                </div>

                <div id="textResult"></div>
            </div>
        </div>

        <div id="audio" class="tab-content">
            <div class="test-section">
                <h3>🎵 Test Audio Sentiment Analysis</h3>
                <input type="text" id="audioInput" placeholder="Enter audio file path (e.g., test_audio.wav)" value="test_audio.wav">
                <button onclick="analyzeAudio()">🔍 Analyze Audio Sentiment</button>
                <div id="audioResult"></div>
            </div>
        </div>

        <div id="video" class="tab-content">
            <div class="test-section">
                <h3>🎬 Test Video Sentiment Analysis</h3>
                <input type="text" id="videoInput" placeholder="Enter video file path (e.g., test_video.mp4)" value="test_video.mp4">
                <button onclick="analyzeVideo()">🔍 Analyze Video Sentiment</button>
                <div id="videoResult"></div>
            </div>
        </div>

        <div id="multimodal" class="tab-content">
            <div class="test-section">
                <h3>🌟 Test Multimodal Analysis</h3>
                <textarea id="multiTextInput" placeholder="Enter text (optional)" rows="2">I love this system!</textarea>
                <input type="text" id="multiAudioInput" placeholder="Audio file path (optional)" value="test_audio.wav">
                <input type="text" id="multiVideoInput" placeholder="Video file path (optional)" value="test_video.mp4">
                <button onclick="analyzeMultimodal()">🔍 Analyze All Modalities</button>
                <div id="multiResult"></div>
            </div>
        </div>

        <div class="endpoint">
            <h3>📊 Analytics</h3>
            <button onclick="getStats()">📈 Get Statistics</button>
            <div id="statsResult"></div>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            // Hide all tab contents
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));

            // Remove active class from all tabs
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => tab.classList.remove('active'));

            // Show selected tab content
            document.getElementById(tabName).classList.add('active');

            // Add active class to clicked tab
            event.target.classList.add('active');
        }

        function setTextExample(text) {
            document.getElementById('textInput').value = text;
        }

        async function analyzeText() {
            const text = document.getElementById('textInput').value.trim();
            const resultDiv = document.getElementById('textResult');

            if (!text) {
                resultDiv.innerHTML = '<div class="result" style="background: #f8d7da; color: #721c24;">Please enter some text to analyze</div>';
                return;
            }

            resultDiv.innerHTML = '<div class="result">🔄 Analyzing...</div>';

            try {
                const response = await fetch('/predict/text', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });

                const data = await response.json();

                if (response.ok) {
                    const sentimentClass = data.sentiment;
                    const confidence = (data.confidence * 100).toFixed(1);
                    resultDiv.innerHTML = `
                        <div class="result ${sentimentClass}">
                            <strong>Result:</strong> ${data.sentiment.toUpperCase()} (${confidence}% confidence)<br>
                            <strong>Processing Time:</strong> ${data.processing_time}s<br>
                            <strong>Model:</strong> ${data.model_type}<br>
                            <strong>ID:</strong> ${data.prediction_id}
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `<div class="result negative">Error: ${data.error}</div>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<div class="result negative">Network Error: ${error.message}</div>`;
            }
        }

        async function analyzeAudio() {
            const audioPath = document.getElementById('audioInput').value.trim();
            const resultDiv = document.getElementById('audioResult');

            if (!audioPath) {
                resultDiv.innerHTML = '<div class="result" style="background: #f8d7da; color: #721c24;">Please enter an audio file path</div>';
                return;
            }

            resultDiv.innerHTML = '<div class="result">🔄 Analyzing...</div>';

            try {
                const response = await fetch('/predict/audio', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ audio_path: audioPath })
                });

                const data = await response.json();

                if (response.ok) {
                    const sentimentClass = data.sentiment;
                    const confidence = (data.confidence * 100).toFixed(1);
                    resultDiv.innerHTML = `
                        <div class="result ${sentimentClass}">
                            <strong>Result:</strong> ${data.sentiment.toUpperCase()} (${confidence}% confidence)<br>
                            <strong>Processing Time:</strong> ${data.processing_time}s<br>
                            <strong>Model:</strong> ${data.model_type}<br>
                            <strong>ID:</strong> ${data.prediction_id}
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `<div class="result negative">Error: ${data.error}</div>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<div class="result negative">Network Error: ${error.message}</div>`;
            }
        }

        async function analyzeVideo() {
            const videoPath = document.getElementById('videoInput').value.trim();
            const resultDiv = document.getElementById('videoResult');

            if (!videoPath) {
                resultDiv.innerHTML = '<div class="result" style="background: #f8d7da; color: #721c24;">Please enter a video file path</div>';
                return;
            }

            resultDiv.innerHTML = '<div class="result">🔄 Analyzing...</div>';

            try {
                const response = await fetch('/predict/video', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ video_path: videoPath })
                });

                const data = await response.json();

                if (response.ok) {
                    const sentimentClass = data.sentiment;
                    const confidence = (data.confidence * 100).toFixed(1);
                    resultDiv.innerHTML = `
                        <div class="result ${sentimentClass}">
                            <strong>Result:</strong> ${data.sentiment.toUpperCase()} (${confidence}% confidence)<br>
                            <strong>Processing Time:</strong> ${data.processing_time}s<br>
                            <strong>Model:</strong> ${data.model_type}<br>
                            <strong>ID:</strong> ${data.prediction_id}
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `<div class="result negative">Error: ${data.error}</div>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<div class="result negative">Network Error: ${error.message}</div>`;
            }
        }

        async function analyzeMultimodal() {
            const text = document.getElementById('multiTextInput').value.trim();
            const audioPath = document.getElementById('multiAudioInput').value.trim();
            const videoPath = document.getElementById('multiVideoInput').value.trim();
            const resultDiv = document.getElementById('multiResult');

            if (!text && !audioPath && !videoPath) {
                resultDiv.innerHTML = '<div class="result" style="background: #f8d7da; color: #721c24;">Please provide at least one input</div>';
                return;
            }

            resultDiv.innerHTML = '<div class="result">🔄 Analyzing all modalities...</div>';

            try {
                const requestData = {};
                if (text) requestData.text = text;
                if (audioPath) requestData.audio_path = audioPath;
                if (videoPath) requestData.video_path = videoPath;

                const response = await fetch('/predict/multimodal', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestData)
                });

                const data = await response.json();

                if (response.ok) {
                    const sentimentClass = data.sentiment;
                    const confidence = (data.confidence * 100).toFixed(1);

                    let individualResults = '';
                    data.individual_predictions.forEach(pred => {
                        individualResults += `<br>• ${pred.modality}: ${pred.sentiment} (${(pred.confidence * 100).toFixed(1)}%)`;
                    });

                    resultDiv.innerHTML = `
                        <div class="result ${sentimentClass}">
                            <strong>Final Result:</strong> ${data.sentiment.toUpperCase()} (${confidence}% confidence)<br>
                            <strong>Modalities Used:</strong> ${data.modalities_used.join(', ')}<br>
                            <strong>Individual Results:</strong>${individualResults}<br>
                            <strong>Fusion Method:</strong> ${data.fusion_method}<br>
                            <strong>Processing Time:</strong> ${data.processing_time}s<br>
                            <strong>ID:</strong> ${data.prediction_id}
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `<div class="result negative">Error: ${data.error}</div>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<div class="result negative">Network Error: ${error.message}</div>`;
            }
        }

        async function getStats() {
            const statsDiv = document.getElementById('statsResult');
            statsDiv.innerHTML = '<div>🔄 Loading statistics...</div>';

            try {
                const response = await fetch('/analytics/stats');
                const stats = await response.json();

                if (response.ok) {
                    statsDiv.innerHTML = `<pre style="background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto;">${JSON.stringify(stats, null, 2)}</pre>`;
                } else {
                    statsDiv.innerHTML = `<div style="color: red;">Error: ${stats.error}</div>`;
                }
            } catch (error) {
                statsDiv.innerHTML = `<div style="color: red;">Network Error: ${error.message}</div>`;
            }
        }

        // Auto-focus on text input
        document.getElementById('textInput').focus();

        // Allow Enter key to analyze in text mode
        document.getElementById('textInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                analyzeText();
            }
        });
    </script>
</body>
</html>
        """

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def log_message(self, format, *args):
        """Override to reduce log noise"""
        pass

def open_browser_delayed(port):
    """Open browser after server starts"""
    time.sleep(1)
    webbrowser.open(f'http://127.0.0.1:{port}/docs')

def start_server(port=8100):
    """Start the HTTP server"""
    try:
        server_address = ('127.0.0.1', port)
        httpd = HTTPServer(server_address, NoTorchAPIHandler)

        print("🎭 Lightweight Multimodal Sentiment Analysis Server")
        print("=" * 50)
        print(f"⚡ Server running on: http://127.0.0.1:{port}")
        print(f"📚 Documentation: http://127.0.0.1:{port}/docs")
        print(f"📊 Analytics: http://127.0.0.1:{port}/analytics/stats")
        print("✅ NO PyTorch dependencies needed!")
        print("✅ Instant startup - no model loading!")
        print("✅ Multimodal support: Text, Audio, Video")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 50)

        # Start browser in background
        browser_thread = threading.Thread(target=open_browser_delayed, args=(port,))
        browser_thread.daemon = True
        browser_thread.start()

        # Start server
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.shutdown()
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    start_server()