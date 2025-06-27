#!/usr/bin/env python3
"""
Minimal API version with lazy loading to test server startup
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import os

# Create FastAPI app
app = FastAPI(
    title="Multimodal Sentiment Analysis API (Minimal)",
    description="Minimal version for testing server startup",
    version="1.0.0"
)

# Global variables for lazy loading
text_model = None
audio_model = None
video_model = None
fusion_engine = None

class TextInput(BaseModel):
    text: str

def load_models():
    """Load models lazily when first needed"""
    global text_model, audio_model, video_model, fusion_engine
    
    if text_model is None:
        print("🧠 Loading text classifier...")
        from classifiers.text_classifier import TextClassifier
        text_model = TextClassifier()
        print("✅ Text classifier loaded")
    
    if audio_model is None:
        print("🎵 Loading audio classifier...")
        from classifiers.audio_classifier import AudioClassifier
        audio_model = AudioClassifier()
        print("✅ Audio classifier loaded")
    
    if video_model is None:
        print("🎥 Loading video classifier...")
        from classifiers.video_classifier import VideoClassifier
        video_model = VideoClassifier()
        print("✅ Video classifier loaded")
    
    if fusion_engine is None:
        print("⚡ Loading fusion engine...")
        from fusion.fusion_engine import FusionEngine
        fusion_engine = FusionEngine()
        print("✅ Fusion engine loaded")

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Multimodal Sentiment Analysis API (Minimal)",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "text_prediction": "/predict/text"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "models_loaded": {
            "text": text_model is not None,
            "audio": audio_model is not None,
            "video": video_model is not None,
            "fusion": fusion_engine is not None
        }
    }

@app.post("/predict/text")
def predict_text_minimal(data: TextInput):
    """Minimal text sentiment prediction"""
    try:
        # Load models if not already loaded
        load_models()
        
        # Simple prediction
        result = text_model.predict(data.text)
        
        if isinstance(result, dict):
            return {
                "sentiment": result.get('sentiment', 'neutral'),
                "confidence": result.get('confidence', 0.5),
                "text": data.text,
                "status": "success"
            }
        else:
            sentiment, confidence = result
            return {
                "sentiment": sentiment,
                "confidence": confidence,
                "text": data.text,
                "status": "success"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/load-models")
def load_all_models():
    """Endpoint to manually load all models"""
    try:
        start_time = time.time()
        load_models()
        load_time = time.time() - start_time
        
        return {
            "status": "success",
            "message": "All models loaded successfully",
            "load_time_seconds": round(load_time, 2),
            "models": {
                "text": "loaded",
                "audio": "loaded", 
                "video": "loaded",
                "fusion": "loaded"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model loading failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting minimal API server...")
    print("🌐 Server will be available at: http://localhost:8001")
    print("📚 API Documentation: http://localhost:8001/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001)
