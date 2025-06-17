# multimodal_dashboard.py - Complete multimodal dashboard with audio/video support

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import random
import time
import os

app = FastAPI(title="Complete Multimodal Sentiment Analysis Dashboard")

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

# Enhanced HTML Dashboard with Audio/Video Support
MULTIMODAL_DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎭 Multimodal AI Sentiment Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class'
        }
    </script>
    <style>
        /* Ensure emoji display properly */
        .emoji {
            font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", "Android Emoji", "EmojiSymbols", sans-serif;
            font-size: 1.5em;
            display: inline-block;
            vertical-align: middle;
        }

        /* Fix emoji in buttons and text */
        button .emoji, span .emoji {
            font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", "Android Emoji", "EmojiSymbols", sans-serif;
        }

        /* Ensure all emojis render properly */
        * {
            font-variant-emoji: emoji;
        }
    </style>
</head>
<body class="bg-gradient-to-br from-blue-100 via-purple-100 to-pink-100 min-h-screen p-4">
    <div class="max-w-4xl mx-auto bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-8">
        <!-- Header -->
        <div class="text-center mb-8">
            <h1 class="text-4xl font-bold mb-2">
                <span class="emoji" style="font-size: 3rem; margin-right: 0.5rem;">🎭</span>
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                    Multimodal AI Sentiment Analyzer
                </span>
            </h1>
            <p class="text-gray-600">Analyze sentiment from Text, Audio, and Video</p>
        </div>
        
        <!-- Mode Selection -->
        <div class="mb-6">
            <label class="block text-sm font-semibold mb-3">Select Analysis Mode:</label>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                <button onclick="setMode('text')" id="btn-text"
                    class="mode-btn bg-blue-500 text-white p-3 rounded-lg font-semibold hover:bg-blue-600 transition">
                    <span class="emoji">📝</span> Text
                </button>
                <button onclick="setMode('audio')" id="btn-audio"
                    class="mode-btn bg-gray-300 text-gray-700 p-3 rounded-lg font-semibold hover:bg-gray-400 transition">
                    <span class="emoji">🎵</span> Audio
                </button>
                <button onclick="setMode('video')" id="btn-video"
                    class="mode-btn bg-gray-300 text-gray-700 p-3 rounded-lg font-semibold hover:bg-gray-400 transition">
                    <span class="emoji">🎥</span> Video
                </button>
                <button onclick="setMode('multimodal')" id="btn-multimodal"
                    class="mode-btn bg-gray-300 text-gray-700 p-3 rounded-lg font-semibold hover:bg-gray-400 transition">
                    <span class="emoji">🎭</span> Multi
                </button>
            </div>
        </div>
        
        <!-- Text Input Section -->
        <div id="text-section" class="mb-6">
            <label class="block text-sm font-semibold mb-2">Enter Text for Analysis:</label>
            <textarea id="textInput" class="w-full p-4 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none" 
                rows="4" placeholder="e.g., I absolutely love this amazing product!"></textarea>
        </div>
        
        <!-- File Upload Section -->
        <div id="file-section" class="mb-6 hidden">
            <label class="block text-sm font-semibold mb-2">Upload File:</label>
            <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-500 transition">
                <input type="file" id="fileInput" class="hidden" accept="" onchange="handleFileSelect(event)">
                <div id="upload-area" onclick="document.getElementById('fileInput').click()" class="cursor-pointer">
                    <div class="text-4xl mb-2">📁</div>
                    <p class="text-gray-600 mb-2">Click to upload or drag & drop</p>
                    <p id="file-types" class="text-sm text-gray-500">Supported: .mp3, .wav, .mp4, .avi</p>
                </div>
                <div id="file-info" class="hidden mt-4 p-3 bg-gray-100 rounded">
                    <p id="file-name" class="font-semibold"></p>
                    <p id="file-size" class="text-sm text-gray-600"></p>
                </div>
            </div>
        </div>
        
        <!-- Analyze Button -->
        <button onclick="analyzeContent()" id="analyzeBtn"
            class="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-4 rounded-lg font-semibold text-lg transition transform hover:scale-105 mb-6">
            🚀 Analyze Sentiment
        </button>
        
        <!-- Loading -->
        <div id="loading" class="text-center hidden mb-6">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-3"></div>
            <p class="text-gray-600">Analyzing content...</p>
        </div>
        
        <!-- Results Section -->
        <div id="results" class="bg-gradient-to-r from-gray-50 to-gray-100 p-6 rounded-xl hidden">
            <h3 class="text-xl font-bold mb-4">📊 Analysis Results</h3>
            <div id="resultContent"></div>
        </div>
        
        <!-- Sample Files Section -->
        <div class="mt-8 p-4 bg-blue-50 rounded-lg">
            <h4 class="font-semibold text-blue-800 mb-2">💡 Quick Test Examples:</h4>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-2 text-sm">
                <button onclick="quickTest('I love this amazing product!')" 
                    class="text-left p-2 bg-white rounded hover:bg-blue-100 transition">
                    😊 "I love this amazing product!"
                </button>
                <button onclick="quickTest('This is terrible and awful!')" 
                    class="text-left p-2 bg-white rounded hover:bg-blue-100 transition">
                    😞 "This is terrible and awful!"
                </button>
                <button onclick="quickTest('The weather is cloudy today.')" 
                    class="text-left p-2 bg-white rounded hover:bg-blue-100 transition">
                    😐 "The weather is cloudy today."
                </button>
            </div>
        </div>
    </div>

    <script>
        let currentMode = 'text';
        let selectedFile = null;
        
        function setMode(mode) {
            currentMode = mode;
            
            // Update button styles
            document.querySelectorAll('.mode-btn').forEach(btn => {
                btn.className = 'mode-btn bg-gray-300 text-gray-700 p-3 rounded-lg font-semibold hover:bg-gray-400 transition';
            });
            document.getElementById(`btn-${mode}`).className = 'mode-btn bg-blue-500 text-white p-3 rounded-lg font-semibold hover:bg-blue-600 transition';
            
            // Show/hide sections
            const textSection = document.getElementById('text-section');
            const fileSection = document.getElementById('file-section');
            const fileTypes = document.getElementById('file-types');
            const fileInput = document.getElementById('fileInput');
            
            if (mode === 'text') {
                textSection.classList.remove('hidden');
                fileSection.classList.add('hidden');
            } else {
                textSection.classList.add('hidden');
                fileSection.classList.remove('hidden');
                
                // Update file types based on mode
                if (mode === 'audio') {
                    fileTypes.textContent = 'Supported: .mp3, .wav, .m4a, .ogg';
                    fileInput.accept = '.mp3,.wav,.m4a,.ogg,audio/*';
                } else if (mode === 'video') {
                    fileTypes.textContent = 'Supported: .mp4, .avi, .mov, .wmv';
                    fileInput.accept = '.mp4,.avi,.mov,.wmv,video/*';
                } else if (mode === 'multimodal') {
                    fileTypes.textContent = 'Supported: Audio and Video files';
                    fileInput.accept = '.mp3,.wav,.m4a,.ogg,.mp4,.avi,.mov,.wmv,audio/*,video/*';
                }
            }
        }
        
        function handleFileSelect(event) {
            const file = event.target.files[0];
            if (file) {
                selectedFile = file;
                document.getElementById('file-name').textContent = file.name;
                document.getElementById('file-size').textContent = `Size: ${(file.size / 1024 / 1024).toFixed(2)} MB`;
                document.getElementById('file-info').classList.remove('hidden');
            }
        }
        
        function quickTest(text) {
            setMode('text');
            document.getElementById('textInput').value = text;
            analyzeContent();
        }
        
        async function analyzeContent() {
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const resultContent = document.getElementById('resultContent');
            const analyzeBtn = document.getElementById('analyzeBtn');
            
            // Show loading
            loading.classList.remove('hidden');
            results.classList.add('hidden');
            analyzeBtn.disabled = true;
            analyzeBtn.textContent = '⏳ Analyzing...';
            
            try {
                let response;
                
                if (currentMode === 'text') {
                    const text = document.getElementById('textInput').value.trim();
                    if (!text) {
                        alert('Please enter some text!');
                        return;
                    }
                    
                    response = await fetch('/predict/text', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({text: text})
                    });
                } else {
                    if (!selectedFile) {
                        alert('Please select a file!');
                        return;
                    }
                    
                    const formData = new FormData();
                    formData.append('file', selectedFile);
                    
                    response = await fetch(`/predict/${currentMode}`, {
                        method: 'POST',
                        body: formData
                    });
                }
                
                const data = await response.json();
                
                // Hide loading
                loading.classList.add('hidden');
                analyzeBtn.disabled = false;
                analyzeBtn.textContent = '🚀 Analyze Sentiment';
                
                if (data.error) {
                    resultContent.innerHTML = `<div class="text-red-600 font-semibold">❌ Error: ${data.error}</div>`;
                } else {
                    displayResults(data);
                }
                
                results.classList.remove('hidden');
                
            } catch (error) {
                loading.classList.add('hidden');
                analyzeBtn.disabled = false;
                analyzeBtn.textContent = '🚀 Analyze Sentiment';
                resultContent.innerHTML = `<div class="text-red-600 font-semibold">❌ Error: ${error.message}</div>`;
                results.classList.remove('hidden');
            }
        }
        
        function displayResults(data) {
            const resultContent = document.getElementById('resultContent');

            // Emoji mapping function for better compatibility
            function getEmoji(sentiment) {
                switch(sentiment) {
                    case 'positive': return '😊';
                    case 'negative': return '😞';
                    case 'neutral': return '😐';
                    default: return '😐';
                }
            }

            function getColor(sentiment) {
                switch(sentiment) {
                    case 'positive': return 'text-green-600';
                    case 'negative': return 'text-red-600';
                    case 'neutral': return 'text-gray-600';
                    default: return 'text-gray-600';
                }
            }

            // Handle multimodal results
            if (data.fused_sentiment) {
                const sentiment = data.fused_sentiment;
                const confidence = data.confidence;
                const emoji = getEmoji(sentiment);
                const color = getColor(sentiment);

                let html = `
                    <div class="mb-6">
                        <div class="text-3xl font-bold ${color} mb-3">
                            <span style="font-size: 2rem;">${emoji}</span> ${sentiment.toUpperCase()}
                        </div>
                        <div class="text-lg mb-3">🎭 Multimodal Confidence: ${(confidence * 100).toFixed(1)}%</div>
                        <div class="w-full bg-gray-300 rounded-full h-4 mb-4">
                            <div class="bg-gradient-to-r from-blue-500 to-purple-600 h-4 rounded-full transition-all duration-1000" style="width: ${confidence * 100}%"></div>
                        </div>
                    </div>
                `;

                if (data.individual && data.individual.length > 0) {
                    html += '<div class="border-t pt-4"><h4 class="font-semibold mb-3 text-lg">📊 Individual Modality Results:</h4>';
                    data.individual.forEach(item => {
                        const itemEmoji = getEmoji(item.sentiment);
                        const itemColor = getColor(item.sentiment);
                        html += `
                            <div class="flex justify-between items-center mb-3 p-3 bg-white rounded-lg shadow-sm border">
                                <span class="font-medium ${itemColor}">
                                    <span style="font-size: 1.2rem;">${itemEmoji}</span>
                                    ${item.modality.charAt(0).toUpperCase() + item.modality.slice(1)}: ${item.sentiment.toUpperCase()}
                                </span>
                                <span class="text-sm font-semibold">${(item.confidence * 100).toFixed(1)}%</span>
                            </div>
                        `;
                    });
                    html += '</div>';
                }

                resultContent.innerHTML = html;
            } else {
                // Handle single modality results
                const sentiment = data.sentiment;
                const confidence = data.confidence;
                const emoji = getEmoji(sentiment);
                const color = getColor(sentiment);

                resultContent.innerHTML = `
                    <div class="text-3xl font-bold ${color} mb-3">
                        <span style="font-size: 2rem;">${emoji}</span> ${sentiment.toUpperCase()}
                    </div>
                    <div class="text-lg mb-3">Confidence: ${(confidence * 100).toFixed(1)}%</div>
                    <div class="w-full bg-gray-300 rounded-full h-4 mb-4">
                        <div class="bg-blue-600 h-4 rounded-full transition-all duration-1000" style="width: ${confidence * 100}%"></div>
                    </div>
                    <div class="text-sm text-gray-600">
                        ⏱️ Processing Time: ${data.processing_time || 0.1}s
                        ${data.text_length ? ` | 📏 Text Length: ${data.text_length} chars` : ''}
                        ${data.file_size ? ` | 📁 File Size: ${(data.file_size / 1024 / 1024).toFixed(2)} MB` : ''}
                    </div>
                `;
            }
        }
        
        // Initialize with text mode
        setMode('text');
    </script>
