#!/usr/bin/env python3
"""
Direct API runner that imports and runs the FastAPI app
Works even when uvicorn module import fails
"""

import sys
import subprocess
import time
import webbrowser
import threading

def install_and_import_uvicorn():
    """Install uvicorn and import it"""
    try:
        # Try to import first
        import uvicorn
        return uvicorn
    except ImportError:
        print("🔧 Installing uvicorn...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "uvicorn[standard]", "fastapi", "python-multipart"
            ])
            # Try importing again
            import uvicorn
            return uvicorn
        except Exception as e:
            print(f"❌ Failed to install/import uvicorn: {e}")
            return None

def open_browser_delayed():
    """Open browser after a delay"""
    time.sleep(3)
    webbrowser.open('http://127.0.0.1:8000/docs')

def main():
    print("🎭 Multimodal Sentiment Analysis API")
    print("=" * 40)
    
    # Install and import uvicorn
    uvicorn = install_and_import_uvicorn()
    
    if uvicorn is None:
        print("❌ Could not get uvicorn working")
        print("🔄 Try running: python simple_server.py")
        return
    
    # Import the FastAPI app
    try:
        from api import app
        print("✅ FastAPI app imported successfully")
    except Exception as e:
        print(f"❌ Error importing API: {e}")
        return
    
    # Start browser in background
    browser_thread = threading.Thread(target=open_browser_delayed)
    browser_thread.daemon = True
    browser_thread.start()
    
    print("🚀 Starting server...")
    print("📍 API: http://127.0.0.1:8000")
    print("📚 Docs: http://127.0.0.1:8000/docs")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 40)
    
    try:
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=False,  # Disable reload to avoid issues
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()
