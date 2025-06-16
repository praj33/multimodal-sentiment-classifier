# fusion/fusion_engine.py

from collections import Counter

class FusionEngine:
    def __init__(self, weights=None):
        """
        Initialize FusionEngine with optional weights for different modalities
        weights: dict with keys 'text', 'audio', 'video' and their respective weights
        """
        # Default weights - text is most reliable, then video, then audio
        self.weights = weights or {
            'text': 0.5,
            'audio': 0.25,
            'video': 0.25
        }

    def predict(self, predictions, modalities=None):
        """
        Predict sentiment using weighted fusion of multiple modalities

        Args:
            predictions: list of (sentiment, confidence) tuples
            modalities: list of modality names corresponding to predictions
                       ['text', 'audio', 'video'] or subset

        Returns:
            tuple: (final_sentiment, final_confidence)
        """
        if not predictions:
            return "neutral", 0.0

        # If no modalities specified, assume order: text, audio, video
        if modalities is None:
            modalities = ['text', 'audio', 'video'][:len(predictions)]

        # Calculate weighted scores for each sentiment
        sentiment_scores = {'positive': 0, 'negative': 0, 'neutral': 0}
        total_weight = 0

        for i, (sentiment, confidence) in enumerate(predictions):
            if i < len(modalities):
                modality = modalities[i]
                weight = self.weights.get(modality, 1.0)

                # Weight the confidence by modality weight
                weighted_score = confidence * weight
                sentiment_scores[sentiment] += weighted_score
                total_weight += weight

        # Normalize scores
        if total_weight > 0:
            for sentiment in sentiment_scores:
                sentiment_scores[sentiment] /= total_weight

        # Find the sentiment with highest weighted score
        final_sentiment = max(sentiment_scores, key=sentiment_scores.get)
        final_confidence = sentiment_scores[final_sentiment]

        # Apply ensemble confidence boost if multiple modalities agree
        agreement_bonus = self._calculate_agreement_bonus(predictions)
        final_confidence = min(final_confidence + agreement_bonus, 1.0)

        return final_sentiment, final_confidence

    def _calculate_agreement_bonus(self, predictions):
        """
        Calculate bonus confidence when multiple modalities agree
        """
        if len(predictions) < 2:
            return 0.0

        sentiments = [s for s, _ in predictions]
        sentiment_counts = Counter(sentiments)

        # If all modalities agree, give a bonus
        if len(sentiment_counts) == 1:
            return 0.1  # 10% bonus for unanimous agreement

        # If majority agrees, give smaller bonus
        most_common_count = sentiment_counts.most_common(1)[0][1]
        if most_common_count > len(predictions) / 2:
            return 0.05  # 5% bonus for majority agreement

        return 0.0

    def predict_with_details(self, predictions, modalities=None):
        """
        Predict sentiment with detailed breakdown of each modality's contribution
        """
        if not predictions:
            return {
                'final_sentiment': 'neutral',
                'final_confidence': 0.0,
                'modality_breakdown': {},
                'weighted_scores': {}
            }

        if modalities is None:
            modalities = ['text', 'audio', 'video'][:len(predictions)]

        # Calculate detailed breakdown
        modality_breakdown = {}
        weighted_scores = {'positive': 0, 'negative': 0, 'neutral': 0}
        total_weight = 0

        for i, (sentiment, confidence) in enumerate(predictions):
            if i < len(modalities):
                modality = modalities[i]
                weight = self.weights.get(modality, 1.0)
                weighted_score = confidence * weight

                modality_breakdown[modality] = {
                    'sentiment': sentiment,
                    'confidence': confidence,
                    'weight': weight,
                    'weighted_contribution': weighted_score
                }

                weighted_scores[sentiment] += weighted_score
                total_weight += weight

        # Normalize scores
        if total_weight > 0:
            for sentiment in weighted_scores:
                weighted_scores[sentiment] /= total_weight

        final_sentiment = max(weighted_scores, key=weighted_scores.get)
        final_confidence = weighted_scores[final_sentiment]

        # Apply agreement bonus
        agreement_bonus = self._calculate_agreement_bonus(predictions)
        final_confidence = min(final_confidence + agreement_bonus, 1.0)

        return {
            'final_sentiment': final_sentiment,
            'final_confidence': final_confidence,
            'modality_breakdown': modality_breakdown,
            'weighted_scores': weighted_scores,
            'agreement_bonus': agreement_bonus
        }