</body>
</html>
"""

@app.get("/")
def root():
    return {"message": "Complete Multimodal Sentiment Analysis API", "dashboard": "/dashboard"}

@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    """Serve the complete multimodal dashboard"""
    return HTMLResponse(content=MULTIMODAL_DASHBOARD_HTML)

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Multimodal API is running"}

@app.post("/predict/text")
def predict_text(data: TextInput):
    """Predict sentiment from text"""
    time.sleep(0.1)  # Simulate processing
    
    text = data.text.lower()
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
        "prediction_id": f"text_{int(time.time())}"
    }

@app.post("/predict/audio")
async def predict_audio(file: UploadFile = File(...)):
    """Predict sentiment from audio file"""
    time.sleep(0.5)  # Simulate audio processing
    
    # Simulate audio analysis based on file characteristics
    file_size = len(await file.read())
    await file.seek(0)  # Reset file pointer
    
    # Mock analysis based on file size (larger files might have more content)
    if file_size > 1000000:  # > 1MB
        sentiment = random.choice(["positive", "negative"])
        confidence = random.uniform(0.75, 0.9)
    else:
        sentiment = random.choice(["positive", "negative", "neutral"])
        confidence = random.uniform(0.6, 0.85)
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "processing_time": 0.5,
        "file_size": file_size,
        "filename": file.filename,
        "prediction_id": f"audio_{int(time.time())}"
    }

@app.post("/predict/video")
async def predict_video(file: UploadFile = File(...)):
    """Predict sentiment from video file"""
    time.sleep(0.8)  # Simulate video processing
    
    file_size = len(await file.read())
    await file.seek(0)
    
    # Mock video analysis
    sentiments = ["positive", "negative", "neutral"]
    sentiment = random.choice(sentiments)
    confidence = random.uniform(0.7, 0.9)
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "processing_time": 0.8,
        "file_size": file_size,
        "filename": file.filename,
        "prediction_id": f"video_{int(time.time())}"
    }

@app.post("/predict/multimodal")
async def predict_multimodal(file: UploadFile = File(...)):
    """Predict sentiment using multimodal analysis"""
    time.sleep(1.0)  # Simulate complex multimodal processing
    
    file_size = len(await file.read())
    await file.seek(0)
    
    # Generate individual modality results
    individual_results = [
        {"modality": "audio", "sentiment": random.choice(["positive", "negative", "neutral"]), "confidence": random.uniform(0.7, 0.9)},
        {"modality": "visual", "sentiment": random.choice(["positive", "negative", "neutral"]), "confidence": random.uniform(0.7, 0.9)},
        {"modality": "text", "sentiment": random.choice(["positive", "negative", "neutral"]), "confidence": random.uniform(0.7, 0.9)}
    ]
    
    # Simulate fusion - majority vote with confidence weighting
    sentiments = [r["sentiment"] for r in individual_results]
    confidences = [r["confidence"] for r in individual_results]
    
    # Simple majority vote
    sentiment_counts = {s: sentiments.count(s) for s in set(sentiments)}
    fused_sentiment = max(sentiment_counts, key=sentiment_counts.get)
    fused_confidence = sum(confidences) / len(confidences)
    
    return {
        "fused_sentiment": fused_sentiment,
        "confidence": fused_confidence,
        "individual": individual_results,
        "processing_time": 1.0,
        "file_size": file_size,
        "filename": file.filename,
        "prediction_id": f"multimodal_{int(time.time())}"
    }

if __name__ == "__main__":
    import uvicorn
    print("🎭 Starting Complete Multimodal Dashboard...")
    print("📊 Dashboard: http://localhost:8003/dashboard")
    print("📚 API docs: http://localhost:8003/docs")
    uvicorn.run(app, host="0.0.0.0", port=8003)
