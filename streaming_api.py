# streaming_api.py - Streaming mode implementation for real-time analysis

import asyncio
import json
import time
from typing import AsyncGenerator, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
import logging

class StreamingProcessor:
    """Real-time streaming sentiment analysis processor"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.processing_queue = asyncio.Queue()
        self.logger = logging.getLogger(__name__)
    
    async def connect_websocket(self, websocket: WebSocket, client_id: str):
        """Connect a new WebSocket client"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.logger.info(f"Client {client_id} connected")
    
    def disconnect_websocket(self, client_id: str):
        """Disconnect a WebSocket client"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            self.logger.info(f"Client {client_id} disconnected")
    
    async def broadcast_result(self, result: Dict[str, Any]):
        """Broadcast result to all connected clients"""
        message = json.dumps(result)
        disconnected_clients = []
        
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(message)
            except:
                disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect_websocket(client_id)
    
    async def stream_text_analysis(self, text: str) -> AsyncGenerator[str, None]:
        """Stream text analysis results in chunks"""
        # Simulate streaming analysis by processing text in chunks
        words = text.split()
        chunk_size = max(1, len(words) // 10)  # Process in 10 chunks
        
        accumulated_text = ""
        
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            accumulated_text += " " + chunk if accumulated_text else chunk
            
            # Simulate processing time
            await asyncio.sleep(0.1)
            
            # Analyze accumulated text
            try:
                from classifiers.text_classifier import TextClassifier
                classifier = TextClassifier()
                sentiment, confidence = classifier.predict(accumulated_text)
                
                result = {
                    "type": "partial_result",
                    "text_processed": accumulated_text,
                    "sentiment": sentiment,
                    "confidence": confidence,
                    "progress": min(100, (i + chunk_size) / len(words) * 100),
                    "timestamp": time.time()
                }
                
                yield f"data: {json.dumps(result)}\n\n"
                
            except Exception as e:
                error_result = {
                    "type": "error",
                    "message": str(e),
                    "timestamp": time.time()
                }
                yield f"data: {json.dumps(error_result)}\n\n"
        
        # Final result
        final_result = {
            "type": "final_result",
            "text": accumulated_text,
            "sentiment": sentiment,
            "confidence": confidence,
            "progress": 100,
            "timestamp": time.time()
        }
        yield f"data: {json.dumps(final_result)}\n\n"
    
    async def stream_audio_analysis(self, audio_chunks: AsyncGenerator[bytes, None]) -> AsyncGenerator[str, None]:
        """Stream audio analysis results as audio is received"""
        accumulated_audio = b""
        chunk_count = 0
        
        async for chunk in audio_chunks:
            accumulated_audio += chunk
            chunk_count += 1
            
            # Process every 10 chunks or when we have enough data
            if chunk_count % 10 == 0 or len(accumulated_audio) > 1024 * 1024:  # 1MB
                try:
                    # Simulate audio processing
                    await asyncio.sleep(0.2)
                    
                    # Mock analysis result
                    import random
                    sentiments = ["positive", "negative", "neutral"]
                    sentiment = random.choice(sentiments)
                    confidence = random.uniform(0.6, 0.9)
                    
                    result = {
                        "type": "partial_audio_result",
                        "sentiment": sentiment,
                        "confidence": confidence,
                        "audio_duration_ms": chunk_count * 100,  # Estimate
                        "timestamp": time.time()
                    }
                    
                    yield f"data: {json.dumps(result)}\n\n"
                    
                except Exception as e:
                    error_result = {
                        "type": "error",
                        "message": str(e),
                        "timestamp": time.time()
                    }
                    yield f"data: {json.dumps(error_result)}\n\n"
        
        # Final audio result
        final_result = {
            "type": "final_audio_result",
            "sentiment": sentiment,
            "confidence": confidence,
            "total_duration_ms": chunk_count * 100,
            "timestamp": time.time()
        }
        yield f"data: {json.dumps(final_result)}\n\n"
    
    async def process_real_time_text(self, websocket: WebSocket, client_id: str):
        """Process real-time text input via WebSocket"""
        try:
            while True:
                # Receive text from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                if message.get("type") == "text_input":
                    text = message.get("text", "")
                    
                    if text:
                        # Process text
                        try:
                            from classifiers.text_classifier import TextClassifier
                            classifier = TextClassifier()
                            sentiment, confidence = classifier.predict(text)
                            
                            result = {
                                "type": "text_result",
                                "client_id": client_id,
                                "text": text,
                                "sentiment": sentiment,
                                "confidence": confidence,
                                "timestamp": time.time()
                            }
                            
                            # Send result back to client
                            await websocket.send_text(json.dumps(result))
                            
                        except Exception as e:
                            error_result = {
                                "type": "error",
                                "message": str(e),
                                "timestamp": time.time()
                            }
                            await websocket.send_text(json.dumps(error_result))
                
                elif message.get("type") == "ping":
                    # Respond to ping
                    pong_result = {
                        "type": "pong",
                        "timestamp": time.time()
                    }
                    await websocket.send_text(json.dumps(pong_result))
                    
        except WebSocketDisconnect:
            self.disconnect_websocket(client_id)
        except Exception as e:
            self.logger.error(f"Error in real-time processing for {client_id}: {e}")
            self.disconnect_websocket(client_id)

# Global streaming processor
streaming_processor = StreamingProcessor()

# FastAPI routes for streaming
def add_streaming_routes(app: FastAPI):
    """Add streaming routes to FastAPI app"""
    
    @app.get("/stream/text")
    async def stream_text_sentiment(text: str):
        """Stream text sentiment analysis"""
        if not text:
            return {"error": "No text provided"}
        
        return StreamingResponse(
            streaming_processor.stream_text_analysis(text),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Cache-Control"
            }
        )
    
    @app.websocket("/ws/realtime/{client_id}")
    async def websocket_realtime(websocket: WebSocket, client_id: str):
        """WebSocket endpoint for real-time sentiment analysis"""
        await streaming_processor.connect_websocket(websocket, client_id)
        await streaming_processor.process_real_time_text(websocket, client_id)
    
    @app.get("/stream/status")
    async def streaming_status():
        """Get streaming service status"""
        return {
            "active_connections": len(streaming_processor.active_connections),
            "connected_clients": list(streaming_processor.active_connections.keys()),
            "queue_size": streaming_processor.processing_queue.qsize(),
            "status": "active"
        }

# HTML client for testing streaming
STREAMING_TEST_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Streaming Sentiment Analysis Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .input-section { margin-bottom: 20px; }
        .results { border: 1px solid #ccc; padding: 10px; height: 300px; overflow-y: auto; }
        .result-item { margin: 5px 0; padding: 5px; border-radius: 3px; }
        .positive { background-color: #d4edda; }
        .negative { background-color: #f8d7da; }
        .neutral { background-color: #e2e3e5; }
        button { padding: 10px 20px; margin: 5px; }
        input[type="text"] { width: 300px; padding: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎭 Streaming Sentiment Analysis Test</h1>
        
        <div class="input-section">
            <h3>Real-time Text Analysis</h3>
            <input type="text" id="textInput" placeholder="Type text for real-time analysis...">
            <button onclick="connectWebSocket()">Connect</button>
            <button onclick="disconnectWebSocket()">Disconnect</button>
            <button onclick="sendText()">Send Text</button>
        </div>
        
        <div class="input-section">
            <h3>Streaming Text Analysis</h3>
            <input type="text" id="streamText" placeholder="Enter text for streaming analysis...">
            <button onclick="startStreaming()">Start Streaming</button>
        </div>
        
        <div class="results" id="results">
            <p>Results will appear here...</p>
        </div>
    </div>

    <script>
        let ws = null;
        let clientId = 'client_' + Math.random().toString(36).substr(2, 9);
        
        function addResult(result) {
            const resultsDiv = document.getElementById('results');
            const resultItem = document.createElement('div');
            resultItem.className = 'result-item ' + (result.sentiment || 'neutral');
            resultItem.innerHTML = `
                <strong>${result.type}:</strong> 
                ${result.sentiment || 'N/A'} 
                (${((result.confidence || 0) * 100).toFixed(1)}%) 
                - ${new Date(result.timestamp * 1000).toLocaleTimeString()}
                ${result.text ? '<br>Text: ' + result.text : ''}
            `;
            resultsDiv.appendChild(resultItem);
            resultsDiv.scrollTop = resultsDiv.scrollHeight;
        }
        
        function connectWebSocket() {
            if (ws) {
                ws.close();
            }
            
            ws = new WebSocket(`ws://localhost:8000/ws/realtime/${clientId}`);
            
            ws.onopen = function() {
                addResult({type: 'Connected', timestamp: Date.now() / 1000});
            };
            
            ws.onmessage = function(event) {
                const result = JSON.parse(event.data);
                addResult(result);
            };
            
            ws.onclose = function() {
                addResult({type: 'Disconnected', timestamp: Date.now() / 1000});
            };
        }
        
        function disconnectWebSocket() {
            if (ws) {
                ws.close();
                ws = null;
            }
        }
        
        function sendText() {
            const text = document.getElementById('textInput').value;
            if (ws && text) {
                ws.send(JSON.stringify({
                    type: 'text_input',
                    text: text
                }));
                document.getElementById('textInput').value = '';
            }
        }
        
        function startStreaming() {
            const text = document.getElementById('streamText').value;
            if (text) {
                const eventSource = new EventSource(`/stream/text?text=${encodeURIComponent(text)}`);
                
                eventSource.onmessage = function(event) {
                    const result = JSON.parse(event.data);
                    addResult(result);
                    
                    if (result.type === 'final_result') {
                        eventSource.close();
                    }
                };
                
                eventSource.onerror = function() {
                    addResult({type: 'Streaming Error', timestamp: Date.now() / 1000});
                    eventSource.close();
                };
            }
        }
        
        // Auto-connect on page load
        window.onload = function() {
            connectWebSocket();
        };
        
        // Send text on Enter key
        document.getElementById('textInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendText();
            }
        });
    </script>
</body>
</html>
"""
