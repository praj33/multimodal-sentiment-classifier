#!/usr/bin/env python3
"""
🎯 UNIGURU AGENT WRAPPER - PART 1 DEMONSTRATION
Showcasing the exact implementation requested by the user
"""

import json
from sentiment_agent_adapter import predict_sync

def main():
    print("🎯 UNIGURU AGENT WRAPPER - PART 1 COMPLETE!")
    print("=" * 60)
    print("✅ Single predict(json_input) function")
    print("✅ Accepts JSON with image_url, text, persona")  
    print("✅ Returns sentiment, tone, confidence, tts_emotion")
    print("✅ BONUS: Language detection included")
    print("=" * 60)
    
    # Example 1: Basic text analysis
    print("\n📋 Example 1: Basic Text Analysis")
    input1 = {
        "text": "I love learning new things!",
        "persona": "youth"
    }
    print(f"Input: {json.dumps(input1, indent=2)}")
    result1 = predict_sync(input1)
    print(f"Output: {json.dumps(result1, indent=2)}")
    
    # Example 2: Image URL analysis  
    print("\n📋 Example 2: Image URL Analysis")
    input2 = {
        "image_url": "https://example.com/happy_image.jpg",
        "persona": "kids"
    }
    print(f"Input: {json.dumps(input2, indent=2)}")
    result2 = predict_sync(input2)
    print(f"Output: {json.dumps(result2, indent=2)}")
    
    # Example 3: Multi-modal analysis
    print("\n📋 Example 3: Multi-modal Analysis")
    input3 = {
        "text": "Finding inner peace through meditation",
        "image_url": "https://example.com/meditation.jpg",
        "persona": "spiritual"
    }
    print(f"Input: {json.dumps(input3, indent=2)}")
    result3 = predict_sync(input3)
    print(f"Output: {json.dumps(result3, indent=2)}")
    
    # Example 4: Language detection bonus
    print("\n📋 Example 4: Language Detection (BONUS)")
    input4 = {
        "text": "¡Estoy muy feliz hoy!",
        "persona": "youth"
    }
    print(f"Input: {json.dumps(input4, indent=2)}")
    result4 = predict_sync(input4)
    print(f"Output: {json.dumps(result4, indent=2)}")
    
    # Example 5: JSON string input
    print("\n📋 Example 5: JSON String Input")
    input5_str = '{"text": "This is amazing!", "persona": "kids"}'
    print(f"Input: {input5_str}")
    result5 = predict_sync(input5_str)
    print(f"Output: {json.dumps(result5, indent=2)}")
    
    print("\n" + "=" * 60)
    print("🎉 PART 1 IMPLEMENTATION COMPLETE!")
    print("🚀 Ready for 3-hour development milestone")
    print("=" * 60)
    
    # Validate all results have required keys
    all_results = [result1, result2, result3, result4, result5]
    required_keys = ["sentiment", "tone", "confidence", "tts_emotion"]
    
    print("\n🔍 VALIDATION SUMMARY:")
    for i, result in enumerate(all_results, 1):
        missing_keys = [key for key in required_keys if key not in result]
        if missing_keys:
            print(f"❌ Example {i}: Missing {missing_keys}")
        else:
            print(f"✅ Example {i}: All required keys present")
            if "language" in result:
                print(f"   🌍 BONUS: Language detected - {result['language']}")

if __name__ == "__main__":
    main()
