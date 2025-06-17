# verify_emoji_fix.py - Verify the headline emoji fix

import requests
import time

def verify_emoji_fix():
    print("🔧 VERIFYING HEADLINE EMOJI FIX")
    print("=" * 50)
    
    # Test different ports to find the running server
    ports = [8003, 8004, 8002, 8001, 8000]
    working_port = None
    
    for port in ports:
        try:
            response = requests.get(f'http://localhost:{port}/health', timeout=2)
            if response.status_code == 200:
                working_port = port
                print(f"✅ Found running server on port {port}")
                break
        except:
            continue
    
    if not working_port:
        print("❌ No running server found. Please start the dashboard first.")
        return
    
    base_url = f"http://localhost:{working_port}"
    
    print(f"\n🌐 DASHBOARD URLS:")
    print(f"📊 Fixed Dashboard: {base_url}/dashboard")
    print(f"📚 API Documentation: {base_url}/docs")
    
    print(f"\n🔧 EMOJI FIXES APPLIED:")
    print("✅ Separated emoji from gradient text in headline")
    print("✅ Added explicit emoji font family CSS")
    print("✅ Enhanced emoji styling with proper sizing")
    print("✅ Fixed emoji display in mode buttons")
    print("✅ Added font-variant-emoji for better rendering")
    
    print(f"\n🎭 HEADLINE STRUCTURE:")
    print("Before: <h1 class='gradient-text'>🎭 Multimodal AI Sentiment Analyzer</h1>")
    print("After:  <h1><span class='emoji'>🎭</span><span class='gradient-text'>Multimodal AI...</span></h1>")
    
    print(f"\n📝 CSS ENHANCEMENTS:")
    print("✅ .emoji { font-family: 'Apple Color Emoji', 'Segoe UI Emoji'... }")
    print("✅ .emoji { font-size: 3rem; display: inline-block; }")
    print("✅ * { font-variant-emoji: emoji; }")
    
    # Test the API to make sure it's working
    try:
        response = requests.post(f"{base_url}/predict/text", 
                               json={"text": "Testing emoji fix!"})
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ API Test: {result['sentiment']} ({result['confidence']:.1%})")
        else:
            print(f"\n⚠️  API Test: HTTP {response.status_code}")
    except Exception as e:
        print(f"\n❌ API Test Failed: {e}")
    
    print(f"\n🎯 WHAT TO CHECK IN BROWSER:")
    print("1. 🎭 emoji should be visible and large in the headline")
    print("2. 'Multimodal AI Sentiment Analyzer' should have gradient colors")
    print("3. Mode buttons should show emojis: 📝 🎵 🎥 🎭")
    print("4. All emojis should render consistently across browsers")
    
    print(f"\n🌐 Open your browser to: {base_url}/dashboard")
    print("🔍 Check if the headline emoji 🎭 is now displaying properly!")

if __name__ == "__main__":
    verify_emoji_fix()
