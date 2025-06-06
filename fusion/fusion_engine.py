# fusion/fusion_engine.py

from collections import Counter

class FusionEngine:
    def __init__(self):
        pass

    def predict(self, predictions):
        """
        predictions: list of (sentiment, confidence) tuples.
        Example:
            [('positive', 0.9), ('neutral', 0.6), ('positive', 0.7)]
        """
        if not predictions:
            return "neutral", 0.0

        sentiments = [s for s, _ in predictions]
        final_sentiment = Counter(sentiments).most_common(1)[0][0]

        avg_confidence = sum(score for _, score in predictions) / len(predictions)

        return final_sentiment, avg_confidence