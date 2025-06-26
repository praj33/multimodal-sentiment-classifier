#!/usr/bin/env python3
"""Debug script to test individual sentiment analysis components"""

import sys
import os
sys.path.insert(0, os.getcwd())

def test_text_classifier():
    """Test text classifier with various inputs"""
    print("🔍 Testing Text Classifier...")
    
    try:
        from classifiers.text_classifier import TextClassifier
        classifier = TextClassifier()
        
        test_texts = [
            "I love this product! It's amazing!",
            "This is terrible and I hate it.",
            "This is okay, nothing special.",
            "The weather is nice today.",
            "I'm feeling great!",
            "This makes me sad.",
            "Neutral statement about facts."
        ]
        
        for text in test_texts:
            sentiment, confidence = classifier.predict(text)
            print(f"  Text: '{text[:30]}...'")
            print(f"  Result: {sentiment} (confidence: {confidence:.3f})")
            print()
            
        return True
    except Exception as e:
        print(f"❌ Text classifier failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fusion_engine():
    """Test fusion engine with sample predictions"""
    print("🔍 Testing Fusion Engine...")
    
    try:
        from fusion.fusion_engine import FusionEngine
        fusion = FusionEngine()
        
        # Test case 1: All positive
        predictions1 = [('positive', 0.9), ('positive', 0.8), ('positive', 0.7)]
        modalities1 = ['text', 'audio', 'video']
        result1 = fusion.predict(predictions1, modalities1)
        print(f"  Test 1 - All positive: {result1}")
        
        # Test case 2: Mixed results
        predictions2 = [('positive', 0.6), ('negative', 0.8), ('neutral', 0.5)]
        modalities2 = ['text', 'audio', 'video']
        result2 = fusion.predict(predictions2, modalities2)
        print(f"  Test 2 - Mixed results: {result2}")
        
        # Test case 3: All negative
        predictions3 = [('negative', 0.9), ('negative', 0.7), ('negative', 0.8)]
        modalities3 = ['text', 'audio', 'video']
        result3 = fusion.predict(predictions3, modalities3)
        print(f"  Test 3 - All negative: {result3}")
        
        return True
    except Exception as e:
        print(f"❌ Fusion engine failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoint():
    """Test API endpoint directly"""
    print("🔍 Testing API Endpoint...")
    
    try:
        import requests
        import json
        
        # Test text endpoint
        url = "http://localhost:8000/predict/text"
        test_data = {"text": "I love this amazing product!"}
        
        response = requests.post(url, json=test_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"  API Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"  API Error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("  ⚠️ API server not running. Start with: python api.py")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_input_validation():
    """Test input validation"""
    print("🔍 Testing Input Validation...")
    
    try:
        from input_validation import input_validator
        
        test_text = "I love this amazing product!"
        sanitized = input_validator.validate_text_input(test_text)
        print(f"  Original: '{test_text}'")
        print(f"  Sanitized: '{sanitized}'")
        print(f"  Type: {type(sanitized)}")
        
        return True
    except Exception as e:
        print(f"❌ Input validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Debugging Multimodal Sentiment Analysis")
    print("=" * 50)
    
    # Test each component
    tests = [
        ("Input Validation", test_input_validation),
        ("Text Classifier", test_text_classifier),
        ("Fusion Engine", test_fusion_engine),
        ("API Endpoint", test_api_endpoint)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        results[test_name] = test_func()
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 Test Results Summary:")
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    if all(results.values()):
        print("\n🎉 All tests passed! The issue might be in the dashboard.")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
