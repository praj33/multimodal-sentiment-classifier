#!/usr/bin/env python3
"""
Simple HTTP server to test if the issue is with uvicorn
"""

import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class SentimentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "message": "Multimodal Sentiment Analysis API",
                "status": "running",
                "timestamp": time.time(),
                "endpoints": {
                    "health": "/health",
                    "predict": "/predict?text=your_text_here"
                }
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif parsed_path.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "timestamp": time.time(),
                "server": "simple_http_server"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif parsed_path.path == '/predict':
            query_params = parse_qs(parsed_path.query)
            text = query_params.get('text', [''])[0]
            
            if text:
                # Simple sentiment analysis (mock)
                sentiment = "positive" if any(word in text.lower() for word in ['good', 'great', 'love', 'excellent', 'amazing']) else \
                           "negative" if any(word in text.lower() for word in ['bad', 'hate', 'terrible', 'awful', 'horrible']) else \
                           "neutral"
                
                confidence = 0.85 if sentiment != "neutral" else 0.5
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "text": text,
                    "sentiment": sentiment,
                    "confidence": confidence,
                    "timestamp": time.time(),
                    "server": "simple_http_server"
                }
                self.wfile.write(json.dumps(response, indent=2).encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": "Missing 'text' parameter"}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/predict':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                text = data.get('text', '')
                
                if text:
                    # Simple sentiment analysis (mock)
                    sentiment = "positive" if any(word in text.lower() for word in ['good', 'great', 'love', 'excellent', 'amazing']) else \
                               "negative" if any(word in text.lower() for word in ['bad', 'hate', 'terrible', 'awful', 'horrible']) else \
                               "neutral"
                    
                    confidence = 0.85 if sentiment != "neutral" else 0.5
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        "text": text,
                        "sentiment": sentiment,
                        "confidence": confidence,
                        "timestamp": time.time(),
                        "server": "simple_http_server"
                    }
                    self.wfile.write(json.dumps(response, indent=2).encode())
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {"error": "Missing 'text' field in JSON"}
                    self.wfile.write(json.dumps(response).encode())
                    
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": "Invalid JSON"}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode())

def run_server():
    """Run the simple HTTP server"""
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, SentimentHandler)
    
    print("🚀 Simple HTTP Server Starting...")
    print(f"🌐 Server running at: http://127.0.0.1:8000")
    print("📚 Endpoints:")
    print("   GET  /           - API info")
    print("   GET  /health     - Health check")
    print("   GET  /predict?text=hello - Simple prediction")
    print("   POST /predict    - JSON prediction")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
