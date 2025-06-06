 # classifiers/text_classifier.py

from transformers import pipeline

class TextClassifier:
    def __init__(self):
        # Use default sentiment analysis model from Hugging Face
        self.classifier = pipeline("sentiment-analysis")

    def predict(self, text):
        result = self.classifier(text)[0]  # Get first result
        sentiment = result['label'].lower()  # 'POSITIVE' → 'positive'
        score = result['score']  # Confidence score
        return sentiment, score
