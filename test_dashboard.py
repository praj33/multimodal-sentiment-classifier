# test_dashboard.py - Test the dashboard API

import requests
import json

def test_api():
    base_url = "http://localhost:8001"
    
    print("🧪 Testing Dashboard API...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health Check: {response.json()}")
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return
    
    # Test text prediction
    try:
        data = {"text": "I love this amazing product!"}
        response = requests.post(f"{base_url}/predict/text", json=data)
        result = response.json()
        print(f"✅ Text Prediction: {result}")
    except Exception as e:
        print(f"❌ Text Prediction Failed: {e}")
    
    # Test with negative sentiment
    try:
        data = {"text": "This is terrible and awful!"}
        response = requests.post(f"{base_url}/predict/text", json=data)
        result = response.json()
        print(f"✅ Negative Text: {result}")
    except Exception as e:
        print(f"❌ Negative Text Failed: {e}")
    
    # Test with neutral sentiment
    try:
        data = {"text": "The weather is cloudy today."}
        response = requests.post(f"{base_url}/predict/text", json=data)
        result = response.json()
        print(f"✅ Neutral Text: {result}")
    except Exception as e:
        print(f"❌ Neutral Text Failed: {e}")
    
    print("\n🌐 Dashboard URLs:")
    print(f"📊 Web Dashboard: {base_url}/dashboard")
    print(f"📚 API Documentation: {base_url}/docs")
    print(f"🔍 Health Check: {base_url}/health")

if __name__ == "__main__":
    test_api()
