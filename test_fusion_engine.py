#!/usr/bin/env python3
"""
Test fusion engine to isolate the hanging issue
"""

import time
import sys

def log_with_timestamp(message):
    """Log with timestamp"""
    timestamp = time.strftime('%H:%M:%S')
    print(f"[{timestamp}] {message}")
    sys.stdout.flush()

def test_fusion_engine():
    """Test fusion engine step by step"""
    
    log_with_timestamp("🔍 Testing Fusion Engine...")
    
    try:
        log_with_timestamp("Step 1: Importing FusionEngine...")
        from fusion.fusion_engine import FusionEngine
        log_with_timestamp("✅ FusionEngine imported successfully")
        
        log_with_timestamp("Step 2: Creating FusionEngine instance...")
        fusion_engine = FusionEngine()
        log_with_timestamp("✅ FusionEngine instance created")
        
        log_with_timestamp("Step 3: Testing simple prediction...")
        
        # Test data that matches what the API would send
        predictions = [
            ("positive", 0.8),  # text
            ("positive", 0.7),  # audio  
            ("neutral", 0.6)    # video
        ]
        modalities = ["text", "audio", "video"]
        
        log_with_timestamp(f"Input predictions: {predictions}")
        log_with_timestamp(f"Input modalities: {modalities}")
        
        log_with_timestamp("Step 4: Calling fusion_engine.predict()...")
        log_with_timestamp("⚠️  This is where it might hang...")
        
        # This is the exact line that's hanging in the API
        result = fusion_engine.predict(predictions, modalities)
        
        log_with_timestamp(f"✅ Fusion engine result: {result}")
        log_with_timestamp("✅ Fusion engine test completed successfully!")
        
        return True
        
    except Exception as e:
        log_with_timestamp(f"❌ Error in fusion engine test: {e}")
        import traceback
        log_with_timestamp(f"❌ Traceback: {traceback.format_exc()}")
        return False

def test_fusion_config_manager():
    """Test fusion config manager separately"""
    
    log_with_timestamp("🔍 Testing FusionConfigManager...")
    
    try:
        log_with_timestamp("Step 1: Importing FusionConfigManager...")
        from fusion_config_manager import FusionConfigManager
        log_with_timestamp("✅ FusionConfigManager imported")
        
        log_with_timestamp("Step 2: Creating FusionConfigManager instance...")
        config_manager = FusionConfigManager()
        log_with_timestamp("✅ FusionConfigManager instance created")
        
        log_with_timestamp("Step 3: Loading config...")
        config = config_manager.load_config()
        log_with_timestamp(f"✅ Config loaded: {config.get('fusion', {}).get('method', 'not found')}")
        
        return True
        
    except Exception as e:
        log_with_timestamp(f"❌ Error in config manager test: {e}")
        import traceback
        log_with_timestamp(f"❌ Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    log_with_timestamp("=" * 60)
    log_with_timestamp("🎯 FUSION ENGINE ISOLATION TEST")
    log_with_timestamp("=" * 60)
    
    # Test config manager first
    config_success = test_fusion_config_manager()
    
    log_with_timestamp("-" * 40)
    
    # Test fusion engine
    if config_success:
        fusion_success = test_fusion_engine()
        
        if fusion_success:
            log_with_timestamp("🎉 ALL TESTS PASSED - Fusion engine is working!")
            log_with_timestamp("🔍 The hanging issue must be elsewhere in the API")
        else:
            log_with_timestamp("❌ FUSION ENGINE IS THE PROBLEM")
    else:
        log_with_timestamp("❌ CONFIG MANAGER IS THE PROBLEM")
    
    log_with_timestamp("=" * 60)
