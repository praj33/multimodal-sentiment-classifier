#!/usr/bin/env python3
"""
Test script for the Multimodal Sentiment Analysis SDK
"""

import sys
from sdk.python.sentiment_sdk import SentimentAnalyzer, analyze_sentiment

def test_api_health():
    """Test if API is healthy"""
    print("🔍 Testing API Health...")
    analyzer = SentimentAnalyzer()

    if analyzer.health_check():
        print("✅ API is healthy and responding")
        return True
    else:
        print("❌ API is not responding. Make sure the server is running:")
        print("   python -m uvicorn api:app --reload")
        return False

def test_text_analysis():
    """Test text sentiment analysis"""
    print("\n📝 Testing Text Analysis...")

    test_texts = [
        "I absolutely love this project!",
        "This is terrible and I hate it.",
        "The weather is okay today.",
        "Amazing work! This is fantastic!",
        "I'm feeling sad and disappointed."
    ]

    analyzer = SentimentAnalyzer()

    for text in test_texts:
        try:
            result = analyzer.analyze_text(text)
            print(f"   Text: '{text[:30]}...'")
            print(f"   Result: {result['sentiment']} (confidence: {result['confidence']:.2f})")
            print(f"   Processing time: {result.get('processing_time', 'N/A')}s")
            print()
        except Exception as e:
            print(f"   ❌ Error analyzing '{text[:30]}...': {e}")

def test_convenience_function():
    """Test the convenience function"""
    print("\n🔧 Testing Convenience Function...")

    try:
        result = analyze_sentiment("This SDK is really convenient!", mode="text")
        print(f"   Convenience function result: {result['sentiment']} ({result['confidence']:.2f})")
    except Exception as e:
        print(f"   ❌ Error with convenience function: {e}")

def test_analytics():
    """Test analytics endpoints"""
    print("\n📊 Testing Analytics...")

    analyzer = SentimentAnalyzer()

    try:
        # Get statistics
        stats = analyzer.get_statistics()
        print(f"   Total predictions: {stats.get('total_predictions', 0)}")
        print(f"   Sentiment distribution: {stats.get('sentiment_distribution', {})}")

        # Get recent predictions
        recent = analyzer.get_recent_predictions(limit=5)
        print(f"   Recent predictions count: {len(recent)}")

    except Exception as e:
        print(f"   ❌ Error getting analytics: {e}")

def test_session_management():
    """Test session management"""
    print("\n🔄 Testing Session Management...")

    analyzer = SentimentAnalyzer()

    try:
        # Start session
        session_id = analyzer.start_session(user_id="test_user")
        print(f"   Started session: {session_id}")

        # Perform some analyses in the session
        analyzer.analyze_text("Session test message")

        # End session
        analyzer.end_session(session_id)
        print(f"   Ended session: {session_id}")

    except Exception as e:
        print(f"   ❌ Error with session management: {e}")

def test_error_handling():
    """Test error handling"""
    print("\n⚠️  Testing Error Handling...")

    analyzer = SentimentAnalyzer(api_url="http://localhost:9999")  # Wrong port

    try:
        analyzer.analyze_text("This should fail")
        print("   ❌ Expected error but got result")
    except Exception as e:
        print(f"   ✅ Correctly caught error: {type(e).__name__}")

def main():
    """Run all tests"""
    print("🧪 Multimodal Sentiment Analysis SDK Test Suite")
    print("=" * 50)

    # Test API health first
    if not test_api_health():
        print("\n❌ Cannot proceed with tests - API is not available")
        sys.exit(1)

    # Run all tests
    test_text_analysis()
    test_convenience_function()
    test_analytics()
    test_session_management()
    test_error_handling()

    print("\n✅ Test suite completed!")
    print("\n💡 To test audio/video functionality:")
    print("   1. Place test files in the project directory")
    print("   2. Run: python run_sentiment.py --input test_audio.wav --mode audio")
    print("   3. Run: python run_sentiment.py --input test_video.mp4 --mode video")

if __name__ == "__main__":
    main()