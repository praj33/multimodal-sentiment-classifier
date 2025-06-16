#!/usr/bin/env python3
"""
Simple HTTP server for the sentiment analysis API
No external dependencies required - uses only Python built-ins
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import webbrowser
import time

# Import our classifiers
from classifiers.text_classifier import TextClassifier
from classifiers.audio_classifier import AudioClassifier
from classifiers.video_classifier import VideoClassifier
from fusion.fusion_engine import FusionEngine
from logging_system import sentiment_logger

class SentimentHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Initialize models
        if not hasattr(SentimentHandler, 'models_initialized'):
            print("🔄 Initializing models...")
            SentimentHandler.text_model = TextClassifier()
            SentimentHandler.audio_model = AudioClassifier()
            SentimentHandler.video_model = VideoClassifier()
            SentimentHandler.fusion = FusionEngine()
            SentimentHandler.models_initialized = True
            print("✅ Models initialized!")
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "message": "🎭 Multimodal Sentiment Analysis API",
                "status": "running",
                "endpoints": {
                    "text": "/predict/text",
                    "audio": "/predict/audio", 
                    "video": "/predict/video",
                    "multimodal": "/predict/multimodal",
                    "stats": "/analytics/stats"
                },
                "docs": "Open /docs for API documentation"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif parsed_path.path == '/docs':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            html_docs = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>🎭 Sentiment Analysis API Documentation</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                    .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    h1 { color: #333; border-bottom: 3px solid #007acc; padding-bottom: 10px; }
                    h2 { color: #007acc; margin-top: 30px; }
                    .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #007acc; }
                    .method { background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
                    code { background: #e9ecef; padding: 2px 6px; border-radius: 3px; }
                    .test-form { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🎭 Multimodal Sentiment Analysis API</h1>
                    
                    <h2>📋 Available Endpoints</h2>
                    
                    <div class="endpoint">
                        <h3><span class="method">POST</span> /predict/text</h3>
                        <p><strong>Description:</strong> Analyze sentiment of text input</p>
                        <p><strong>Body:</strong> <code>{"text": "Your text here"}</code></p>
                        
                        <div class="test-form">
                            <h4>🧪 Test Text Analysis:</h4>
                            <input type="text" id="textInput" placeholder="Enter text to analyze..." style="width: 300px; padding: 8px;">
                            <button onclick="testText()" style="padding: 8px 15px; background: #007acc; color: white; border: none; border-radius: 4px; cursor: pointer;">Analyze</button>
                            <div id="textResult" style="margin-top: 10px; font-weight: bold;"></div>
                        </div>
                    </div>
                    
                    <div class="endpoint">
                        <h3><span class="method">GET</span> /analytics/stats</h3>
                        <p><strong>Description:</strong> Get prediction statistics</p>
                        <button onclick="getStats()" style="padding: 8px 15px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer;">Get Stats</button>
                        <div id="statsResult" style="margin-top: 10px;"></div>
                    </div>
                    
                    <h2>📊 Server Status</h2>
                    <p>✅ Server is running on: <strong>http://127.0.0.1:8005</strong></p>
                    <p>✅ Text Classifier: Ready</p>
                    <p>✅ Audio Classifier: Ready</p>
                    <p>✅ Video Classifier: Ready</p>
                    <p>✅ Logging System: Active</p>
                </div>
                
                <script>
                    async function testText() {
                        const text = document.getElementById('textInput').value;
                        if (!text) {
                            alert('Please enter some text');
                            return;
                        }
                        
                        try {
                            const response = await fetch('/predict/text', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({text: text})
                            });
                            const result = await response.json();
                            document.getElementById('textResult').innerHTML = 
                                `Result: <span style="color: ${result.sentiment === 'positive' ? 'green' : result.sentiment === 'negative' ? 'red' : 'orange'}">${result.sentiment}</span> (${(result.confidence * 100).toFixed(1)}% confidence)`;
                        } catch (error) {
                            document.getElementById('textResult').innerHTML = 'Error: ' + error.message;
                        }
                    }
                    
                    async function getStats() {
                        try {
                            const response = await fetch('/analytics/stats');
                            const stats = await response.json();
                            document.getElementById('statsResult').innerHTML = 
                                `<pre>${JSON.stringify(stats, null, 2)}</pre>`;
                        } catch (error) {
                            document.getElementById('statsResult').innerHTML = 'Error: ' + error.message;
                        }
                    }
                </script>
            </body>
            </html>
            """
            self.wfile.write(html_docs.encode())
            
        elif parsed_path.path == '/analytics/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            stats = sentiment_logger.get_statistics()
            self.wfile.write(json.dumps(stats, indent=2).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            if parsed_path.path == '/predict/text':
                data = json.loads(post_data.decode('utf-8'))
                text = data.get('text', '')
                
                if not text:
                    self.send_error_response(400, "Text is required")
                    return
                
                # Analyze text
                start_time = time.time()
                sentiment, confidence = self.text_model.predict(text)
                processing_time = time.time() - start_time
                
                # Log prediction
                prediction_id = sentiment_logger.log_prediction(
                    input_data=text,
                    mode="text",
                    sentiment=sentiment,
                    confidence=confidence,
                    processing_time=processing_time
                )
                
                response = {
                    "sentiment": sentiment,
                    "confidence": confidence,
                    "prediction_id": prediction_id,
                    "processing_time": processing_time
                }
                
                self.send_json_response(response)
                
            else:
                self.send_error_response(404, "Endpoint not found")
                
        except Exception as e:
            self.send_error_response(500, str(e))

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def send_error_response(self, code, message):
        """Send error response"""
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        error_response = {"error": message}
        self.wfile.write(json.dumps(error_response).encode())

    def log_message(self, format, *args):
        """Override to reduce log noise"""
        pass

def start_server(port=8005):
    """Start the HTTP server"""
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, SentimentHandler)
    
    print(f"🚀 Starting Sentiment Analysis Server...")
    print(f"📍 Server running on: http://127.0.0.1:{port}")
    print(f"📚 API Documentation: http://127.0.0.1:{port}/docs")
    print(f"🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Auto-open browser after a short delay
    def open_browser():
        time.sleep(2)
        webbrowser.open(f'http://127.0.0.1:{port}/docs')
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.shutdown()

if __name__ == "__main__":
    start_server()
