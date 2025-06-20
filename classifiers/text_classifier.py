# classifiers/text_classifier.py

from transformers import pipeline
import torch
import logging

logger = logging.getLogger(__name__)

class TextClassifier:
    def __init__(self):
        """Initialize text classifier with performance optimizations"""
        # Determine device for optimal performance
        device = 0 if torch.cuda.is_available() else -1

        # Use optimized model with caching
        try:
            self.classifier = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=device,
                return_all_scores=False,  # Only return top prediction for speed
                tokenizer_kwargs={'padding': True, 'truncation': True, 'max_length': 512}
            )
            logger.info(f"Text classifier initialized on device: {'GPU' if device >= 0 else 'CPU'}")
        except Exception as e:
            logger.error(f"Failed to initialize text classifier: {e}")
            raise

    def predict(self, text):
        """Predict sentiment with input validation and error handling"""
        if not text or not isinstance(text, str):
            return "neutral", 0.5

        # Truncate very long texts for performance
        if len(text) > 512:
            text = text[:512]

        try:
            result = self.classifier(text)[0]  # Get first result
            sentiment = result['label'].lower()  # 'POSITIVE' → 'positive'
            score = result['score']  # Confidence score

            # Normalize sentiment labels
            if sentiment == 'positive':
                sentiment = 'positive'
            elif sentiment == 'negative':
                sentiment = 'negative'
            else:
                sentiment = 'neutral'

            return sentiment, float(score)
        except Exception as e:
            logger.error(f"Text prediction failed: {e}")
            return "neutral", 0.5
