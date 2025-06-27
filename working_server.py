#!/usr/bin/env python3
"""
Working server solution that bypasses uvicorn.run() hanging issue
"""

import asyncio
import sys
import time
import signal
from typing import Optional

def log_message(message):
    """Print with timestamp"""
    print(f"[{time.strftime('%H:%M:%S')}] {message}")
    sys.stdout.flush()

async def run_server_async():
    """Run server using asyncio approach"""
    try:
        log_message("🚀 Starting Multimodal Sentiment Analysis API...")
        log_message("📦 Loading modules...")
        
        # Import uvicorn and create server
        import uvicorn
        from api import app
        
        log_message("✅ Modules loaded successfully")
        log_message("🌐 Creating server configuration...")
        
        # Create server config
        config = uvicorn.Config(
            app=app,
            host="127.0.0.1",
            port=8000,
            log_level="info",
            access_log=True,
            reload=False
        )
        
        log_message("✅ Server configuration created")
        log_message("🚀 Starting server...")
        
        # Create and start server
        server = uvicorn.Server(config)
        
        log_message("=" * 60)
        log_message("🎭 Multimodal Sentiment Analysis API")
        log_message("🌐 Server URL: http://127.0.0.1:8000")
        log_message("📚 API Docs: http://127.0.0.1:8000/docs")
        log_message("🎯 Dashboard: http://127.0.0.1:8000/dashboard")
        log_message("=" * 60)
        log_message("✅ Server is starting... (Press Ctrl+C to stop)")
        
        # Start the server
        await server.serve()
        
    except KeyboardInterrupt:
        log_message("🛑 Server stopped by user")
    except Exception as e:
        log_message(f"❌ Server error: {e}")
        import traceback
        log_message(f"❌ Traceback: {traceback.format_exc()}")

def run_with_subprocess():
    """Alternative method using subprocess"""
    import subprocess
    import os
    
    log_message("🚀 Method 2: Using subprocess approach...")
    
    try:
        # Set environment variables
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'
        
        # Run uvicorn as subprocess
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "api:app", 
            "--host", "127.0.0.1", 
            "--port", "8000",
            "--reload"
        ]
        
        log_message(f"🔧 Running command: {' '.join(cmd)}")
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,
            env=env
        )
        
        log_message("✅ Subprocess started, monitoring output...")
        
        # Monitor output
        for line in iter(process.stdout.readline, ''):
            if line:
                print(line.rstrip())
                sys.stdout.flush()
        
        process.wait()
        
    except KeyboardInterrupt:
        log_message("🛑 Stopping subprocess...")
        process.terminate()
        process.wait()
    except Exception as e:
        log_message(f"❌ Subprocess error: {e}")

def run_with_threading():
    """Method 3: Using threading"""
    import threading
    import uvicorn
    
    log_message("🚀 Method 3: Using threading approach...")
    
    def server_thread():
        try:
            from api import app
            uvicorn.run(
                app,
                host="127.0.0.1",
                port=8000,
                log_level="info"
            )
        except Exception as e:
            log_message(f"❌ Thread error: {e}")
    
    # Start server in thread
    thread = threading.Thread(target=server_thread, daemon=True)
    thread.start()
    
    log_message("✅ Server thread started")
    log_message("🌐 Server should be available at: http://127.0.0.1:8000")
    log_message("🛑 Press Ctrl+C to stop")
    
    try:
        # Keep main thread alive
        while thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        log_message("🛑 Stopping server...")

def main():
    """Main function with multiple startup methods"""
    log_message("🎭 Multimodal Sentiment Analysis API - Startup Solutions")
    log_message("=" * 60)
    
    if len(sys.argv) > 1:
        method = sys.argv[1]
        
        if method == "async":
            log_message("📋 Using async method...")
            asyncio.run(run_server_async())
        elif method == "subprocess":
            log_message("📋 Using subprocess method...")
            run_with_subprocess()
        elif method == "thread":
            log_message("📋 Using threading method...")
            run_with_threading()
        else:
            log_message("❌ Invalid method. Use: async, subprocess, or thread")
    else:
        log_message("📋 Available methods:")
        log_message("  python working_server.py async      - Async approach")
        log_message("  python working_server.py subprocess - Subprocess approach")
        log_message("  python working_server.py thread     - Threading approach")
        log_message("")
        log_message("🎯 Recommended: Try 'subprocess' first")

if __name__ == "__main__":
    main()
