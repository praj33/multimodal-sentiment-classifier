# logging_system.py

import json
import os
from datetime import datetime
from tinydb import TinyDB, Query
from typing import Dict, Any, Optional
import uuid

class SentimentLogger:
    def __init__(self, db_path: str = "logs/sentiment_predictions.json"):
        """
        Initialize the sentiment logging system
        
        Args:
            db_path: Path to the TinyDB database file
        """
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db = TinyDB(db_path)
        self.predictions_table = self.db.table('predictions')
        self.sessions_table = self.db.table('sessions')
        
    def log_prediction(self, 
                      input_data: str,
                      mode: str,
                      sentiment: str,
                      confidence: float,
                      processing_time: float = None,
                      model_details: Dict[str, Any] = None,
                      session_id: str = None) -> str:
        """
        Log a sentiment prediction
        
        Args:
            input_data: The input text/file path
            mode: The prediction mode (text, audio, video, multimodal)
            sentiment: Predicted sentiment
            confidence: Confidence score
            processing_time: Time taken for prediction in seconds
            model_details: Additional model-specific details
            session_id: Optional session identifier
            
        Returns:
            str: Unique prediction ID
        """
        prediction_id = str(uuid.uuid4())
        
        log_entry = {
            'prediction_id': prediction_id,
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'input_data': input_data[:500] if isinstance(input_data, str) else str(input_data),  # Truncate long inputs
            'mode': mode,
            'sentiment': sentiment,
            'confidence': confidence,
            'processing_time': processing_time,
            'model_details': model_details or {}
        }
        
        self.predictions_table.insert(log_entry)
        return prediction_id
    
    def log_multimodal_prediction(self,
                                 input_data: str,
                                 individual_results: list,
                                 fused_result: tuple,
                                 processing_time: float = None,
                                 session_id: str = None) -> str:
        """
        Log a multimodal prediction with individual modality results
        
        Args:
            input_data: The input file path
            individual_results: List of (modality, sentiment, confidence) tuples
            fused_result: Final (sentiment, confidence) tuple
            processing_time: Total processing time
            session_id: Optional session identifier
            
        Returns:
            str: Unique prediction ID
        """
        prediction_id = str(uuid.uuid4())
        
        log_entry = {
            'prediction_id': prediction_id,
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'input_data': str(input_data),
            'mode': 'multimodal',
            'individual_results': [
                {
                    'modality': modality,
                    'sentiment': sentiment,
                    'confidence': confidence
                }
                for modality, sentiment, confidence in individual_results
            ],
            'fused_sentiment': fused_result[0],
            'fused_confidence': fused_result[1],
            'processing_time': processing_time
        }
        
        self.predictions_table.insert(log_entry)
        return prediction_id
    
    def start_session(self, user_id: str = None, metadata: Dict[str, Any] = None) -> str:
        """
        Start a new logging session
        
        Args:
            user_id: Optional user identifier
            metadata: Additional session metadata
            
        Returns:
            str: Session ID
        """
        session_id = str(uuid.uuid4())
        
        session_entry = {
            'session_id': session_id,
            'user_id': user_id,
            'start_time': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        self.sessions_table.insert(session_entry)
        return session_id
    
    def end_session(self, session_id: str):
        """
        End a logging session
        
        Args:
            session_id: Session to end
        """
        Session = Query()
        self.sessions_table.update(
            {'end_time': datetime.now().isoformat()},
            Session.session_id == session_id
        )
    
    def get_predictions(self, 
                       limit: int = 100,
                       mode: str = None,
                       sentiment: str = None,
                       session_id: str = None) -> list:
        """
        Retrieve predictions with optional filtering
        
        Args:
            limit: Maximum number of predictions to return
            mode: Filter by prediction mode
            sentiment: Filter by sentiment
            session_id: Filter by session ID
            
        Returns:
            list: List of prediction records
        """
        Prediction = Query()
        
        # Build query conditions
        conditions = []
        if mode:
            conditions.append(Prediction.mode == mode)
        if sentiment:
            conditions.append(Prediction.sentiment == sentiment)
        if session_id:
            conditions.append(Prediction.session_id == session_id)
        
        if conditions:
            # Combine conditions with AND
            query = conditions[0]
            for condition in conditions[1:]:
                query = query & condition
            results = self.predictions_table.search(query)
        else:
            results = self.predictions_table.all()
        
        # Sort by timestamp (newest first) and limit
        results.sort(key=lambda x: x['timestamp'], reverse=True)
        return results[:limit]
    
    def get_statistics(self, session_id: str = None) -> Dict[str, Any]:
        """
        Get prediction statistics
        
        Args:
            session_id: Optional session filter
            
        Returns:
            dict: Statistics summary
        """
        if session_id:
            Prediction = Query()
            predictions = self.predictions_table.search(Prediction.session_id == session_id)
        else:
            predictions = self.predictions_table.all()
        
        if not predictions:
            return {
                'total_predictions': 0,
                'sentiment_distribution': {},
                'mode_distribution': {},
                'average_confidence': 0,
                'processing_time_stats': {}
            }
        
        # Calculate statistics
        total = len(predictions)
        sentiments = [p['sentiment'] for p in predictions if 'sentiment' in p]
        modes = [p['mode'] for p in predictions]
        confidences = [p['confidence'] for p in predictions if 'confidence' in p and p['confidence'] is not None]
        processing_times = [p['processing_time'] for p in predictions if 'processing_time' in p and p['processing_time'] is not None]
        
        # Sentiment distribution
        sentiment_dist = {}
        for sentiment in sentiments:
            sentiment_dist[sentiment] = sentiment_dist.get(sentiment, 0) + 1
        
        # Mode distribution
        mode_dist = {}
        for mode in modes:
            mode_dist[mode] = mode_dist.get(mode, 0) + 1
        
        # Processing time statistics
        processing_stats = {}
        if processing_times:
            processing_stats = {
                'average': sum(processing_times) / len(processing_times),
                'min': min(processing_times),
                'max': max(processing_times),
                'count': len(processing_times)
            }
        
        return {
            'total_predictions': total,
            'sentiment_distribution': sentiment_dist,
            'mode_distribution': mode_dist,
            'average_confidence': sum(confidences) / len(confidences) if confidences else 0,
            'processing_time_stats': processing_stats
        }
    
    def export_logs(self, output_path: str, format: str = 'json'):
        """
        Export logs to file
        
        Args:
            output_path: Path to save the exported logs
            format: Export format ('json' or 'csv')
        """
        predictions = self.predictions_table.all()
        
        if format.lower() == 'json':
            with open(output_path, 'w') as f:
                json.dump(predictions, f, indent=2)
        elif format.lower() == 'csv':
            import csv
            if predictions:
                with open(output_path, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=predictions[0].keys())
                    writer.writeheader()
                    writer.writerows(predictions)
        else:
            raise ValueError("Format must be 'json' or 'csv'")
    
    def clear_logs(self, older_than_days: int = None):
        """
        Clear logs, optionally only those older than specified days
        
        Args:
            older_than_days: Only clear logs older than this many days
        """
        if older_than_days:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=older_than_days)
            cutoff_iso = cutoff_date.isoformat()
            
            Prediction = Query()
            self.predictions_table.remove(Prediction.timestamp < cutoff_iso)
        else:
            self.predictions_table.truncate()
            self.sessions_table.truncate()

# Global logger instance
sentiment_logger = SentimentLogger()
