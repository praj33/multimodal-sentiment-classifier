#!/usr/bin/env python3
"""
Simple server startup script with better error handling and progress tracking
"""

import sys
import time
import traceback

def start_server():
    """Start the FastAPI server with progress tracking"""
    
    print("🚀 Starting Multimodal Sentiment Analysis API Server...")
    print("=" * 60)
    
    try:
        # Step 1: Import basic modules
        print("📦 Step 1/6: Importing basic modules...")
        import os
        import uvicorn
        print("✅ Basic modules imported")
        
        # Step 2: Import FastAPI
        print("📦 Step 2/6: Importing FastAPI...")
        from fastapi import FastAPI
        print("✅ FastAPI imported")
        
        # Step 3: Import classifiers (this takes time)
        print("📦 Step 3/6: Loading AI models (this may take 30-60 seconds)...")
        print("   🧠 Loading text classifier...")
        from classifiers.text_classifier import TextClassifier
        print("   🎵 Loading audio classifier...")
        from classifiers.audio_classifier import AudioClassifier
        print("   🎥 Loading video classifier...")
        from classifiers.video_classifier import VideoClassifier
        print("✅ All AI models loaded successfully")
        
        # Step 4: Import API module
        print("📦 Step 4/6: Importing API module...")
        import api
        print("✅ API module imported")
        
        # Step 5: Get the FastAPI app
        print("📦 Step 5/6: Initializing FastAPI application...")
        app = api.app
        print("✅ FastAPI application ready")
        
        # Step 6: Start the server
        print("📦 Step 6/6: Starting uvicorn server...")
        print("=" * 60)
        print("🎭 Multimodal Sentiment Analysis API")
        print("🌐 Server will be available at: http://localhost:8000")
        print("📚 API Documentation: http://localhost:8000/docs")
        print("🎯 Dashboard: http://localhost:8000/dashboard")
        print("=" * 60)
        print("🚀 Starting server... (Press Ctrl+C to stop)")
        print()
        
        # Start the server
        uvicorn.run(
            "api:app",  # Use import string for reload mode
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print("\n🔍 Full traceback:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    start_server()
