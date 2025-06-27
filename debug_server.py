#!/usr/bin/env python3
"""
Debug server that writes to file to bypass terminal issues
"""

import sys
import time
import traceback

def log_to_file(message):
    """Write log message to file"""
    with open("server_debug.log", "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        f.flush()

def test_uvicorn():
    """Test uvicorn startup with file logging"""
    try:
        log_to_file("=== UVICORN DEBUG TEST STARTED ===")
        log_to_file("Step 1: Importing modules...")
        
        import uvicorn
        log_to_file("✅ uvicorn imported successfully")
        
        from fastapi import FastAPI
        log_to_file("✅ FastAPI imported successfully")
        
        # Create simple app
        app = FastAPI()
        
        @app.get("/")
        def root():
            return {"message": "test"}
        
        log_to_file("✅ FastAPI app created successfully")
        
        log_to_file("Step 2: Starting uvicorn server...")
        log_to_file("This is where it might hang...")
        
        # Try to start server
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="debug"
        )
        
        log_to_file("✅ Server started successfully")
        
    except Exception as e:
        log_to_file(f"❌ Error occurred: {str(e)}")
        log_to_file(f"❌ Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    # Clear previous log
    with open("server_debug.log", "w") as f:
        f.write("")
    
    log_to_file("Starting debug test...")
    test_uvicorn()
