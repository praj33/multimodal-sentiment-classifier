#!/usr/bin/env python3
"""
Universal server starter that works in any Python environment
No external dependencies required
"""

import sys
import subprocess
import os

def install_uvicorn():
    """Install uvicorn if not available"""
    print("🔧 Installing uvicorn...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "uvicorn[standard]", "fastapi", "python-multipart"])
        print("✅ uvicorn installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install uvicorn")
        return False

def check_uvicorn():
    """Check if uvicorn is available"""
    try:
        import uvicorn
        print("✅ uvicorn is available")
        return True
    except ImportError:
        print("⚠️  uvicorn not found")
        return False

def start_with_uvicorn():
    """Start server with uvicorn"""
    try:
        import uvicorn
        print("🚀 Starting server with uvicorn...")
        print("📍 Server will be available at: http://127.0.0.1:8000")
        print("📚 API Documentation: http://127.0.0.1:8000/docs")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 50)
        
        uvicorn.run(
            "api:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error starting uvicorn: {e}")
        return False
    return True

def start_with_simple_server():
    """Fallback to simple HTTP server"""
    print("🔄 Falling back to simple HTTP server...")
    try:
        import simple_server
        simple_server.start_server(8000)
    except Exception as e:
        print(f"❌ Error starting simple server: {e}")
        return False
    return True

def main():
    print("🎭 Multimodal Sentiment Analysis Server Starter")
    print("=" * 50)
    
    # Check current environment
    print(f"🐍 Python: {sys.executable}")
    print(f"📁 Working Directory: {os.getcwd()}")
    
    # Try to use uvicorn
    if check_uvicorn():
        if start_with_uvicorn():
            return
    
    # Try to install uvicorn
    print("\n🔧 Attempting to install uvicorn...")
    if install_uvicorn():
        if start_with_uvicorn():
            return
    
    # Fallback to simple server
    print("\n🔄 Using fallback simple server...")
    start_with_simple_server()

if __name__ == "__main__":
    main()
