#!/usr/bin/env python3
"""
Simple test script for audio and video classifiers
Tests the classifiers directly without the API
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_audio_classifier():
    """Test the audio classifier directly"""
    print("🎵 Testing Audio Classifier...")
    
    try:
        from classifiers.audio_classifier import AudioClassifier
        
        # Initialize classifier
        audio_classifier = AudioClassifier()
        print("✅ Audio classifier initialized successfully")
        
        # Test with bytes (simulating file upload)
        test_bytes = b"fake audio data for testing"
        sentiment, confidence = audio_classifier.predict(test_bytes)
        
        print(f"📊 Audio Test Result:")
        print(f"   Sentiment: {sentiment}")
        print(f"   Confidence: {confidence:.3f}")
        
        # Test with file path if audio files exist
        audio_files = [
            "test_files/audio/positive_happy_tone.wav",
            "test_files/audio/negative_sad_tone.wav",
            "test_files/audio/neutral_calm_tone.wav"
        ]
        
        for audio_file in audio_files:
            if os.path.exists(audio_file):
                print(f"\n🎵 Testing with file: {os.path.basename(audio_file)}")
                sentiment, confidence = audio_classifier.predict(audio_file)
                print(f"   Sentiment: {sentiment}")
                print(f"   Confidence: {confidence:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Audio classifier test failed: {e}")
        return False

def test_video_classifier():
    """Test the video classifier directly"""
    print("\n🎬 Testing Video Classifier...")
    
    try:
        from classifiers.video_classifier import VideoClassifier
        
        # Initialize classifier
        video_classifier = VideoClassifier()
        print("✅ Video classifier initialized successfully")
        
        # Test with bytes (simulating file upload)
        test_bytes = b"fake video data for testing"
        sentiment, confidence = video_classifier.predict(test_bytes)
        
        print(f"📊 Video Test Result:")
        print(f"   Sentiment: {sentiment}")
        print(f"   Confidence: {confidence:.3f}")
        
        # Test with file path if video files exist
        video_files = [
            "test_files/video/positive_bright_video.mp4",
            "test_files/video/negative_dark_video.mp4",
            "test_files/video/neutral_balanced_video.mp4"
        ]
        
        for video_file in video_files:
            if os.path.exists(video_file):
                print(f"\n🎬 Testing with file: {os.path.basename(video_file)}")
                sentiment, confidence = video_classifier.predict(video_file)
                print(f"   Sentiment: {sentiment}")
                print(f"   Confidence: {confidence:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Video classifier test failed: {e}")
        return False

def test_text_classifier():
    """Test the text classifier for comparison"""
    print("\n📝 Testing Text Classifier...")
    
    try:
        from classifiers.text_classifier import TextClassifier
        
        # Initialize classifier
        text_classifier = TextClassifier()
        print("✅ Text classifier initialized successfully")
        
        # Test with sample texts
        test_texts = [
            "I love this amazing product!",
            "This is terrible and disappointing.",
            "It's okay, nothing special."
        ]
        
        for text in test_texts:
            print(f"\n📝 Testing: '{text}'")
            result = text_classifier.predict(text)
            
            if isinstance(result, dict):
                sentiment = result.get('sentiment', 'unknown')
                confidence = result.get('confidence', 0.0)
            else:
                sentiment, confidence = result
            
            print(f"   Sentiment: {sentiment}")
            print(f"   Confidence: {confidence:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Text classifier test failed: {e}")
        return False

def main():
    """Run all classifier tests"""
    print("🧪 Testing Multimodal Sentiment Classifiers")
    print("=" * 50)
    
    results = []
    
    # Test each classifier
    results.append(("Audio", test_audio_classifier()))
    results.append(("Video", test_video_classifier()))
    results.append(("Text", test_text_classifier()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    for classifier_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {classifier_name} Classifier: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All classifiers are working correctly!")
        print("\n💡 Next steps:")
        print("   1. Start the server: python start_server.py")
        print("   2. Test via API: python test_files/test_classifiers.py")
        print("   3. Use the web dashboard: http://localhost:8000/dashboard")
    else:
        print("\n⚠️  Some classifiers failed. Check the error messages above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
