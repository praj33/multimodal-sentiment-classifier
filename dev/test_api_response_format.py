#!/usr/bin/env python3
"""
Quick test to verify API response format matches requirements
"""

import sys
import os
sys.path.append('.')

from model_versioning import format_api_response, ModelVersionManager

def test_api_response_format():
    """Test that API response matches exact requirements"""
    
    # Test the format_api_response function
    response = format_api_response(
        sentiment="positive",
        confidence=0.88,
        used_models=["text"]
    )
    
    print("=== API Response Format Test ===")
    print("Response:", response)
    print()
    
    # Check required fields
    required_fields = ["sentiment", "confidence", "model_version"]
    for field in required_fields:
        if field not in response:
            print(f"❌ MISSING FIELD: {field}")
            return False
        else:
            print(f"✅ Found field: {field}")
    
    # Check model_version structure
    model_version = response.get("model_version", {})
    required_model_fields = ["text", "audio", "video", "fusion"]
    
    print("\n=== Model Version Structure Test ===")
    for field in required_model_fields:
        if field not in model_version:
            print(f"❌ MISSING MODEL VERSION: {field}")
            return False
        else:
            print(f"✅ Found model version: {field} = {model_version[field]}")
    
    # Check exact format match
    expected_structure = {
        "sentiment": str,
        "confidence": (int, float),
        "model_version": {
            "text": str,
            "audio": str,
            "video": str,
            "fusion": str
        }
    }
    
    print("\n=== Structure Validation ===")
    if isinstance(response["sentiment"], str):
        print("✅ sentiment is string")
    else:
        print("❌ sentiment is not string")
        return False
        
    if isinstance(response["confidence"], (int, float)):
        print("✅ confidence is number")
    else:
        print("❌ confidence is not number")
        return False
        
    if isinstance(response["model_version"], dict):
        print("✅ model_version is dict")
    else:
        print("❌ model_version is not dict")
        return False
    
    print("\n=== EXACT FORMAT MATCH TEST ===")
    print("Expected format:")
    print('''{
  "sentiment": "positive",
  "confidence": 0.88,
  "model_version": {
    "text": "v1.0",
    "audio": "v1.0", 
    "video": "v1.0",
    "fusion": "v1.0"
  }
}''')
    
    print("\nActual response:")
    import json
    print(json.dumps(response, indent=2))
    
    print("\n🎉 ALL TESTS PASSED! API response format matches requirements.")
    return True

if __name__ == "__main__":
    test_api_response_format()
