# api.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from classifiers.text_classifier import TextClassifier
from classifiers.audio_classifier import AudioClassifier
from classifiers.video_classifier import VideoClassifier
from fusion.fusion_engine import FusionEngine
import os
import yaml

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
    sentiment, score = text_model.predict(data.text)
    return {"sentiment": sentiment, "confidence": score}

@app.post("/predict/audio")
async def predict_audio(file: UploadFile = File(...)):
    if not config["model"]["audio"]:
        return {"error": "Audio model disabled in config"}
    
    contents = await file.read()
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    sentiment, score = audio_model.predict(temp_path)
    os.remove(temp_path)

    return {"sentiment": sentiment, "confidence": score}

@app.post("/predict/video")
async def predict_video(file: UploadFile = File(...)):
    if not config["model"]["video"]:
        return {"error": "Video model disabled in config"}
    
    contents = await file.read()
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    sentiment, score = video_model.predict(temp_path)
    os.remove(temp_path)

    return {"sentiment": sentiment, "confidence": score}

@app.post("/predict/multimodal")
async def predict_multimodal(file: UploadFile = File(...)):
    results = []

    contents = await file.read()
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    if config["model"]["text"]:
        sentiment, score = text_model.predict("This is a great example!")  # dummy input
        results.append((sentiment, score))

    if config["model"]["audio"]:
        sentiment, score = audio_model.predict(temp_path)
        results.append((sentiment, score))

    if config["model"]["video"]:
        sentiment, score = video_model.predict(temp_path)
        results.append((sentiment, score))

    os.remove(temp_path)

    final_sentiment, final_confidence = fusion.predict(results)
    return {
        "fused_sentiment": final_sentiment,
        "confidence": final_confidence,
        "individual": [
            {"mode": m, "sentiment": s, "confidence": c}
            for (m, (s, c)) in zip(["text", "audio", "video"], results)
        ]
    }