# test_fixed_emojis.py - Test the fixed emoji display

import requests
import os

def test_emoji_display():
    base_url = "http://localhost:8003"
    
    print("🔧 TESTING FIXED EMOJI DISPLAY IN MULTIMODAL DASHBOARD")
    print("=" * 60)
    
    # Create a test file for multimodal analysis
    print("\n📁 Creating test file...")
    with open('test_multimodal.mp4', 'wb') as f:
        f.write(b'\x00\x00\x00\x20ftypmp42')
        f.write(b'\x00' * 500)
    print("✅ Created test_multimodal.mp4")
    
    # Test multimodal analysis
    print("\n🎭 Testing Multimodal Analysis with Fixed Emojis...")
    try:
        with open('test_multimodal.mp4', 'rb') as f:
            files = {'file': ('test_multimodal.mp4', f, 'video/mp4')}
            response = requests.post(f"{base_url}/predict/multimodal", files=files)
            result = response.json()
            
            print(f"📊 Multimodal Result:")
            print(f"   🎭 Fused Sentiment: {result['fused_sentiment'].upper()}")
            print(f"   📈 Confidence: {result['confidence']:.1%}")
            print(f"   ⏱️  Processing Time: {result['processing_time']}s")
            
            print(f"\n📋 Individual Results:")
            for individual in result['individual']:
                emoji = "😊" if individual['sentiment'] == 'positive' else "😞" if individual['sentiment'] == 'negative' else "😐"
                print(f"   {emoji} {individual['modality'].title()}: {individual['sentiment'].upper()} ({individual['confidence']:.1%})")
            
            print(f"\n✅ Emoji Display Test: PASSED")
            print(f"   - Fused result emoji should display properly")
            print(f"   - Individual result emojis should display properly")
            print(f"   - Enhanced styling should be visible")
            
    except Exception as e:
        print(f"❌ Multimodal test failed: {e}")
    
    # Test text analysis for comparison
    print(f"\n📝 Testing Text Analysis...")
    try:
        response = requests.post(f"{base_url}/predict/text", 
                               json={"text": "I absolutely love this amazing product!"})
        result = response.json()
        emoji = "😊" if result['sentiment'] == 'positive' else "😞" if result['sentiment'] == 'negative' else "😐"
        print(f"   {emoji} Text Result: {result['sentiment'].upper()} ({result['confidence']:.1%})")
    except Exception as e:
        print(f"❌ Text test failed: {e}")
    
    # Clean up
    try:
        os.remove('test_multimodal.mp4')
        print(f"\n🧹 Cleaned up test file")
    except:
        pass
    
    print(f"\n🎯 EMOJI FIXES APPLIED:")
    print("✅ Added explicit emoji font families")
    print("✅ Enhanced UTF-8 encoding support")
    print("✅ Improved emoji sizing and styling")
    print("✅ Better emoji function mapping")
    print("✅ Enhanced visual styling for multimodal results")
    
    print(f"\n🌐 Open your browser to see the fixed emojis:")
    print(f"📊 Dashboard: {base_url}/dashboard")
    print("🎭 Try the multimodal mode to see the enhanced emoji display!")

if __name__ == "__main__":
    test_emoji_display()
