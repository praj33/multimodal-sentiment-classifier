# fusion/fusion_engine.py

from collections import Counter

class FusionEngine:
    def __init__(self, weights=None, fusion_method='confidence_weighted'):
        """
        Initialize FusionEngine with advanced weighting strategies
        weights: dict with keys 'text', 'audio', 'video' and their respective weights
        fusion_method: 'simple', 'confidence_weighted', 'adaptive'
        """
        # Default base weights - text is most reliable, then video, then audio
        self.base_weights = weights or {
            'text': 0.5,
            'audio': 0.25,
            'video': 0.25
        }
        self.fusion_method = fusion_method
        self.confidence_threshold = 0.7
        self.uncertainty_penalty = 0.3
        self.consensus_boost = 0.15

    def calculate_dynamic_weights(self, predictions, modalities):
        """Calculate dynamic weights based on confidence and consensus"""
        if self.fusion_method == 'simple':
            return self.base_weights

        weights = self.base_weights.copy()

        # Confidence-based weight adjustment
        for i, (sentiment, confidence) in enumerate(predictions):
            if i < len(modalities):
                modality = modalities[i]

                # Boost weight for high-confidence predictions
                if confidence > self.confidence_threshold:
                    confidence_boost = (confidence - self.confidence_threshold) * 0.5
                    weights[modality] *= (1 + confidence_boost)

                # Penalize low-confidence predictions
                elif confidence < 0.5:
                    uncertainty_penalty = (0.5 - confidence) * self.uncertainty_penalty
                    weights[modality] *= max(0.1, 1 - uncertainty_penalty)

        # Consensus detection - boost agreeing modalities
        sentiments = [pred[0] for pred in predictions]
        if len(set(sentiments)) == 1:  # All agree
            for modality in weights:
                if modality in [modalities[i] for i in range(len(predictions))]:
                    weights[modality] *= (1 + self.consensus_boost)

        # Normalize weights
        total_weight = sum(weights.values())
        if total_weight > 0:
            weights = {k: v/total_weight for k, v in weights.items()}

        return weights

    def predict(self, predictions, modalities=None):
        """
        Predict sentiment using advanced weighted fusion of multiple modalities

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

        # Calculate dynamic weights based on confidence and consensus
        dynamic_weights = self.calculate_dynamic_weights(predictions, modalities)

        # Calculate weighted scores for each sentiment
        sentiment_scores = {'positive': 0, 'negative': 0, 'neutral': 0}
        total_weight = 0

        for i, (sentiment, confidence) in enumerate(predictions):
            if i < len(modalities):
                modality = modalities[i]
                weight = dynamic_weights.get(modality, 1.0)

                # Weight the confidence by dynamic modality weight
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