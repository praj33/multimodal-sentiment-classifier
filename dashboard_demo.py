# dashboard_demo.py - Live Dashboard Demonstration

import requests
import json
import time

def demo_dashboard():
    base_url = "http://localhost:8002"
    
    print("🎬 LIVE DASHBOARD DEMONSTRATION")
    print("=" * 60)
    
    # Check server health
    print("\n🔍 STEP 1: Checking Server Health...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Server Status: {response.json()}")
    except Exception as e:
        print(f"❌ Server Error: {e}")
        return
    
    print("\n🌐 STEP 2: Dashboard URLs")
    print(f"📊 Web Dashboard: {base_url}/dashboard")
    print(f"📚 API Documentation: {base_url}/docs")
    print(f"🔍 Health Check: {base_url}/health")
    
    # Test different sentiments
    test_cases = [
        {
            "name": "POSITIVE SENTIMENT",
            "text": "I absolutely love this amazing product! It is fantastic and wonderful!",
            "emoji": "😊"
        },
        {
            "name": "NEGATIVE SENTIMENT", 
            "text": "This is terrible and awful! I hate it completely!",
            "emoji": "😞"
        },
        {
            "name": "NEUTRAL SENTIMENT",
            "text": "The weather is cloudy today. It might rain later.",
            "emoji": "😐"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 STEP {i+2}: Testing {test['name']}")
        print("-" * 50)
        print(f"Input Text: \"{test['text']}\"")
        
        try:
            response = requests.post(f"{base_url}/predict/text", 
                                   json={"text": test['text']})
            result = response.json()
            
            print(f"{test['emoji']} Result: {result['sentiment'].upper()}")
            print(f"📊 Confidence: {result['confidence']:.1%}")
            print(f"⏱️  Processing Time: {result['processing_time']}s")
            print(f"📏 Text Length: {result['text_length']} characters")
            print(f"🆔 Prediction ID: {result['prediction_id']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n🎯 STEP 6: Dashboard Features Summary")
    print("-" * 50)
    print("✅ Real-time sentiment analysis")
    print("✅ Confidence scoring with visual progress bar")
    print("✅ Emoji indicators (😊 😞 😐)")
    print("✅ Processing time measurement")
    print("✅ Professional web interface")
    print("✅ Responsive design")
    print("✅ Clean, modern UI")
    
    print(f"\n🚀 DASHBOARD IS LIVE AND READY!")
    print("=" * 60)
    print(f"🌐 Open your browser to: {base_url}/dashboard")
    print("📝 Enter any text and click 'Analyze Sentiment'")
    print("🎉 Enjoy your working Multimodal Sentiment Analysis System!")

if __name__ == "__main__":
    demo_dashboard()
