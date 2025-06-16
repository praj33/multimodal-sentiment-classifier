#!/usr/bin/env python3
"""
Quick sentiment analysis server - no heavy models, instant startup
Uses lightweight sentiment analysis without BERT
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
class SimpleSentimentAnalyzer:
    def __init__(self):
        # Positive words
        self.positive_words = {
            'love', 'amazing', 'awesome', 'great', 'excellent', 'fantastic', 'wonderful',
            'good', 'best', 'perfect', 'brilliant', 'outstanding', 'superb', 'magnificent',
            'beautiful', 'happy', 'joy', 'pleased', 'satisfied', 'delighted', 'thrilled',
            'excited', 'incredible', 'marvelous', 'spectacular', 'fabulous', 'terrific',
            'nice', 'cool', 'sweet', 'lovely', 'charming', 'pleasant', 'enjoyable'
        }
        
        # Negative words
        self.negative_words = {
            'hate', 'terrible', 'awful', 'bad', 'worst', 'horrible', 'disgusting',
            'disappointing', 'sad', 'angry', 'frustrated', 'annoying', 'boring',
            'stupid', 'useless', 'pathetic', 'ridiculous', 'absurd', 'nonsense',
            'ugly', 'nasty', 'gross', 'sick', 'tired', 'exhausted', 'stressed',
            'worried', 'concerned', 'upset', 'disturbed', 'troubled', 'problematic'
        }
        
        print("✅ Simple Sentiment Analyzer initialized")

    def predict(self, text):
        """Analyze sentiment using word matching"""
        if not text:
            return "neutral", 0.5
        
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            return "neutral", 0.6
        
        if positive_count > negative_count:
            confidence = min(0.95, 0.7 + (positive_count - negative_count) * 0.1)
            return "positive", confidence
        elif negative_count > positive_count:
            confidence = min(0.95, 0.7 + (negative_count - positive_count) * 0.1)
            return "negative", confidence
        else:
            return "neutral", 0.6

class QuickAPIHandler(BaseHTTPRequestHandler):
    # Initialize analyzer once
    _analyzer = None
    _prediction_count = 0
    _predictions = []

    @classmethod
    def get_analyzer(cls):
        if cls._analyzer is None:
            cls._analyzer = SimpleSentimentAnalyzer()
        return cls._analyzer

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_json_response({
                "message": "🚀 Quick Sentiment Analysis API",
                "status": "running",
                "features": ["Instant startup", "No heavy models", "Fast analysis"],
                "endpoints": {
                    "text_analysis": "POST /predict/text",
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
                "server_type": "Quick Sentiment Server",
                "model_type": "Lightweight word-based analysis"
            })
                
        else:
            self.send_error_response(404, "Endpoint not found")

    def do_POST(self):
        """Handle POST requests"""
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
            analyzer = self.get_analyzer()
            sentiment, confidence = analyzer.predict(text)
            processing_time = time.time() - start_time
            
            # Store prediction
            self._prediction_count += 1
            prediction_record = {
                "id": self._prediction_count,
                "text": text[:50] + "..." if len(text) > 50 else text,
                "sentiment": sentiment,
                "confidence": confidence,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            self._predictions.append(prediction_record)
            
            response = {
                "sentiment": sentiment,
                "confidence": round(confidence, 4),
                "prediction_id": f"quick_{self._prediction_count}",
                "processing_time": round(processing_time, 4),
                "input_text": text[:100] + "..." if len(text) > 100 else text,
                "model_type": "Quick word-based analysis"
            }
            
            self.send_json_response(response)
            print(f"✅ Quick analysis: '{text[:30]}...' → {sentiment} ({confidence:.2f})")
            
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
    <title>🚀 Quick Sentiment Analysis</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); min-height: 100vh; }
        .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        h1 { color: #333; text-align: center; margin-bottom: 30px; font-size: 2.5em; }
        .feature { background: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #28a745; }
        .test-section { background: #fff3cd; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #ffc107; }
        input[type="text"] { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; margin: 10px 0; box-sizing: border-box; }
        button { background: #007acc; color: white; padding: 12px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; transition: background 0.3s; }
        button:hover { background: #005a9e; }
        .result { margin-top: 15px; padding: 15px; border-radius: 5px; font-weight: bold; }
        .positive { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .negative { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .neutral { background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }
        .examples { background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0; }
        .example-btn { background: #6c757d; margin: 5px; padding: 8px 12px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Quick Sentiment Analysis</h1>
        
        <div class="feature">
            <h3>⚡ Features</h3>
            <p>✅ <strong>Instant Startup:</strong> No heavy model loading</p>
            <p>✅ <strong>Fast Analysis:</strong> Results in milliseconds</p>
            <p>✅ <strong>No Dependencies:</strong> Works in any Python environment</p>
            <p>✅ <strong>Word-based Analysis:</strong> Reliable sentiment detection</p>
        </div>

        <div class="test-section">
            <h3>🧪 Test Sentiment Analysis</h3>
            <input type="text" id="textInput" placeholder="Enter text to analyze..." value="I absolutely love this quick system!">
            <button onclick="analyzeText()">🔍 Analyze Sentiment</button>
            
            <div class="examples">
                <h4>📝 Try these examples:</h4>
                <button class="example-btn" onclick="setExample('I love this amazing project!')">Positive Example</button>
                <button class="example-btn" onclick="setExample('This is terrible and disappointing')">Negative Example</button>
                <button class="example-btn" onclick="setExample('The weather is okay today')">Neutral Example</button>
            </div>
            
            <div id="result"></div>
        </div>

        <div class="feature">
            <h3>📊 Analytics</h3>
            <button onclick="getStats()">📈 Get Statistics</button>
            <div id="statsResult"></div>
        </div>
    </div>

    <script>
        function setExample(text) {
            document.getElementById('textInput').value = text;
        }

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
        
        // Allow Enter key to analyze
        document.getElementById('textInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
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

def start_server(port=8090):
    """Start the HTTP server"""
    try:
        server_address = ('127.0.0.1', port)
        httpd = HTTPServer(server_address, QuickAPIHandler)
        
        print("🚀 Quick Sentiment Analysis Server")
        print("=" * 40)
        print(f"⚡ Server running on: http://127.0.0.1:{port}")
        print(f"📚 Documentation: http://127.0.0.1:{port}/docs")
        print(f"📊 Analytics: http://127.0.0.1:{port}/analytics/stats")
        print("✅ Instant startup - no model loading!")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 40)
        
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
