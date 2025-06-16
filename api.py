# api.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from classifiers.text_classifier import TextClassifier
from classifiers.audio_classifier import AudioClassifier
from classifiers.video_classifier import VideoClassifier
from fusion.fusion_engine import FusionEngine
from logging_system import sentiment_logger
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

# Load config
def load_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config", "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

config = load_config()

# Load models
text_model = TextClassifier()
audio_model = AudioClassifier()
video_model = VideoClassifier()
fusion = FusionEngine()

# Request model for text
class TextInput(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Multimodal Sentiment Classifier API is running."}

@app.post("/predict/text")
def predict_text(data: TextInput):
    if not config["model"]["text"]:
        return {"error": "Text model disabled in config"}

    start_time = time.time()
    sentiment, score = text_model.predict(data.text)
    processing_time = time.time() - start_time

    # Log the prediction
    prediction_id = sentiment_logger.log_prediction(
        input_data=data.text,
        mode="text",
        sentiment=sentiment,
        confidence=score,
        processing_time=processing_time
    )

    return {
        "sentiment": sentiment,
        "confidence": score,
        "prediction_id": prediction_id,
        "processing_time": processing_time
    }

@app.post("/predict/audio")
async def predict_audio(file: UploadFile = File(...)):
    if not config["model"]["audio"]:
        return {"error": "Audio model disabled in config"}

    start_time = time.time()
    contents = await file.read()
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    sentiment, score = audio_model.predict(temp_path)
    processing_time = time.time() - start_time
    os.remove(temp_path)

    # Log the prediction
    prediction_id = sentiment_logger.log_prediction(
        input_data=file.filename,
        mode="audio",
        sentiment=sentiment,
        confidence=score,
        processing_time=processing_time,
        model_details={"file_size": len(contents), "filename": file.filename}
    )

    return {
        "sentiment": sentiment,
        "confidence": score,
        "prediction_id": prediction_id,
        "processing_time": processing_time
    }

@app.post("/predict/video")
async def predict_video(file: UploadFile = File(...)):
    if not config["model"]["video"]:
        return {"error": "Video model disabled in config"}

    start_time = time.time()
    contents = await file.read()
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    sentiment, score = video_model.predict(temp_path)
    processing_time = time.time() - start_time
    os.remove(temp_path)

    # Log the prediction
    prediction_id = sentiment_logger.log_prediction(
        input_data=file.filename,
        mode="video",
        sentiment=sentiment,
        confidence=score,
        processing_time=processing_time,
        model_details={"file_size": len(contents), "filename": file.filename}
    )

    return {
        "sentiment": sentiment,
        "confidence": score,
        "prediction_id": prediction_id,
        "processing_time": processing_time
    }

@app.post("/predict/multimodal")
async def predict_multimodal(file: UploadFile = File(...)):
    start_time = time.time()
    results = []
    modalities = []

    contents = await file.read()
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    # Process each enabled modality
    if config["model"]["text"]:
        sentiment, score = text_model.predict("This is a great example!")  # dummy input for now
        results.append((sentiment, score))
        modalities.append("text")

    if config["model"]["audio"]:
        sentiment, score = audio_model.predict(temp_path)
        results.append((sentiment, score))
        modalities.append("audio")

    if config["model"]["video"]:
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
    prediction_id = sentiment_logger.log_multimodal_prediction(
        input_data=file.filename,
        individual_results=[(modalities[i], results[i][0], results[i][1]) for i in range(len(results))],
        fused_result=(final_sentiment, final_confidence),
        processing_time=processing_time
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
    return sentiment_logger.get_statistics()

@app.get("/analytics/predictions")
def get_predictions(limit: int = 50, mode: str = None, sentiment: str = None):
    """Get recent predictions with optional filtering"""
    return sentiment_logger.get_predictions(limit=limit, mode=mode, sentiment=sentiment)

@app.post("/analytics/session/start")
def start_session(user_id: str = None):
    """Start a new logging session"""
    session_id = sentiment_logger.start_session(user_id=user_id)
    return {"session_id": session_id}

@app.post("/analytics/session/{session_id}/end")
def end_session(session_id: str):
    """End a logging session"""
    sentiment_logger.end_session(session_id)
    return {"message": "Session ended", "session_id": session_id}