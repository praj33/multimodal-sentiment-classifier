# start_api.py - Easy API startup script

import subprocess
import sys
import time
import requests
import os

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        import transformers
        import torch
        print("✅ All Python dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Installing missing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def start_api_server():
    """Start the API server"""
    print("🚀 Starting Multimodal Sentiment API...")
    print("=" * 50)
    
    # Check dependencies first
    if not check_dependencies():
        return False
    
    # Start the server
    try:
        print("🔧 Starting Uvicorn server...")
        print("📍 Server will be available at: http://localhost:8000")
        print("📊 Dashboard: http://localhost:8000/dashboard")
        print("📚 API Docs: http://localhost:8000/docs")
        print("\n⏳ Starting server (this may take a moment)...")
        
        # Start server with auto-reload for development
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "api:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

def test_api_after_start():
    """Test API endpoints after server starts"""
    print("🧪 Testing API endpoints...")
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running successfully!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Could not connect to API: {e}")
        return False

def main():
    """Main function"""
    print("🎯 MULTIMODAL SENTIMENT CLASSIFIER")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("api.py"):
        print("❌ Error: api.py not found!")
        print("Please run this script from the project directory:")
        print("cd C:\\Users\\PC\\multimodal_sentiment")
        return
    
    # Check if config exists
    if not os.path.exists("config/config.yaml"):
        print("❌ Error: config/config.yaml not found!")
        return
    
    print("✅ Project files found")
    print("✅ Configuration available")
    
    # Start the API server
    start_api_server()

if __name__ == "__main__":
    main()
