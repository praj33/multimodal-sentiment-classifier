#!/usr/bin/env python3
"""
Test script to identify where the startup is hanging
"""

import sys
import time

def test_imports():
    """Test imports step by step to find the hanging point"""
    
    print("🔍 Testing imports step by step...")
    
    try:
        print("1. Testing basic imports...")
        import os
        import time
        print("✅ Basic imports OK")
        
        print("2. Testing FastAPI import...")
        from fastapi import FastAPI
        print("✅ FastAPI import OK")
        
        print("3. Testing config loader...")
        from config_loader import get_config_loader
        print("✅ Config loader OK")
        
        print("4. Testing model versioning...")
        from model_versioning import ModelVersionManager
        print("✅ Model versioning OK")
        
        print("5. Testing fusion config manager...")
        from fusion_config_manager import FusionConfigManager
        print("✅ Fusion config manager OK")
        
        print("6. Testing fusion engine...")
        from fusion.fusion_engine import FusionEngine
        print("✅ Fusion engine OK")
        
        print("7. Testing text classifier...")
        from classifiers.text_classifier import TextClassifier
        print("✅ Text classifier OK")
        
        print("8. Testing audio classifier...")
        from classifiers.audio_classifier import AudioClassifier
        print("✅ Audio classifier OK")
        
        print("9. Testing video classifier...")
        from classifiers.video_classifier import VideoClassifier
        print("✅ Video classifier OK")
        
        print("10. Testing input validation...")
        from input_validation import InputValidator
        print("✅ Input validation OK")
        
        print("11. Testing enhanced logging...")
        from enhanced_logging import EnhancedSentimentLogger
        print("✅ Enhanced logging OK")
        
        print("12. Testing streaming API...")
        from streaming_api import add_streaming_routes
        print("✅ Streaming API OK")
        
        print("13. Creating instances...")
        print("   Creating config loader...")
        config_loader = get_config_loader()
        print("   Creating version manager...")
        version_manager = ModelVersionManager()
        print("   Creating fusion engine...")
        fusion_engine = FusionEngine()
        print("   Creating text model...")
        text_model = TextClassifier()
        print("   Creating audio model...")
        audio_model = AudioClassifier()
        print("   Creating video model...")
        video_model = VideoClassifier()
        print("✅ All instances created OK")
        
        print("14. Testing API import...")
        import api
        print("✅ API import OK")
        
        print("🎉 All tests passed! API should start normally.")
        
    except Exception as e:
        print(f"❌ Error at step: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\n🚀 Try running: python -m uvicorn api:app --host 0.0.0.0 --port 8000")
    else:
        print("\n❌ Fix the errors above before starting the server")
