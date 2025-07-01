#!/usr/bin/env python3
"""
Alternative API runner with multiple startup methods
"""

import sys
import os

def method1_uvicorn_basic():
    """Method 1: Basic uvicorn without reload"""
    print("🚀 Method 1: Starting with basic uvicorn...")
    os.system("python -m uvicorn api:app --host 127.0.0.1 --port 8000 --workers 1")

def method2_uvicorn_different_port():
    """Method 2: Different port"""
    print("🚀 Method 2: Starting with different port...")
    os.system("python -m uvicorn api:app --host 127.0.0.1 --port 9000 --workers 1")

def method3_direct_run():
    """Method 3: Direct Python execution"""
    print("🚀 Method 3: Starting with direct Python execution...")
    os.system("python api.py")

def method4_gunicorn():
    """Method 4: Try with gunicorn if available"""
    print("🚀 Method 4: Installing and trying gunicorn...")
    os.system("pip install gunicorn")
    os.system("gunicorn api:app -w 1 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000")

def method5_development_server():
    """Method 5: Simple development server"""
    print("🚀 Method 5: Creating simple development server...")
    
    try:
        from api import app
        import uvicorn
        
        print("Starting development server on http://127.0.0.1:8000")
        print("Press Ctrl+C to stop")
        
        # Try with minimal configuration
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=8000,
            reload=False,
            workers=1,
            access_log=False
        )
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("🎭 Multimodal Sentiment Analysis API - Startup Methods")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        method = sys.argv[1]
        if method == "1":
            method1_uvicorn_basic()
        elif method == "2":
            method2_uvicorn_different_port()
        elif method == "3":
            method3_direct_run()
        elif method == "4":
            method4_gunicorn()
        elif method == "5":
            method5_development_server()
        else:
            print("Invalid method. Use 1, 2, 3, 4, or 5")
    else:
        print("Available startup methods:")
        print("1. Basic uvicorn (port 8000)")
        print("2. Different port (port 9000)")
        print("3. Direct Python execution")
        print("4. Gunicorn with uvicorn worker")
        print("5. Development server")
        print()
        print("Usage: python run_api.py [1|2|3|4|5]")
        print("Example: python run_api.py 2")
