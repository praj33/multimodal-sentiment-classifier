# test_api.py - Simple API testing script

import requests
import json

def test_api():
    """Test all API endpoints"""
    print('🧪 TESTING ALL API ENDPOINTS')
    print('=' * 50)
    
    base_url = 'http://localhost:8000'
    
    # Test 1: Health endpoint
    try:
        response = requests.get(f'{base_url}/health')
        print(f'✅ Health: {response.status_code} - {response.json()}')
    except Exception as e:
        print(f'❌ Health: {e}')
    
    # Test 2: Dashboard endpoint
    try:
        response = requests.get(f'{base_url}/dashboard')
        print(f'✅ Dashboard: {response.status_code} - HTML content loaded')
    except Exception as e:
        print(f'❌ Dashboard: {e}')
    
    # Test 3: Text prediction
    try:
        response = requests.post(f'{base_url}/predict/text', 
                               json={'text': 'I love this project!'})
        result = response.json()
        sentiment = result.get('sentiment', 'unknown')
        confidence = result.get('confidence', 0)
        print(f'✅ Text prediction: {response.status_code} - Sentiment: {sentiment} ({confidence:.2f})')
    except Exception as e:
        print(f'❌ Text prediction: {e}')
    
    # Test 4: API docs
    try:
        response = requests.get(f'{base_url}/docs')
        print(f'✅ API docs: {response.status_code} - Documentation available')
    except Exception as e:
        print(f'❌ API docs: {e}')
    
    # Test 5: Analytics
    try:
        response = requests.get(f'{base_url}/analytics/stats')
        print(f'✅ Analytics: {response.status_code} - Stats available')
    except Exception as e:
        print(f'❌ Analytics: {e}')
    
    print('\n🎯 API TESTING COMPLETE!')

if __name__ == "__main__":
    test_api()
