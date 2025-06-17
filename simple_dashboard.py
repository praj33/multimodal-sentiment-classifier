# simple_dashboard.py - Simple working dashboard

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import random
import time

app = FastAPI(title="Multimodal Sentiment Analysis Dashboard")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

# Embedded HTML Dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔍 AI Sentiment Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-blue-100 to-purple-100 min-h-screen p-4">
    <div class="max-w-2xl mx-auto bg-white rounded-2xl shadow-xl p-8">
        <h1 class="text-3xl font-bold text-center text-blue-600 mb-8">🔍 AI Sentiment Analyzer</h1>
        
        <!-- Text Input -->
        <div class="mb-6">
            <label class="block text-sm font-semibold mb-2">Enter Text for Analysis:</label>
            <textarea id="textInput" class="w-full p-3 border rounded-lg" rows="4" 
                placeholder="e.g., I love this amazing product!"></textarea>
        </div>
        
        <!-- Analyze Button -->
        <button onclick="analyzeText()" 
            class="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold mb-6">
            🚀 Analyze Sentiment
        </button>
        
        <!-- Results -->
        <div id="results" class="bg-gray-100 p-4 rounded-lg hidden">
            <h3 class="font-semibold mb-2">Results:</h3>
            <div id="resultContent"></div>
        </div>
        
        <!-- Loading -->
        <div id="loading" class="text-center hidden">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p class="mt-2">Analyzing...</p>
        </div>
    </div>

    <script>
        async function analyzeText() {
            const text = document.getElementById('textInput').value.trim();
            if (!text) {
                alert('Please enter some text!');
                return;
            }
            
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const resultContent = document.getElementById('resultContent');
            
            // Show loading
            loading.classList.remove('hidden');
            results.classList.add('hidden');
            
            try {
                const response = await fetch('/predict/text', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text})
                });
                
                const data = await response.json();
                
                // Hide loading
                loading.classList.add('hidden');
                
                // Show results
                const emoji = data.sentiment === 'positive' ? '😊' : 
                             data.sentiment === 'negative' ? '😞' : '😐';
                const color = data.sentiment === 'positive' ? 'text-green-600' : 
                             data.sentiment === 'negative' ? 'text-red-600' : 'text-gray-600';
                
                resultContent.innerHTML = `
                    <div class="text-xl font-bold ${color}">
                        ${emoji} ${data.sentiment.toUpperCase()}
                    </div>
                    <div class="text-sm mt-2">
                        Confidence: ${(data.confidence * 100).toFixed(1)}%
                    </div>
                    <div class="w-full bg-gray-300 rounded-full h-2 mt-2">
                        <div class="bg-blue-600 h-2 rounded-full" style="width: ${data.confidence * 100}%"></div>
                    </div>
                `;
                
                results.classList.remove('hidden');
                
            } catch (error) {
                loading.classList.add('hidden');
                alert('Error: ' + error.message);
            }
        }
        
        // Allow Enter key to submit
        document.getElementById('textInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                analyzeText();
            }
        });
    </script>
</body>
</html>
"""

@app.get("/")
def root():
    return {"message": "Multimodal Sentiment Analysis API", "dashboard": "/dashboard"}

@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    """Serve the embedded dashboard"""
    return HTMLResponse(content=DASHBOARD_HTML)

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.post("/predict/text")
def predict_text(data: TextInput):
    """Predict sentiment from text"""
    time.sleep(0.1)  # Simulate processing
    
    text = data.text.lower()
    
    # Simple keyword-based sentiment analysis
    positive_words = ['love', 'great', 'amazing', 'excellent', 'fantastic', 'wonderful', 'awesome', 'good']
    negative_words = ['hate', 'terrible', 'awful', 'bad', 'horrible', 'worst', 'disgusting', 'disappointing']
    
    positive_score = sum(1 for word in positive_words if word in text)
    negative_score = sum(1 for word in negative_words if word in text)
    
    if positive_score > negative_score:
        sentiment = "positive"
        confidence = min(0.95, 0.7 + (positive_score * 0.1))
    elif negative_score > positive_score:
        sentiment = "negative"
        confidence = min(0.95, 0.7 + (negative_score * 0.1))
    else:
        sentiment = "neutral"
        confidence = random.uniform(0.6, 0.8)
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "processing_time": 0.1,
        "text_length": len(data.text),
        "prediction_id": f"demo_{int(time.time())}"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple Dashboard Server...")
    print("📊 Dashboard: http://localhost:8000/dashboard")
    print("📚 API docs: http://localhost:8000/docs")
    print("🔍 Health: http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000)
