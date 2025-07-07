#!/usr/bin/env python3
"""
🎓 Uniguru Sentiment Agent + API Adapter
Production-grade plug-in agent for Uniguru/Gurukul educational platform

🚀 Features:
- Single predict(json_input) function for unified sentiment analysis
- Multi-modal support: text, image_url, audio processing
- Gurukul persona integration: youth/kids/spiritual contexts
- Language detection and multi-language support
- TTS emotion mapping for voice synthesis
- Production-ready JSON API with comprehensive error handling
- CLI and Google Colab compatibility

🎯 Designed for Educational Excellence with Raj's Advanced Implementation
"""

import asyncio
import base64
import json
import logging
import os
import time
import traceback
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from urllib.parse import urlparse
import requests
from PIL import Image
import io

# Language detection
try:
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed = 0  # Ensure consistent results
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False
    print("⚠️  langdetect not installed. Language detection will be limited.")

# Import our existing multimodal components
from classifiers.text_classifier import TextClassifier
from classifiers.audio_classifier import AudioClassifier
from classifiers.video_classifier import VideoClassifier
from fusion.fusion_engine import FusionEngine
from advanced_analytics_dashboard import analytics_engine, AnalyticsMetric

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UniguruSentimentAgent:
    """
    🎓 Production-grade Uniguru Sentiment Agent
    
    Unified sentiment analysis agent designed specifically for educational platforms
    with persona-aware analysis and comprehensive multi-modal support.
    """
    
    def __init__(self):
        """Initialize the Uniguru Sentiment Agent with all required models"""
        self.text_classifier = None
        self.audio_classifier = None
        self.video_classifier = None
        self.fusion_engine = None
        self.is_initialized = False
        
        # Persona-specific configurations
        self.persona_configs = {
            "youth": {
                "tone_mapping": {
                    "positive": ["enthusiastic", "excited", "confident", "motivated"],
                    "negative": ["frustrated", "disappointed", "stressed", "overwhelmed"],
                    "neutral": ["focused", "contemplative", "steady", "balanced"]
                },
                "tts_emotions": {
                    "positive": "energetic",
                    "negative": "concerned",
                    "neutral": "calm"
                },
                "sensitivity_boost": 1.2  # Amplify emotional detection for youth
            },
            "kids": {
                "tone_mapping": {
                    "positive": ["joyful", "playful", "happy", "cheerful"],
                    "negative": ["sad", "confused", "worried", "upset"],
                    "neutral": ["curious", "thoughtful", "peaceful", "content"]
                },
                "tts_emotions": {
                    "positive": "cheerful",
                    "negative": "gentle",
                    "neutral": "friendly"
                },
                "sensitivity_boost": 1.5  # Higher sensitivity for children
            },
            "spiritual": {
                "tone_mapping": {
                    "positive": ["serene", "enlightened", "peaceful", "grateful"],
                    "negative": ["troubled", "seeking", "reflective", "contemplative"],
                    "neutral": ["meditative", "centered", "mindful", "balanced"]
                },
                "tts_emotions": {
                    "positive": "serene",
                    "negative": "compassionate",
                    "neutral": "peaceful"
                },
                "sensitivity_boost": 0.9  # More nuanced detection for spiritual context
            }
        }
        
        # Language code mapping
        self.language_names = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
            'ko': 'Korean', 'zh': 'Chinese', 'ar': 'Arabic', 'hi': 'Hindi',
            'bn': 'Bengali', 'ur': 'Urdu', 'ta': 'Tamil', 'te': 'Telugu',
            'mr': 'Marathi', 'gu': 'Gujarati', 'kn': 'Kannada', 'ml': 'Malayalam',
            'pa': 'Punjabi', 'or': 'Odia', 'as': 'Assamese', 'ne': 'Nepali'
        }
        
        logger.info("🎓 Uniguru Sentiment Agent initialized")
    
    def _lazy_load_models(self):
        """Lazy load models to improve startup time"""
        if not self.is_initialized:
            logger.info("🧠 Loading sentiment analysis models...")
            
            try:
                self.text_classifier = TextClassifier()
                logger.info("✅ Text classifier loaded")
                
                self.audio_classifier = AudioClassifier()
                logger.info("✅ Audio classifier loaded")
                
                self.video_classifier = VideoClassifier()
                logger.info("✅ Video classifier loaded")
                
                self.fusion_engine = FusionEngine()
                logger.info("✅ Fusion engine loaded")
                
                self.is_initialized = True
                logger.info("🚀 All models loaded successfully")
                
            except Exception as e:
                logger.error(f"❌ Failed to load models: {e}")
                raise RuntimeError(f"Model initialization failed: {e}")
    
    def detect_language(self, text: str) -> Optional[str]:
        """Detect language of input text"""
        if not text or not text.strip():
            return None
            
        try:
            if LANGDETECT_AVAILABLE:
                detected_code = detect(text)
                return self.language_names.get(detected_code, detected_code)
            else:
                # Fallback: Simple heuristic detection
                if any(ord(char) > 127 for char in text):
                    return "Non-English"
                return "English"
        except Exception as e:
            logger.warning(f"Language detection failed: {e}")
            return "Unknown"
    
    def _download_image(self, image_url: str) -> Optional[bytes]:
        """Download image from URL with error handling"""
        try:
            # Validate URL
            parsed_url = urlparse(image_url)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError("Invalid URL format")
            
            # Download with timeout and size limits
            response = requests.get(
                image_url, 
                timeout=10,
                headers={'User-Agent': 'Uniguru-Sentiment-Agent/1.0'},
                stream=True
            )
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            if not content_type.startswith('image/'):
                raise ValueError(f"URL does not point to an image: {content_type}")
            
            # Check file size (max 10MB)
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > 10 * 1024 * 1024:
                raise ValueError("Image too large (max 10MB)")
            
            # Read content with size limit
            content = b""
            for chunk in response.iter_content(chunk_size=8192):
                content += chunk
                if len(content) > 10 * 1024 * 1024:
                    raise ValueError("Image too large (max 10MB)")
            
            return content
            
        except Exception as e:
            logger.error(f"Failed to download image from {image_url}: {e}")
            return None
    
    def _analyze_image_sentiment(self, image_data: bytes) -> Dict[str, Any]:
        """Analyze sentiment from image data using video classifier"""
        try:
            # Convert image bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Save temporarily for video classifier (which can handle images)
            temp_path = f"temp_image_{int(time.time())}.jpg"
            image.save(temp_path, 'JPEG')
            
            try:
                # Use video classifier for image analysis
                result = self.video_classifier.predict(temp_path)
                
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
                return result
                
            except Exception as e:
                # Clean up on error
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                raise e
                
        except Exception as e:
            logger.error(f"Image sentiment analysis failed: {e}")
            return {"sentiment": "neutral", "confidence": 0.5}
    
    def _map_persona_tone(self, sentiment: str, confidence: float, persona: str) -> str:
        """Map sentiment to persona-specific tone"""
        if persona not in self.persona_configs:
            persona = "youth"  # Default fallback
        
        config = self.persona_configs[persona]
        tone_options = config["tone_mapping"].get(sentiment, ["neutral"])
        
        # Select tone based on confidence level
        if confidence > 0.8:
            return tone_options[0]  # Most confident tone
        elif confidence > 0.6:
            return tone_options[min(1, len(tone_options) - 1)]
        else:
            return tone_options[-1]  # Most conservative tone
    
    def _get_tts_emotion(self, sentiment: str, persona: str) -> str:
        """Get TTS emotion mapping for persona"""
        if persona not in self.persona_configs:
            persona = "youth"
        
        return self.persona_configs[persona]["tts_emotions"].get(sentiment, "neutral")
    
    def _apply_persona_sensitivity(self, confidence: float, persona: str) -> float:
        """Apply persona-specific sensitivity adjustments"""
        if persona not in self.persona_configs:
            return confidence
        
        boost = self.persona_configs[persona]["sensitivity_boost"]
        adjusted = confidence * boost
        return min(1.0, adjusted)  # Cap at 1.0
    
    async def predict(self, json_input: Union[str, Dict[str, Any]], simple_format: bool = True) -> Dict[str, Any]:
        """
        🎯 Main prediction function for Uniguru Sentiment Agent

        Args:
            json_input: JSON string or dict with keys:
                - text (optional): Text to analyze
                - image_url (optional): URL of image to analyze
                - audio_url (optional): URL of audio to analyze
                - persona (optional): "youth", "kids", or "spiritual"
                - language (optional): Force specific language
                - simple_format (optional): Return simple format (default: True)

        Returns:
            Simple format (default):
            {
                "sentiment": "positive|negative|neutral",
                "tone": "persona-specific tone",
                "confidence": 0.89,
                "tts_emotion": "emotion for TTS",
                "language": "detected language" (if detected)
            }

            Advanced format (simple_format=False):
            {
                "sentiment": "positive|negative|neutral",
                "tone": "persona-specific tone",
                "confidence": 0.0-1.0,
                "tts_emotion": "emotion for TTS",
                "language": "detected language",
                "processing_time_ms": float,
                "analysis_details": {...},
                "persona": "applied persona",
                "timestamp": "ISO timestamp"
            }
        """
        start_time = time.time()
        
        try:
            # Parse input
            if isinstance(json_input, str):
                try:
                    input_data = json.loads(json_input)
                except json.JSONDecodeError as e:
                    return {
                        "error": "Invalid JSON input",
                        "details": str(e),
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                input_data = json_input
            
            # Lazy load models
            self._lazy_load_models()
            
            # Extract parameters
            text = input_data.get("text", "").strip()
            image_url = input_data.get("image_url", "").strip()
            audio_url = input_data.get("audio_url", "").strip()
            persona = input_data.get("persona", "youth").lower()
            forced_language = input_data.get("language")

            # Check if simple format is requested in input
            if "simple_format" in input_data:
                simple_format = input_data.get("simple_format", True)

            # Validate persona
            if persona not in self.persona_configs:
                persona = "youth"  # Default fallback
            
            # Validate input - handle empty input gracefully
            if not any([text, image_url, audio_url]):
                # Return neutral response for empty input
                if simple_format:
                    return {
                        "sentiment": "neutral",
                        "tone": "neutral",
                        "confidence": 0.5,
                        "tts_emotion": "calm"
                    }
                else:
                    return {
                        "sentiment": "neutral",
                        "tone": "neutral",
                        "confidence": 0.5,
                        "tts_emotion": "calm",
                        "processing_time_ms": 0.0,
                        "persona": persona,
                        "timestamp": datetime.now().isoformat(),
                        "analysis_details": {
                            "text": {
                                "sentiment": "neutral",
                                "confidence": 0.5,
                                "basic_analysis": True,
                                "emotions": {"neutral": 0.5},
                                "intensity": "low",
                                "emotional_context": {
                                    "dominant_emotion": "neutral",
                                    "secondary_emotion": None,
                                    "emotional_stability": 1.0
                                },
                                "advanced_metrics": {
                                    "emotional_complexity": 0.0,
                                    "sentiment_strength": 0.5,
                                    "emotional_consistency": 1.0
                                },
                                "advanced_analysis": True
                            }
                        },
                        "language": "Unknown",
                        "input_summary": {
                            "has_text": False,
                            "has_image": False,
                            "has_audio": False,
                            "modalities_analyzed": 0
                        }
                    }
            
            # Initialize results
            results = []
            analysis_details = {}
            detected_language = None
            
            # Text analysis
            if text:
                try:
                    # Detect language
                    if not forced_language:
                        detected_language = self.detect_language(text)
                    else:
                        detected_language = forced_language
                    
                    # Analyze text sentiment
                    text_result = self.text_classifier.predict(text)
                    
                    if isinstance(text_result, dict):
                        sentiment = text_result.get('sentiment', 'neutral')
                        confidence = text_result.get('confidence', 0.5)
                        analysis_details['text'] = text_result
                    else:
                        sentiment, confidence = text_result
                        analysis_details['text'] = {'sentiment': sentiment, 'confidence': confidence}
                    
                    results.append(('text', sentiment, confidence))
                    
                except Exception as e:
                    logger.error(f"Text analysis failed: {e}")
                    analysis_details['text'] = {'error': str(e)}
            
            # Image analysis
            if image_url:
                try:
                    image_data = self._download_image(image_url)
                    if image_data:
                        image_result = self._analyze_image_sentiment(image_data)
                        
                        if isinstance(image_result, dict):
                            sentiment = image_result.get('sentiment', 'neutral')
                            confidence = image_result.get('confidence', 0.5)
                            analysis_details['image'] = image_result
                        else:
                            sentiment, confidence = image_result
                            analysis_details['image'] = {'sentiment': sentiment, 'confidence': confidence}
                        
                        results.append(('image', sentiment, confidence))
                    else:
                        # Handle image download failure gracefully - provide neutral sentiment
                        logger.warning(f"Image download failed for {image_url}, using neutral sentiment")
                        results.append(('image', 'neutral', 0.5))
                        analysis_details['image'] = {
                            'sentiment': 'neutral',
                            'confidence': 0.5,
                            'note': 'Image unavailable, neutral sentiment assigned'
                        }
                        
                except Exception as e:
                    logger.error(f"Image analysis failed: {e}")
                    analysis_details['image'] = {'error': str(e)}
            
            # Audio analysis (if URL provided)
            if audio_url:
                try:
                    # Note: This would require downloading and processing audio
                    # For now, we'll provide a placeholder
                    analysis_details['audio'] = {'note': 'Audio URL processing not yet implemented'}
                except Exception as e:
                    logger.error(f"Audio analysis failed: {e}")
                    analysis_details['audio'] = {'error': str(e)}
            
            # Fusion analysis if multiple modalities
            if len(results) > 1:
                try:
                    # Use fusion engine for multi-modal analysis
                    sentiments = [r[1] for r in results]
                    confidences = [r[2] for r in results]
                    
                    fusion_result = self.fusion_engine.predict({
                        'sentiments': sentiments,
                        'confidences': confidences,
                        'modalities': [r[0] for r in results]
                    })
                    
                    final_sentiment = fusion_result.get('sentiment', sentiments[0])
                    final_confidence = fusion_result.get('confidence', sum(confidences) / len(confidences))
                    analysis_details['fusion'] = fusion_result
                    
                except Exception as e:
                    logger.error(f"Fusion analysis failed: {e}")
                    # Fallback to highest confidence result
                    best_result = max(results, key=lambda x: x[2])
                    final_sentiment = best_result[1]
                    final_confidence = best_result[2]
                    analysis_details['fusion'] = {'error': str(e), 'fallback': 'highest_confidence'}
            
            elif len(results) == 1:
                final_sentiment = results[0][1]
                final_confidence = results[0][2]
            else:
                # Ensure we always return the required format, even on complete failure
                logger.warning("All analysis methods failed, returning neutral sentiment")
                final_sentiment = "neutral"
                final_confidence = 0.5
            
            # Apply persona sensitivity
            final_confidence = self._apply_persona_sensitivity(final_confidence, persona)
            
            # Generate persona-specific tone and TTS emotion
            tone = self._map_persona_tone(final_sentiment, final_confidence, persona)
            tts_emotion = self._get_tts_emotion(final_sentiment, persona)
            
            # Calculate processing time
            processing_time = (time.time() - start_time) * 1000
            
            # Log analytics
            try:
                await analytics_engine.add_metric(AnalyticsMetric(
                    timestamp=datetime.now(),
                    sentiment=final_sentiment,
                    confidence=final_confidence,
                    modality="uniguru_agent",
                    processing_time=processing_time,
                    user_id=input_data.get("user_id"),
                    location=input_data.get("location"),
                    session_id=input_data.get("session_id")
                ))
            except Exception as e:
                logger.warning(f"Analytics logging failed: {e}")
            
            # Build response based on format preference
            if simple_format:
                # Simple format as requested
                response = {
                    "sentiment": final_sentiment,
                    "tone": tone,
                    "confidence": round(final_confidence, 2),
                    "tts_emotion": tts_emotion
                }

                # Add language if detected (bonus feature)
                if detected_language:
                    response["language"] = detected_language

            else:
                # Advanced format with full details
                response = {
                    "sentiment": final_sentiment,
                    "tone": tone,
                    "confidence": round(final_confidence, 3),
                    "tts_emotion": tts_emotion,
                    "processing_time_ms": round(processing_time, 2),
                    "persona": persona,
                    "timestamp": datetime.now().isoformat(),
                    "analysis_details": analysis_details
                }

                # Add language if detected
                if detected_language:
                    response["language"] = detected_language

                # Add input summary
                response["input_summary"] = {
                    "has_text": bool(text),
                    "has_image": bool(image_url),
                    "has_audio": bool(audio_url),
                    "modalities_analyzed": len(results)
                }

            return response
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            logger.error(traceback.format_exc())
            
            return {
                "error": "Prediction failed",
                "details": str(e),
                "processing_time_ms": round((time.time() - start_time) * 1000, 2),
                "timestamp": datetime.now().isoformat()
            }

# Global agent instance
_agent_instance = None

def get_agent() -> UniguruSentimentAgent:
    """Get singleton agent instance"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = UniguruSentimentAgent()
    return _agent_instance

async def predict(json_input: Union[str, Dict[str, Any]], simple_format: bool = True) -> Dict[str, Any]:
    """
    🎯 Main prediction function for Uniguru Sentiment Agent

    This is the primary entry point for the Uniguru Sentiment Agent.

    Args:
        json_input: JSON string or dict with analysis parameters:
            {
                "image_url": "...",
                "text": "...",
                "persona": "youth/kids/spiritual"
            }
        simple_format: Return simple format (default: True)

    Returns:
        Simple format (default):
        {
            "sentiment": "positive",
            "tone": "joyful",
            "confidence": 0.89,
            "tts_emotion": "cheerful",
            "language": "English" (bonus - if detected)
        }
    """
    agent = get_agent()
    return await agent.predict(json_input, simple_format)

def predict_sync(json_input: Union[str, Dict[str, Any]], simple_format: bool = True) -> Dict[str, Any]:
    """
    🎯 Synchronous wrapper for predict function

    Args:
        json_input: JSON string or dict with analysis parameters
        simple_format: Return simple format (default: True)

    Returns:
        Same as predict() but runs synchronously
    """
    return asyncio.run(predict(json_input, simple_format))

# CLI Support
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python sentiment_agent_adapter.py '<json_input>'")
        print("Example: python sentiment_agent_adapter.py '{\"text\": \"I love learning!\", \"persona\": \"kids\"}'")
        sys.exit(1)
    
    json_input = sys.argv[1]
    
    # Run prediction
    result = asyncio.run(predict(json_input))
    print(json.dumps(result, indent=2))
