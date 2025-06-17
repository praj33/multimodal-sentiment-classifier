# demo_server.py - Simple demo server for dashboard

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
import os
import time
import random

app = FastAPI(title="Multimodal Sentiment Analysis Demo")

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

@app.get("/")
def root():
    return {"message": "Multimodal Sentiment Classifier API is running."}

# Serve the web dashboard
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    """Serve the web dashboard"""
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        error_html = f"""
        <html>
        <head><title>Dashboard Error</title></head>
        <body>
            <h1>Dashboard Error</h1>
            <p>Error: {str(e)}</p>
            <p>Current directory: {os.getcwd()}</p>
            <p>Frontend exists: {os.path.exists('frontend')}</p>
            <p>HTML exists: {os.path.exists('frontend/index.html')}</p>
        </body>
        </html>
        """
        return HTMLResponse(content=error_html)

# Serve static files (CSS, JS)
@app.get("/frontend/{file_path}")
def get_static_file(file_path: str):
    """Serve static frontend files"""
    file_location = f"frontend/{file_path}"
    if os.path.exists(file_location):
        return FileResponse(file_location)
    else:
        return {"error": "File not found"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

# Mock prediction endpoints for demo
@app.post("/predict/text")
def predict_text(data: TextInput):
    """Mock text sentiment prediction"""
    time.sleep(0.1)  # Simulate processing time
    
    # Simple sentiment analysis based on keywords
    text = data.text.lower()
    if any(word in text for word in ['love', 'great', 'amazing', 'excellent', 'fantastic', 'wonderful']):
        sentiment = "positive"
        confidence = random.uniform(0.8, 0.95)
    elif any(word in text for word in ['hate', 'terrible', 'awful', 'bad', 'horrible', 'worst']):
        sentiment = "negative"
        confidence = random.uniform(0.8, 0.95)
    else:
        sentiment = "neutral"
        confidence = random.uniform(0.6, 0.8)
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "processing_time": 0.1,
        "prediction_id": f"demo_{int(time.time())}"
    }

@app.post("/predict/audio")
async def predict_audio(file: UploadFile = File(...)):
    """Mock audio sentiment prediction"""
    time.sleep(0.5)  # Simulate processing time
    
    # Random sentiment for demo
    sentiments = ["positive", "negative", "neutral"]
    sentiment = random.choice(sentiments)
    confidence = random.uniform(0.7, 0.9)
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "processing_time": 0.5,
        "prediction_id": f"demo_audio_{int(time.time())}"
    }

@app.post("/predict/video")
async def predict_video(file: UploadFile = File(...)):
    """Mock video sentiment prediction"""
    time.sleep(0.3)  # Simulate processing time
    
    # Random sentiment for demo
    sentiments = ["positive", "negative", "neutral"]
    sentiment = random.choice(sentiments)
    confidence = random.uniform(0.7, 0.9)
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "processing_time": 0.3,
        "prediction_id": f"demo_video_{int(time.time())}"
    }

@app.post("/predict/multimodal")
async def predict_multimodal(file: UploadFile = File(...)):
    """Mock multimodal sentiment prediction"""
    time.sleep(0.8)  # Simulate processing time
    
    # Generate individual results
    individual_results = [
        {"modality": "text", "sentiment": "positive", "confidence": 0.85},
        {"modality": "audio", "sentiment": "neutral", "confidence": 0.72},
        {"modality": "video", "sentiment": "positive", "confidence": 0.78}
    ]
    
    # Fused result
    fused_sentiment = "positive"
    fused_confidence = 0.82
    
    return {
        "fused_sentiment": fused_sentiment,
        "confidence": fused_confidence,
        "individual": individual_results,
        "processing_time": 0.8,
        "prediction_id": f"demo_multimodal_{int(time.time())}"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Demo Server...")
    print("📊 Dashboard will be available at: http://localhost:8000/dashboard")
    print("📚 API docs will be available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
