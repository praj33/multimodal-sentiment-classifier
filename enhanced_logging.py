# enhanced_logging.py - Enhanced logging system with multiple database backends

import json
import os
import sqlite3
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging
from tinydb import TinyDB, Query
import hashlib
import uuid

class EnhancedSentimentLogger:
    """Enhanced logging system supporting JSON, SQLite, and TinyDB backends"""
    
    def __init__(self, 
                 db_type: str = "sqlite",  # json, sqlite, tinydb
                 db_path: str = "logs/sentiment_enhanced.db",
                 json_path: str = "logs/sentiment_predictions.json"):
        self.db_type = db_type
        self.db_path = db_path
        self.json_path = json_path
        self.ensure_log_directory()
        
        # Initialize database based on type
        if db_type == "sqlite":
            self._init_sqlite()
        elif db_type == "tinydb":
            self._init_tinydb()
        
        # Setup Python logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/enhanced_app.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Enhanced logging initialized with {db_type} backend")
    
    def ensure_log_directory(self):
        """Ensure logs directory exists"""
        for path in [self.db_path, self.json_path]:
            if path:
                os.makedirs(os.path.dirname(path), exist_ok=True)
    
    def _init_sqlite(self):
        """Initialize SQLite database with comprehensive schema"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Main predictions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prediction_id TEXT UNIQUE NOT NULL,
                    timestamp TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    sentiment TEXT,
                    confidence REAL,
                    processing_time_ms REAL,
                    input_meta TEXT,
                    result_json TEXT,
                    session_id TEXT,
                    input_hash TEXT,
                    model_version TEXT,
                    api_version TEXT,
                    user_agent TEXT,
                    ip_address TEXT
                )
            ''')
            
            # Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    total_predictions INTEGER DEFAULT 0,
                    user_id TEXT,
                    metadata TEXT
                )
            ''')
            
            # Performance metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    processing_time_ms REAL,
                    memory_usage_mb REAL,
                    cpu_usage_percent REAL,
                    model_load_time_ms REAL
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON predictions(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_mode ON predictions(mode)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sentiment ON predictions(sentiment)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_session ON predictions(session_id)')
            
            conn.commit()
            conn.close()
            self.logger.info("SQLite database initialized with enhanced schema")
        except Exception as e:
            self.logger.error(f"Failed to initialize SQLite: {e}")
    
    def _init_tinydb(self):
        """Initialize TinyDB database"""
        try:
            self.tinydb = TinyDB(self.db_path.replace('.db', '_tiny.json'))
            self.predictions_table = self.tinydb.table('predictions')
            self.sessions_table = self.tinydb.table('sessions')
            self.metrics_table = self.tinydb.table('performance_metrics')
            self.logger.info("TinyDB database initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize TinyDB: {e}")
    
    def log_prediction(self, 
                      mode: str, 
                      result: Dict[str, Any], 
                      confidence: float,
                      input_data: Optional[Dict[str, Any]] = None,
                      processing_time: Optional[float] = None,
                      input_content: Optional[str] = None,
                      session_id: Optional[str] = None,
                      model_version: str = "1.0",
                      api_version: str = "1.0",
                      user_agent: Optional[str] = None,
                      ip_address: Optional[str] = None) -> str:
        """Log a sentiment prediction with comprehensive metadata"""
        
        prediction_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        input_hash = self._generate_input_hash(input_content) if input_content else None
        
        # Extract sentiment from result
        sentiment = result.get('sentiment', 'unknown') if isinstance(result, dict) else str(result)
        
        log_entry = {
            "prediction_id": prediction_id,
            "timestamp": timestamp,
            "mode": mode,
            "sentiment": sentiment,
            "result": result,
            "confidence": confidence,
            "input_meta": input_data or {},
            "processing_time_ms": processing_time,
            "session_id": session_id,
            "input_hash": input_hash,
            "model_version": model_version,
            "api_version": api_version,
            "user_agent": user_agent,
            "ip_address": ip_address
        }
        
        # Write to appropriate storage
        if self.db_type == "sqlite":
            self._write_to_sqlite(log_entry)
        elif self.db_type == "tinydb":
            self._write_to_tinydb(log_entry)
        else:
            self._write_to_json(log_entry)
        
        # Log to Python logger
        self.logger.info(f"Prediction logged: {prediction_id} - {mode} - {sentiment} - {confidence:.3f}")
        
        return prediction_id
    
    def log_performance_metrics(self,
                               mode: str,
                               processing_time_ms: float,
                               memory_usage_mb: Optional[float] = None,
                               cpu_usage_percent: Optional[float] = None,
                               model_load_time_ms: Optional[float] = None):
        """Log performance metrics"""
        
        metrics_entry = {
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "processing_time_ms": processing_time_ms,
            "memory_usage_mb": memory_usage_mb,
            "cpu_usage_percent": cpu_usage_percent,
            "model_load_time_ms": model_load_time_ms
        }
        
        if self.db_type == "sqlite":
            self._write_metrics_to_sqlite(metrics_entry)
        elif self.db_type == "tinydb":
            self.metrics_table.insert(metrics_entry)
        
        self.logger.debug(f"Performance metrics logged: {mode} - {processing_time_ms}ms")
    
    def _write_to_sqlite(self, entry: Dict[str, Any]):
        """Write entry to SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO predictions 
                (prediction_id, timestamp, mode, sentiment, confidence, processing_time_ms, 
                 input_meta, result_json, session_id, input_hash, model_version, 
                 api_version, user_agent, ip_address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                entry['prediction_id'],
                entry['timestamp'],
                entry['mode'],
                entry['sentiment'],
                entry['confidence'],
                entry['processing_time_ms'],
                json.dumps(entry['input_meta']),
                json.dumps(entry['result']),
                entry['session_id'],
                entry['input_hash'],
                entry['model_version'],
                entry['api_version'],
                entry['user_agent'],
                entry['ip_address']
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Failed to write to SQLite: {e}")
    
    def _write_metrics_to_sqlite(self, entry: Dict[str, Any]):
        """Write performance metrics to SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO performance_metrics 
                (timestamp, mode, processing_time_ms, memory_usage_mb, 
                 cpu_usage_percent, model_load_time_ms)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                entry['timestamp'],
                entry['mode'],
                entry['processing_time_ms'],
                entry['memory_usage_mb'],
                entry['cpu_usage_percent'],
                entry['model_load_time_ms']
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Failed to write metrics to SQLite: {e}")
    
    def _write_to_tinydb(self, entry: Dict[str, Any]):
        """Write entry to TinyDB"""
        try:
            self.predictions_table.insert(entry)
        except Exception as e:
            self.logger.error(f"Failed to write to TinyDB: {e}")
    
    def _write_to_json(self, entry: Dict[str, Any]):
        """Write entry to JSON log file"""
        try:
            # Read existing data
            if os.path.exists(self.json_path):
                with open(self.json_path, 'r') as f:
                    data = json.load(f)
            else:
                data = []
            
            # Append new entry
            data.append(entry)
            
            # Keep only last 1000 entries to prevent file from growing too large
            if len(data) > 1000:
                data = data[-1000:]
            
            # Write back to file
            with open(self.json_path, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to write to JSON log: {e}")
    
    def _generate_input_hash(self, content: str) -> str:
        """Generate hash of input content for deduplication"""
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def get_analytics(self, days: int = 7) -> Dict[str, Any]:
        """Get comprehensive analytics"""
        try:
            if self.db_type == "sqlite":
                return self._get_sqlite_analytics(days)
            elif self.db_type == "tinydb":
                return self._get_tinydb_analytics(days)
            else:
                return self._get_json_analytics(days)
        except Exception as e:
            self.logger.error(f"Failed to generate analytics: {e}")
            return {"error": str(e)}
