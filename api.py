# api.py

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from input_validation import input_validator
from streaming_api import add_streaming_routes, STREAMING_TEST_HTML
from classifiers.text_classifier import TextClassifier
from classifiers.audio_classifier import AudioClassifier
from classifiers.video_classifier import VideoClassifier
from fusion.fusion_engine import FusionEngine
from enhanced_logging import EnhancedSentimentLogger
import os
import yaml
import time

app = FastAPI()

# Enable CORS for frontend (Allow all for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security middleware
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    """Basic security middleware"""
    # Add security headers
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# Load config with environment variable support
from config_loader import get_config_loader

config_loader = get_config_loader()
config = config_loader.get_config()

# Print configuration summary for debugging
if os.getenv('DEBUG', 'false').lower() == 'true':
    config_loader.print_config_summary()

# Load models
text_model = TextClassifier()
audio_model = AudioClassifier()
video_model = VideoClassifier()
fusion = FusionEngine()

# Initialize enhanced logger
sentiment_logger = EnhancedSentimentLogger()

# Request model for text
class TextInput(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Multimodal Sentiment Classifier API is running."}

# Import the enhanced dashboard HTML
from multimodal_dashboard import MULTIMODAL_DASHBOARD_HTML

# Serve the enhanced multimodal dashboard
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    """Serve the enhanced multimodal dashboard"""
    return HTMLResponse(content=MULTIMODAL_DASHBOARD_HTML)

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

# Analytics endpoint
@app.get("/analytics")
def get_analytics():
    """Get system analytics"""
    try:
        from enhanced_logging import EnhancedSentimentLogger
        logger = EnhancedSentimentLogger()
        analytics = logger.get_analytics()
        return analytics
    except Exception as e:
        return {"error": f"Analytics not available: {str(e)}"}

@app.post("/predict/text")
def predict_text(data: TextInput):
    if not config["models"]["text"]["enabled"]:
        return {"error": "Text model disabled in config"}

    # Validate and sanitize input text
    try:
        sanitized_text = input_validator.validate_text_input(data.text)
    except HTTPException as e:
        raise e

    start_time = time.time()
    sentiment, score = text_model.predict(sanitized_text)
    processing_time = time.time() - start_time

    # Log the prediction
    prediction_id = sentiment_logger.log_prediction(
        mode="text",
        result={"sentiment": sentiment, "confidence": score},
        confidence=score,
        input_content=sanitized_text,
        processing_time=processing_time * 1000  # Convert to milliseconds
    )

    return {
        "sentiment": sentiment,
        "confidence": score,
        "prediction_id": prediction_id,
        "processing_time": processing_time
    }

@app.post("/predict/audio")
async def predict_audio(file: UploadFile = File(...)):
    if not config["models"]["audio"]["enabled"]:
        return {"error": "Audio model disabled in config"}

    # Validate uploaded file
    try:
        file_info = input_validator.validate_file_upload(file, "audio")
    except HTTPException as e:
        raise e

    start_time = time.time()
    contents = await file.read()
    safe_filename = input_validator.sanitize_filename(file.filename)
    temp_path = f"temp_{safe_filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    sentiment, score = audio_model.predict(temp_path)
    processing_time = time.time() - start_time
    os.remove(temp_path)

    # Log the prediction
    prediction_id = sentiment_logger.log_prediction(
        mode="audio",
        result={"sentiment": sentiment, "confidence": score},
        confidence=score,
        input_data={"file_size": len(contents), "filename": file.filename},
        processing_time=processing_time * 1000  # Convert to milliseconds
    )

    return {
        "sentiment": sentiment,
        "confidence": score,
        "prediction_id": prediction_id,
        "processing_time": processing_time
    }

@app.post("/predict/video")
async def predict_video(file: UploadFile = File(...)):
    if not config["models"]["video"]["enabled"]:
        return {"error": "Video model disabled in config"}

    # Validate uploaded file
    try:
        file_info = input_validator.validate_file_upload(file, "video")
    except HTTPException as e:
        raise e

    start_time = time.time()
    contents = await file.read()
    safe_filename = input_validator.sanitize_filename(file.filename)
    temp_path = f"temp_{safe_filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    sentiment, score = video_model.predict(temp_path)
    processing_time = time.time() - start_time
    os.remove(temp_path)

    # Log the prediction
    prediction_id = sentiment_logger.log_prediction(
        mode="video",
        result={"sentiment": sentiment, "confidence": score},
        confidence=score,
        input_data={"file_size": len(contents), "filename": file.filename},
        processing_time=processing_time * 1000  # Convert to milliseconds
    )

    return {
        "sentiment": sentiment,
        "confidence": score,
        "prediction_id": prediction_id,
        "processing_time": processing_time
    }

@app.post("/predict/multimodal")
async def predict_multimodal(file: UploadFile = File(...)):
    # Validate uploaded file (try video first, then audio)
    try:
        file_info = input_validator.validate_file_upload(file, "video")
    except HTTPException:
        try:
            file_info = input_validator.validate_file_upload(file, "audio")
        except HTTPException as e:
            raise HTTPException(status_code=400, detail="File must be a valid audio or video file")

    start_time = time.time()
    results = []
    modalities = []

    contents = await file.read()
    safe_filename = input_validator.sanitize_filename(file.filename)
    temp_path = f"temp_{safe_filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    # Process each enabled modality
    if config["models"]["text"]["enabled"]:
        sentiment, score = text_model.predict("This is a great example!")  # dummy input for now
        results.append((sentiment, score))
        modalities.append("text")

    if config["models"]["audio"]["enabled"]:
        sentiment, score = audio_model.predict(temp_path)
        results.append((sentiment, score))
        modalities.append("audio")

    if config["models"]["video"]["enabled"]:
        sentiment, score = video_model.predict(temp_path)
        results.append((sentiment, score))
        modalities.append("video")

    os.remove(temp_path)
    processing_time = time.time() - start_time

    # Use enhanced fusion with modality information
    final_sentiment, final_confidence = fusion.predict(results, modalities)

    # Prepare individual results for response
    individual_results = [
        {"modality": modalities[i], "sentiment": results[i][0], "confidence": results[i][1]}
        for i in range(len(results))
    ]

    # Log the multimodal prediction
    prediction_id = sentiment_logger.log_prediction(
        mode="multimodal",
        result={
            "sentiment": final_sentiment,
            "confidence": final_confidence,
            "individual_results": individual_results
        },
        confidence=final_confidence,
        input_data={"filename": file.filename, "modalities": modalities},
        processing_time=processing_time * 1000  # Convert to milliseconds
    )

    return {
        "fused_sentiment": final_sentiment,
        "confidence": final_confidence,
        "individual": individual_results,
        "prediction_id": prediction_id,
        "processing_time": processing_time
    }

# Logging and Analytics Endpoints
@app.get("/analytics/stats")
def get_analytics():
    """Get prediction statistics"""
    try:
        return sentiment_logger.get_analytics()
    except Exception as e:
        return {"error": f"Analytics not available: {str(e)}"}

@app.get("/analytics/predictions")
def get_predictions(limit: int = 50, mode: str = None, sentiment: str = None):
    """Get recent predictions with optional filtering"""
    try:
        # Basic implementation - return recent predictions
        return {"message": "Predictions endpoint available", "limit": limit, "mode": mode, "sentiment": sentiment}
    except Exception as e:
        return {"error": f"Predictions not available: {str(e)}"}

@app.post("/analytics/session/start")
def start_session(user_id: str = None):
    """Start a new logging session"""
    try:
        import uuid
        session_id = str(uuid.uuid4())
        return {"session_id": session_id, "user_id": user_id}
    except Exception as e:
        return {"error": f"Session start failed: {str(e)}"}

@app.post("/analytics/session/{session_id}/end")
def end_session(session_id: str):
    """End a logging session"""
    try:
        return {"message": "Session ended", "session_id": session_id}
    except Exception as e:
        return {"error": f"Session end failed: {str(e)}"}

# Performance benchmarking endpoint
@app.get("/benchmark/run")
def run_performance_benchmark():
    """Run performance benchmark"""
    try:
        from model_performance_report import ModelPerformanceBenchmark
        benchmark = ModelPerformanceBenchmark(api_url="http://localhost:8000")
        results = benchmark.run_comprehensive_benchmark()
        return results
    except Exception as e:
        return {"error": f"Benchmark failed: {str(e)}"}

# Streaming test page
@app.get("/streaming/test", response_class=HTMLResponse)
def get_streaming_test():
    """Serve streaming test page"""
    return HTMLResponse(content=STREAMING_TEST_HTML)

# Add streaming routes
add_streaming_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)