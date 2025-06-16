#!/usr/bin/env python3
"""
Basic HTTP server for sentiment analysis - no external dependencies
Uses only Python standard library
"""

import json
import os
import sys
import time
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Add current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our classifiers
try:
    from classifiers.text_classifier import TextClassifier
    from classifiers.audio_classifier import AudioClassifier
    from classifiers.video_classifier import VideoClassifier
    from fusion.fusion_engine import FusionEngine
    from logging_system import sentiment_logger
    print("✅ All modules imported successfully")
except Exception as e:
    print(f"❌ Error importing modules: {e}")
    print("Make sure you're in the correct directory with all the classifier files")
    sys.exit(1)

class SentimentAPIHandler(BaseHTTPRequestHandler):
    # Class variables to store models (initialized once)
    _models_initialized = False
    _text_model = None
    _audio_model = None
    _video_model = None
    _fusion = None

    @classmethod
    def initialize_models(cls):
        """Initialize models once"""
        if not cls._models_initialized:
            print("🔄 Initializing AI models...")
            try:
                cls._text_model = TextClassifier()
                cls._audio_model = AudioClassifier()
                cls._video_model = VideoClassifier()
                cls._fusion = FusionEngine()
                cls._models_initialized = True
                print("✅ All models initialized successfully!")
            except Exception as e:
                print(f"❌ Error initializing models: {e}")
                raise

    def do_GET(self):
        """Handle GET requests"""
        self.initialize_models()
        
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_json_response({
                "message": "🎭 Multimodal Sentiment Analysis API",
                "status": "running",
                "endpoints": {
                    "text_analysis": "POST /predict/text",
                    "analytics": "GET /analytics/stats",
                    "documentation": "GET /docs"
                },
                "note": "Visit /docs for interactive documentation"
            })
            
        elif parsed_path.path == '/docs':
            self.send_html_docs()
            
        elif parsed_path.path == '/analytics/stats':
            try:
                stats = sentiment_logger.get_statistics()
                self.send_json_response(stats)
            except Exception as e:
                self.send_error_response(500, f"Error getting stats: {str(e)}")
                
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
            
            # Log the prediction
            prediction_id = sentiment_logger.log_prediction(
                input_data=text,
                mode="text",
                sentiment=sentiment,
                confidence=confidence,
                processing_time=processing_time
            )
            
            response = {
                "sentiment": sentiment,
                "confidence": round(confidence, 4),
                "prediction_id": prediction_id,
                "processing_time": round(processing_time, 4),
                "input_text": text[:100] + "..." if len(text) > 100 else text
            }
            
            self.send_json_response(response)
            print(f"✅ Text analysis: '{text[:50]}...' → {sentiment} ({confidence:.2f})")
            
        except Exception as e:
            self.send_error_response(500, f"Error analyzing text: {str(e)}")

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
    <title>🎭 Sentiment Analysis API</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        h1 { color: #333; text-align: center; margin-bottom: 30px; font-size: 2.5em; }
        .endpoint { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 10px; border-left: 5px solid #007acc; }
        .method { background: #28a745; color: white; padding: 5px 10px; border-radius: 5px; font-size: 12px; font-weight: bold; }
        .test-section { background: #fff3cd; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #ffc107; }
        input[type="text"] { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; margin: 10px 0; }
        button { background: #007acc; color: white; padding: 12px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; transition: background 0.3s; }
        button:hover { background: #005a9e; }
        .result { margin-top: 15px; padding: 15px; border-radius: 5px; font-weight: bold; }
        .positive { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .negative { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .neutral { background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }
        .status { background: #e7f3ff; padding: 15px; border-radius: 10px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎭 Multimodal Sentiment Analysis API</h1>
        
        <div class="status">
            <h3>📊 Server Status</h3>
            <p>✅ <strong>Server Running:</strong> http://127.0.0.1:8080</p>
            <p>✅ <strong>Text Classifier:</strong> Ready (BERT-based)</p>
            <p>✅ <strong>Audio Classifier:</strong> Ready (MFCC-based)</p>
            <p>✅ <strong>Video Classifier:</strong> Ready (MediaPipe-based)</p>
            <p>✅ <strong>Logging System:</strong> Active</p>
        </div>

        <div class="endpoint">
            <h3><span class="method">POST</span> /predict/text</h3>
            <p><strong>Description:</strong> Analyze sentiment of text input using BERT model</p>
            <p><strong>Request Body:</strong> <code>{"text": "Your text here"}</code></p>
            <p><strong>Response:</strong> <code>{"sentiment": "positive|negative|neutral", "confidence": 0.95, "prediction_id": "uuid"}</code></p>
        </div>

        <div class="test-section">
            <h3>🧪 Test Text Analysis</h3>
            <input type="text" id="textInput" placeholder="Enter text to analyze (e.g., 'I love this project!')" value="I absolutely love this amazing system!">
            <button onclick="analyzeText()">🔍 Analyze Sentiment</button>
            <div id="result"></div>
        </div>

        <div class="endpoint">
            <h3><span class="method">GET</span> /analytics/stats</h3>
            <p><strong>Description:</strong> Get prediction statistics and analytics</p>
            <button onclick="getStats()">📊 Get Statistics</button>
            <div id="statsResult"></div>
        </div>
    </div>

    <script>
        async function analyzeText() {
            const text = document.getElementById('textInput').value.trim();
            const resultDiv = document.getElementById('result');
            
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
                            <strong>Prediction ID:</strong> ${data.prediction_id}
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
    time.sleep(2)
    webbrowser.open(f'http://127.0.0.1:{port}/docs')

def start_server(port=8080):
    """Start the HTTP server"""
    try:
        server_address = ('127.0.0.1', port)
        httpd = HTTPServer(server_address, SentimentAPIHandler)
        
        print("🎭 Multimodal Sentiment Analysis API")
        print("=" * 50)
        print(f"🚀 Server starting on: http://127.0.0.1:{port}")
        print(f"📚 Documentation: http://127.0.0.1:{port}/docs")
        print(f"📊 Analytics: http://127.0.0.1:{port}/analytics/stats")
        print("🛑 Press Ctrl+C to stop the server")
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
