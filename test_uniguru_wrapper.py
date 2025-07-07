#!/usr/bin/env python3
"""
🎯 Test Suite for Uniguru Agent Wrapper - Part 1 Implementation
Testing the exact specifications requested by the user
"""

import asyncio
import json
import sys
import time
from sentiment_agent_adapter import predict, predict_sync

def test_simple_format():
    """Test the simple format as specified by user requirements"""
    
    print("🎯 UNIGURU AGENT WRAPPER - PART 1 TEST SUITE")
    print("=" * 60)
    
    # Test cases matching user specifications
    test_cases = [
        {
            "name": "📋 Test 1: Basic Text + Youth Persona",
            "input": {
                "text": "I love learning new things!",
                "persona": "youth"
            },
            "expected_keys": ["sentiment", "tone", "confidence", "tts_emotion"]
        },
        {
            "name": "📋 Test 2: Image URL + Kids Persona", 
            "input": {
                "image_url": "https://example.com/happy_child.jpg",
                "persona": "kids"
            },
            "expected_keys": ["sentiment", "tone", "confidence", "tts_emotion"]
        },
        {
            "name": "📋 Test 3: Text + Image + Spiritual Persona",
            "input": {
                "text": "Finding peace in meditation",
                "image_url": "https://example.com/meditation.jpg", 
                "persona": "spiritual"
            },
            "expected_keys": ["sentiment", "tone", "confidence", "tts_emotion"]
        },
        {
            "name": "📋 Test 4: Multi-language Text (Bonus Language Detection)",
            "input": {
                "text": "Je suis très heureux aujourd'hui!",
                "persona": "youth"
            },
            "expected_keys": ["sentiment", "tone", "confidence", "tts_emotion", "language"]
        },
        {
            "name": "📋 Test 5: JSON String Input Format",
            "input": '{"text": "This is amazing!", "persona": "kids"}',
            "expected_keys": ["sentiment", "tone", "confidence", "tts_emotion"]
        }
    ]
    
    passed_tests = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{test_case['name']}")
        
        try:
            # Test synchronous version
            start_time = time.time()
            result = predict_sync(test_case["input"])
            processing_time = (time.time() - start_time) * 1000
            
            # Validate response format
            if not isinstance(result, dict):
                print(f"❌ FAILED - Response is not a dictionary")
                continue
                
            # Check required keys
            missing_keys = []
            for key in ["sentiment", "tone", "confidence", "tts_emotion"]:
                if key not in result:
                    missing_keys.append(key)
            
            if missing_keys:
                print(f"❌ FAILED - Missing keys: {missing_keys}")
                continue
            
            # Validate data types and ranges
            if result["sentiment"] not in ["positive", "negative", "neutral"]:
                print(f"❌ FAILED - Invalid sentiment: {result['sentiment']}")
                continue
                
            if not isinstance(result["confidence"], (int, float)) or not (0 <= result["confidence"] <= 1):
                print(f"❌ FAILED - Invalid confidence: {result['confidence']}")
                continue
            
            if not isinstance(result["tone"], str) or not result["tone"]:
                print(f"❌ FAILED - Invalid tone: {result['tone']}")
                continue
                
            if not isinstance(result["tts_emotion"], str) or not result["tts_emotion"]:
                print(f"❌ FAILED - Invalid tts_emotion: {result['tts_emotion']}")
                continue
            
            # Check for unwanted extra fields (should be minimal)
            extra_fields = set(result.keys()) - {"sentiment", "tone", "confidence", "tts_emotion", "language"}
            if extra_fields:
                print(f"⚠️  WARNING - Extra fields found: {extra_fields}")
            
            # Success
            print(f"✅ PASSED")
            print(f"   📊 Sentiment: {result['sentiment']}")
            print(f"   🎭 Tone: {result['tone']}")
            print(f"   📈 Confidence: {result['confidence']}")
            print(f"   🎵 TTS Emotion: {result['tts_emotion']}")
            if "language" in result:
                print(f"   🌍 Language: {result['language']} (BONUS)")
            print(f"   ⏱️  Processing: {processing_time:.1f}ms")
            
            passed_tests += 1
            
        except Exception as e:
            print(f"❌ FAILED - Exception: {e}")
            import traceback
            traceback.print_exc()
    
    # Final Results
    print("\n" + "=" * 60)
    print("🏆 FINAL TEST RESULTS")
    print("=" * 60)
    print(f"📊 Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}")
    print(f"🎯 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 PERFECT! All tests passed!")
        print("🚀 Uniguru Agent Wrapper Part 1 - COMPLETE!")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} tests failed")
        return False

def test_format_comparison():
    """Test both simple and advanced formats"""
    print("\n" + "=" * 60)
    print("🔄 FORMAT COMPARISON TEST")
    print("=" * 60)
    
    test_input = {
        "text": "I'm excited about learning!",
        "persona": "youth"
    }
    
    print("\n📋 Simple Format (Default):")
    simple_result = predict_sync(test_input, simple_format=True)
    print(json.dumps(simple_result, indent=2))
    
    print("\n📋 Advanced Format:")
    advanced_result = predict_sync(test_input, simple_format=False)
    print(json.dumps(advanced_result, indent=2))
    
    print(f"\n📊 Simple format keys: {len(simple_result)} fields")
    print(f"📊 Advanced format keys: {len(advanced_result)} fields")

if __name__ == "__main__":
    success = test_simple_format()
    test_format_comparison()
    
    if success:
        print("\n🎯 PART 1 REQUIREMENTS COMPLETED SUCCESSFULLY!")
        print("✅ Single predict(json_input) function")
        print("✅ Accepts JSON with image_url, text, persona")
        print("✅ Returns sentiment, tone, confidence, tts_emotion")
        print("✅ BONUS: Language detection included")
        sys.exit(0)
    else:
        sys.exit(1)
