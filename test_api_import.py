#!/usr/bin/env python3
"""
Test API import step by step to find the hanging point
"""

import time
import sys

def log_with_timestamp(message):
    """Log with timestamp"""
    timestamp = time.strftime('%H:%M:%S')
    print(f"[{timestamp}] {message}")
    sys.stdout.flush()

def test_model_imports():
    """Test model imports individually"""
    
    log_with_timestamp("🔍 Testing individual model imports...")
    
    try:
        log_with_timestamp("Step 1: Testing TextClassifier import...")
        from classifiers.text_classifier import TextClassifier
        log_with_timestamp("✅ TextClassifier imported")
        
        log_with_timestamp("Step 2: Creating TextClassifier instance...")
        text_model = TextClassifier()
        log_with_timestamp("✅ TextClassifier instance created")
        
        log_with_timestamp("Step 3: Testing AudioClassifier import...")
        from classifiers.audio_classifier import AudioClassifier
        log_with_timestamp("✅ AudioClassifier imported")
        
        log_with_timestamp("Step 4: Creating AudioClassifier instance...")
        audio_model = AudioClassifier()
        log_with_timestamp("✅ AudioClassifier instance created")
        
        log_with_timestamp("Step 5: Testing VideoClassifier import...")
        from classifiers.video_classifier import VideoClassifier
        log_with_timestamp("✅ VideoClassifier imported")
        
        log_with_timestamp("Step 6: Creating VideoClassifier instance...")
        video_model = VideoClassifier()
        log_with_timestamp("✅ VideoClassifier instance created")
        
        return True
        
    except Exception as e:
        log_with_timestamp(f"❌ Error in model import test: {e}")
        import traceback
        log_with_timestamp(f"❌ Traceback: {traceback.format_exc()}")
        return False

def test_api_components():
    """Test API components step by step"""
    
    log_with_timestamp("🔍 Testing API components...")
    
    try:
        log_with_timestamp("Step 1: Testing FastAPI import...")
        from fastapi import FastAPI
        log_with_timestamp("✅ FastAPI imported")
        
        log_with_timestamp("Step 2: Testing config loader...")
        from config_loader import get_config_loader
        config_loader = get_config_loader()
        log_with_timestamp("✅ Config loader created")
        
        log_with_timestamp("Step 3: Testing model versioning...")
        from model_versioning import ModelVersionManager
        version_manager = ModelVersionManager()
        log_with_timestamp("✅ Model versioning created")
        
        log_with_timestamp("Step 4: Testing input validation...")
        from input_validation import InputValidator
        input_validator = InputValidator()
        log_with_timestamp("✅ Input validation created")
        
        log_with_timestamp("Step 5: Testing enhanced logging...")
        from enhanced_logging import EnhancedSentimentLogger
        sentiment_logger = EnhancedSentimentLogger()
        log_with_timestamp("✅ Enhanced logging created")
        
        return True
        
    except Exception as e:
        log_with_timestamp(f"❌ Error in API components test: {e}")
        import traceback
        log_with_timestamp(f"❌ Traceback: {traceback.format_exc()}")
        return False

def test_api_import():
    """Test the actual API import"""
    
    log_with_timestamp("🔍 Testing API import...")
    
    try:
        log_with_timestamp("Step 1: Importing api module...")
        log_with_timestamp("⚠️  This might be where it hangs...")
        
        import api
        
        log_with_timestamp("✅ API module imported successfully!")
        log_with_timestamp("Step 2: Getting FastAPI app...")
        
        app = api.app
        log_with_timestamp("✅ FastAPI app retrieved successfully!")
        
        return True
        
    except Exception as e:
        log_with_timestamp(f"❌ Error in API import: {e}")
        import traceback
        log_with_timestamp(f"❌ Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    log_with_timestamp("=" * 60)
    log_with_timestamp("🎯 API IMPORT ISOLATION TEST")
    log_with_timestamp("=" * 60)
    
    # Test models first
    models_success = test_model_imports()
    
    log_with_timestamp("-" * 40)
    
    # Test API components
    if models_success:
        components_success = test_api_components()
        
        log_with_timestamp("-" * 40)
        
        # Test full API import
        if components_success:
            api_success = test_api_import()
            
            if api_success:
                log_with_timestamp("🎉 ALL TESTS PASSED - API imports successfully!")
                log_with_timestamp("🔍 The hanging issue must be with uvicorn startup")
            else:
                log_with_timestamp("❌ API IMPORT IS THE PROBLEM")
        else:
            log_with_timestamp("❌ API COMPONENTS ARE THE PROBLEM")
    else:
        log_with_timestamp("❌ MODEL IMPORTS ARE THE PROBLEM")
    
    log_with_timestamp("=" * 60)
