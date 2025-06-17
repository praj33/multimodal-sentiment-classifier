# multimodal_demo.py - Complete multimodal dashboard demonstration

import requests
import os
import time

def create_test_files():
    """Create test audio and video files for demonstration"""
    
    # Create mock audio file (WAV format)
    with open('demo_audio.wav', 'wb') as f:
        # WAV header + some data
        f.write(b'RIFF')
        f.write((1000).to_bytes(4, 'little'))  # File size
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write((16).to_bytes(4, 'little'))   # Format chunk size
        f.write(b'\x01\x00\x01\x00')         # Audio format and channels
        f.write((44100).to_bytes(4, 'little')) # Sample rate
        f.write(b'\x00' * 100)               # Audio data
    
    # Create mock video file (MP4-like)
    with open('demo_video.mp4', 'wb') as f:
        # MP4 header + some data
        f.write(b'\x00\x00\x00\x20ftypmp42')
        f.write(b'\x00' * 500)  # Video data
    
    print("✅ Created test files: demo_audio.wav, demo_video.mp4")

def test_multimodal_dashboard():
    base_url = "http://localhost:8003"
    
    print("🎭 COMPLETE MULTIMODAL DASHBOARD DEMONSTRATION")
    print("=" * 70)
    
    # Check server health
    print("\n🔍 STEP 1: Server Health Check")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Server Status: {response.json()}")
    except Exception as e:
        print(f"❌ Server Error: {e}")
        return
    
    print(f"\n🌐 STEP 2: Dashboard URLs")
    print(f"📊 Enhanced Dashboard: {base_url}/dashboard")
    print(f"📚 API Documentation: {base_url}/docs")
    
    # Test Text Analysis
    print(f"\n📝 STEP 3: Text Sentiment Analysis")
    print("-" * 50)
    text_tests = [
        "I absolutely love this amazing product!",
        "This is terrible and disappointing!",
        "The weather is okay today."
    ]
    
    for text in text_tests:
        try:
            response = requests.post(f"{base_url}/predict/text", 
                                   json={"text": text})
            result = response.json()
            emoji = "😊" if result['sentiment'] == 'positive' else "😞" if result['sentiment'] == 'negative' else "😐"
            print(f"{emoji} \"{text}\" → {result['sentiment'].upper()} ({result['confidence']:.1%})")
        except Exception as e:
            print(f"❌ Text test failed: {e}")
    
    # Create test files
    print(f"\n📁 STEP 4: Creating Test Media Files")
    create_test_files()
    
    # Test Audio Analysis
    print(f"\n🎵 STEP 5: Audio Sentiment Analysis")
    print("-" * 50)
    try:
        with open('demo_audio.wav', 'rb') as f:
            files = {'file': ('demo_audio.wav', f, 'audio/wav')}
            response = requests.post(f"{base_url}/predict/audio", files=files)
            result = response.json()
            emoji = "😊" if result['sentiment'] == 'positive' else "😞" if result['sentiment'] == 'negative' else "😐"
            print(f"{emoji} Audio Analysis → {result['sentiment'].upper()} ({result['confidence']:.1%})")
            print(f"   📏 File Size: {result['file_size']} bytes")
            print(f"   ⏱️  Processing Time: {result['processing_time']}s")
    except Exception as e:
        print(f"❌ Audio test failed: {e}")
    
    # Test Video Analysis
    print(f"\n🎥 STEP 6: Video Sentiment Analysis")
    print("-" * 50)
    try:
        with open('demo_video.mp4', 'rb') as f:
            files = {'file': ('demo_video.mp4', f, 'video/mp4')}
            response = requests.post(f"{base_url}/predict/video", files=files)
            result = response.json()
            emoji = "😊" if result['sentiment'] == 'positive' else "😞" if result['sentiment'] == 'negative' else "😐"
            print(f"{emoji} Video Analysis → {result['sentiment'].upper()} ({result['confidence']:.1%})")
            print(f"   📏 File Size: {result['file_size']} bytes")
            print(f"   ⏱️  Processing Time: {result['processing_time']}s")
    except Exception as e:
        print(f"❌ Video test failed: {e}")
    
    # Test Multimodal Analysis
    print(f"\n🎭 STEP 7: Multimodal Fusion Analysis")
    print("-" * 50)
    try:
        with open('demo_video.mp4', 'rb') as f:
            files = {'file': ('demo_video.mp4', f, 'video/mp4')}
            response = requests.post(f"{base_url}/predict/multimodal", files=files)
            result = response.json()
            
            emoji = "😊" if result['fused_sentiment'] == 'positive' else "😞" if result['fused_sentiment'] == 'negative' else "😐"
            print(f"{emoji} Fused Result → {result['fused_sentiment'].upper()} ({result['confidence']:.1%})")
            print(f"   ⏱️  Total Processing: {result['processing_time']}s")
            
            print(f"   📊 Individual Modality Results:")
            for individual in result['individual']:
                ind_emoji = "😊" if individual['sentiment'] == 'positive' else "😞" if individual['sentiment'] == 'negative' else "😐"
                print(f"      {ind_emoji} {individual['modality'].title()}: {individual['sentiment']} ({individual['confidence']:.1%})")
                
    except Exception as e:
        print(f"❌ Multimodal test failed: {e}")
    
    # Dashboard Features Summary
    print(f"\n🎯 STEP 8: Enhanced Dashboard Features")
    print("-" * 50)
    print("✅ Text Analysis - Real-time sentiment from text input")
    print("✅ Audio Upload - Drag & drop .wav, .mp3, .m4a files")
    print("✅ Video Upload - Drag & drop .mp4, .avi, .mov files")
    print("✅ Multimodal Fusion - Combined analysis from multiple sources")
    print("✅ Mode Selection - Easy switching between analysis types")
    print("✅ File Type Validation - Automatic file format detection")
    print("✅ Progress Visualization - Animated confidence bars")
    print("✅ Individual Results - Breakdown of multimodal analysis")
    print("✅ Professional UI - Modern, responsive design")
    print("✅ Quick Test Examples - One-click sentiment testing")
    
    # Usage Instructions
    print(f"\n🚀 STEP 9: How to Use the Enhanced Dashboard")
    print("-" * 50)
    print("1. 🌐 Open browser → http://localhost:8003/dashboard")
    print("2. 📝 For Text: Select 'Text' mode, enter text, click Analyze")
    print("3. 🎵 For Audio: Select 'Audio' mode, upload .wav/.mp3 file")
    print("4. 🎥 For Video: Select 'Video' mode, upload .mp4/.avi file")
    print("5. 🎭 For Multimodal: Select 'Multi' mode, upload media file")
    print("6. 📊 View results with confidence scores and progress bars")
    print("7. 🔄 Try different files and modes to test all features")
    
    # Clean up test files
    print(f"\n🧹 STEP 10: Cleanup")
    try:
        os.remove('demo_audio.wav')
        os.remove('demo_video.mp4')
        print("✅ Cleaned up test files")
    except:
        print("⚠️  Some test files may still exist")
    
    print(f"\n🎉 MULTIMODAL DASHBOARD DEMONSTRATION COMPLETE!")
    print("=" * 70)
    print(f"🌐 Your enhanced dashboard is live at: {base_url}/dashboard")
    print("🎭 Ready for complete multimodal sentiment analysis!")

if __name__ == "__main__":
    test_multimodal_dashboard()
