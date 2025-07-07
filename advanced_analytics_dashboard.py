"""
🚀 Advanced Real-time Analytics Dashboard for Multimodal Sentiment Analysis
Enterprise-grade analytics with live streaming, advanced visualizations, and insights

Features:
- Real-time sentiment trend analysis with WebSocket streaming
- Geographic sentiment heatmaps and regional analysis
- Advanced data visualizations with interactive charts
- Performance metrics and model analytics
- Sentiment distribution analysis and pattern detection
- Export capabilities and reporting features
- Multi-dimensional filtering and drill-down analysis
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import sqlite3
import pandas as pd
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import logging
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentTrend(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative" 
    NEUTRAL = "neutral"

@dataclass
class AnalyticsMetric:
    timestamp: datetime
    sentiment: str
    confidence: float
    modality: str
    processing_time: float
    user_id: Optional[str] = None
    location: Optional[str] = None
    session_id: Optional[str] = None

class AdvancedAnalyticsEngine:
    """Advanced analytics engine for real-time sentiment analysis insights"""
    
    def __init__(self, db_path: str = "logs/sentiment_enhanced.db"):
        self.db_path = db_path
        self.real_time_buffer = deque(maxlen=1000)  # Store last 1000 predictions
        self.active_connections: List[WebSocket] = []
        self.sentiment_trends = defaultdict(list)
        self.geographic_data = defaultdict(lambda: defaultdict(int))
        self.performance_metrics = defaultdict(list)
        
        # Initialize analytics database
        self._init_analytics_db()
        
    def _init_analytics_db(self):
        """Initialize analytics database with advanced schema"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create analytics tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analytics_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    sentiment TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    modality TEXT NOT NULL,
                    processing_time REAL NOT NULL,
                    user_id TEXT,
                    location TEXT,
                    session_id TEXT,
                    metadata TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sentiment_trends (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE NOT NULL,
                    hour INTEGER NOT NULL,
                    sentiment TEXT NOT NULL,
                    count INTEGER DEFAULT 1,
                    avg_confidence REAL,
                    UNIQUE(date, hour, sentiment)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS geographic_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    count INTEGER DEFAULT 1,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(location, sentiment)
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("Analytics database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize analytics database: {e}")
    
    async def add_metric(self, metric: AnalyticsMetric):
        """Add new analytics metric and update real-time data"""
        try:
            # Add to real-time buffer
            self.real_time_buffer.append(metric)
            
            # Store in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO analytics_metrics 
                (timestamp, sentiment, confidence, modality, processing_time, user_id, location, session_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                metric.timestamp.isoformat(),
                metric.sentiment,
                metric.confidence,
                metric.modality,
                metric.processing_time,
                metric.user_id,
                metric.location,
                metric.session_id
            ))
            
            # Update trend data
            date = metric.timestamp.date()
            hour = metric.timestamp.hour
            cursor.execute("""
                INSERT OR REPLACE INTO sentiment_trends 
                (date, hour, sentiment, count, avg_confidence)
                VALUES (?, ?, ?, 
                    COALESCE((SELECT count FROM sentiment_trends WHERE date=? AND hour=? AND sentiment=?), 0) + 1,
                    COALESCE((SELECT avg_confidence FROM sentiment_trends WHERE date=? AND hour=? AND sentiment=?), ?) 
                )
            """, (date, hour, metric.sentiment, date, hour, metric.sentiment, date, hour, metric.sentiment, metric.confidence))
            
            # Update geographic data if location provided
            if metric.location:
                cursor.execute("""
                    INSERT OR REPLACE INTO geographic_analytics 
                    (location, sentiment, count, last_updated)
                    VALUES (?, ?, 
                        COALESCE((SELECT count FROM geographic_analytics WHERE location=? AND sentiment=?), 0) + 1,
                        CURRENT_TIMESTAMP
                    )
                """, (metric.location, metric.sentiment, metric.location, metric.sentiment))
            
            conn.commit()
            conn.close()
            
            # Broadcast to connected WebSocket clients
            await self._broadcast_real_time_update(metric)
            
        except Exception as e:
            logger.error(f"Failed to add analytics metric: {e}")
    
    async def _broadcast_real_time_update(self, metric: AnalyticsMetric):
        """Broadcast real-time updates to connected WebSocket clients"""
        if not self.active_connections:
            return
            
        update_data = {
            "type": "sentiment_update",
            "data": asdict(metric),
            "timestamp": metric.timestamp.isoformat(),
            "summary": await self.get_real_time_summary()
        }
        
        # Convert datetime objects to strings for JSON serialization
        update_data["data"]["timestamp"] = metric.timestamp.isoformat()
        
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(update_data))
            except WebSocketDisconnect:
                disconnected.append(connection)
            except Exception as e:
                logger.error(f"Error broadcasting to WebSocket: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            self.active_connections.remove(conn)
    
    async def get_real_time_summary(self) -> Dict[str, Any]:
        """Get real-time summary statistics"""
        if not self.real_time_buffer:
            return {"total": 0, "sentiment_distribution": {}, "avg_confidence": 0}
        
        recent_metrics = list(self.real_time_buffer)[-100:]  # Last 100 predictions
        
        sentiment_counts = defaultdict(int)
        total_confidence = 0
        modality_counts = defaultdict(int)
        
        for metric in recent_metrics:
            sentiment_counts[metric.sentiment] += 1
            total_confidence += metric.confidence
            modality_counts[metric.modality] += 1
        
        return {
            "total": len(recent_metrics),
            "sentiment_distribution": dict(sentiment_counts),
            "avg_confidence": total_confidence / len(recent_metrics) if recent_metrics else 0,
            "modality_distribution": dict(modality_counts),
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_trend_analysis(self, hours: int = 24) -> Dict[str, Any]:
        """Get sentiment trend analysis for specified time period"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Get trend data
            query = """
                SELECT date, hour, sentiment, count, avg_confidence
                FROM sentiment_trends 
                WHERE datetime(date || ' ' || printf('%02d:00:00', hour)) >= datetime('now', '-{} hours')
                ORDER BY date, hour
            """.format(hours)
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if df.empty:
                return {"trends": [], "summary": {}}
            
            # Process trend data
            trends = []
            for _, row in df.iterrows():
                trends.append({
                    "datetime": f"{row['date']} {row['hour']:02d}:00:00",
                    "sentiment": row['sentiment'],
                    "count": row['count'],
                    "confidence": row['avg_confidence']
                })
            
            # Calculate summary statistics
            summary = {
                "total_predictions": df['count'].sum(),
                "avg_confidence": df['avg_confidence'].mean(),
                "sentiment_breakdown": df.groupby('sentiment')['count'].sum().to_dict(),
                "peak_hour": df.loc[df['count'].idxmax(), 'hour'] if not df.empty else None
            }
            
            return {"trends": trends, "summary": summary}
            
        except Exception as e:
            logger.error(f"Failed to get trend analysis: {e}")
            return {"trends": [], "summary": {}}
    
    async def get_geographic_analysis(self) -> Dict[str, Any]:
        """Get geographic sentiment analysis"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = """
                SELECT location, sentiment, count, last_updated
                FROM geographic_analytics 
                WHERE location IS NOT NULL
                ORDER BY count DESC
            """
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if df.empty:
                return {"geographic_data": [], "summary": {}}
            
            geographic_data = df.to_dict('records')
            
            # Calculate summary
            summary = {
                "total_locations": df['location'].nunique(),
                "total_predictions": df['count'].sum(),
                "top_location": df.loc[df['count'].idxmax(), 'location'] if not df.empty else None,
                "sentiment_by_location": df.groupby('location')['sentiment'].apply(
                    lambda x: x.value_counts().to_dict()
                ).to_dict()
            }
            
            return {"geographic_data": geographic_data, "summary": summary}
            
        except Exception as e:
            logger.error(f"Failed to get geographic analysis: {e}")
            return {"geographic_data": [], "summary": {}}

# Initialize analytics engine
analytics_engine = AdvancedAnalyticsEngine()

# FastAPI app for analytics dashboard
analytics_app = FastAPI(title="Advanced Analytics Dashboard", version="1.0.0")

# Mount static files and templates
analytics_app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@analytics_app.websocket("/ws/analytics")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time analytics updates"""
    await websocket.accept()
    analytics_engine.active_connections.append(websocket)
    
    try:
        # Send initial data
        initial_data = {
            "type": "initial_data",
            "summary": await analytics_engine.get_real_time_summary(),
            "trends": await analytics_engine.get_trend_analysis(24),
            "geographic": await analytics_engine.get_geographic_analysis()
        }
        await websocket.send_text(json.dumps(initial_data))
        
        # Keep connection alive
        while True:
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        analytics_engine.active_connections.remove(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in analytics_engine.active_connections:
            analytics_engine.active_connections.remove(websocket)

@analytics_app.get("/", response_class=HTMLResponse)
async def analytics_dashboard(request: Request):
    """Main analytics dashboard page"""
    return templates.TemplateResponse("analytics_dashboard.html", {"request": request})

@analytics_app.get("/api/analytics/summary")
async def get_analytics_summary():
    """Get current analytics summary"""
    return await analytics_engine.get_real_time_summary()

@analytics_app.get("/api/analytics/trends")
async def get_trends(hours: int = 24):
    """Get sentiment trends for specified hours"""
    return await analytics_engine.get_trend_analysis(hours)

@analytics_app.get("/api/analytics/geographic")
async def get_geographic():
    """Get geographic sentiment analysis"""
    return await analytics_engine.get_geographic_analysis()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(analytics_app, host="0.0.0.0", port=8001)
