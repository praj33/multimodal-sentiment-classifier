#!/usr/bin/env python3
"""
Deployment script for Multimodal Sentiment Analysis Service
"""

import os
import sys
import subprocess
import argparse
import time
import requests

def run_command(command, check=True):
    """Run a shell command"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if check and result.returncode != 0:
        print(f"Error running command: {command}")
        print(f"Error output: {result.stderr}")
        sys.exit(1)
    
    return result

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    # Check if pip is available
    try:
        subprocess.run(["pip", "--version"], check=True, capture_output=True)
        print("✅ pip is available")
    except subprocess.CalledProcessError:
        print("❌ pip is not available")
        sys.exit(1)
    
    # Check if Docker is available (optional)
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        print("✅ Docker is available")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Docker is not available (optional for containerized deployment)")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    run_command("pip install -r requirements.txt")
    print("✅ Dependencies installed")

def setup_directories():
    """Create necessary directories"""
    print("📁 Setting up directories...")
    
    directories = ["logs", "temp", "uploads"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   Created: {directory}/")
    
    print("✅ Directories created")

def test_installation():
    """Test if the installation works"""
    print("🧪 Testing installation...")
    
    # Test imports
    try:
        from classifiers.text_classifier import TextClassifier
        from classifiers.audio_classifier import AudioClassifier
        from classifiers.video_classifier import VideoClassifier
        from fusion.fusion_engine import FusionEngine
        from logging_system import sentiment_logger
        print("✅ All modules import successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test model initialization
    try:
        text_model = TextClassifier()
        print("✅ Text classifier initialized")
    except Exception as e:
        print(f"❌ Text classifier error: {e}")
        return False
    
    return True

def start_api_server(port=8000, host="127.0.0.1"):
    """Start the API server"""
    print(f"🚀 Starting API server on {host}:{port}...")
    
    command = f"uvicorn api:app --host {host} --port {port}"
    print(f"Command: {command}")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run(command, shell=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")

def wait_for_api(url="http://127.0.0.1:8000", timeout=30):
    """Wait for API to be ready"""
    print(f"⏳ Waiting for API at {url}...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("✅ API is ready")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(2)
    
    print("❌ API did not start within timeout")
    return False

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    
    try:
        result = subprocess.run([sys.executable, "test_sdk.py"], 
                              capture_output=True, text=True, timeout=60)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("❌ Some tests failed")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Tests timed out")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def deploy_docker():
    """Deploy using Docker"""
    print("🐳 Deploying with Docker...")
    
    # Build image
    print("Building Docker image...")
    run_command("docker build -t sentiment-api .")
    
    # Stop existing container if running
    print("Stopping existing container...")
    run_command("docker stop sentiment-api", check=False)
    run_command("docker rm sentiment-api", check=False)
    
    # Run new container
    print("Starting new container...")
    run_command("docker run -d --name sentiment-api -p 8000:8000 sentiment-api")
    
    # Wait for container to be ready
    if wait_for_api():
        print("✅ Docker deployment successful")
        return True
    else:
        print("❌ Docker deployment failed")
        return False

def deploy_docker_compose():
    """Deploy using Docker Compose"""
    print("🐳 Deploying with Docker Compose...")
    
    # Stop existing services
    run_command("docker-compose down", check=False)
    
    # Start services
    run_command("docker-compose up -d --build")
    
    # Wait for services to be ready
    if wait_for_api("http://127.0.0.1:80"):  # nginx proxy
        print("✅ Docker Compose deployment successful")
        return True
    else:
        print("❌ Docker Compose deployment failed")
        return False

def main():
    parser = argparse.ArgumentParser(description="Deploy Multimodal Sentiment Analysis Service")
    parser.add_argument("--mode", choices=["local", "docker", "docker-compose"], 
                       default="local", help="Deployment mode")
    parser.add_argument("--port", type=int, default=8000, help="Port for local deployment")
    parser.add_argument("--host", default="127.0.0.1", help="Host for local deployment")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument("--skip-deps", action="store_true", help="Skip dependency installation")
    
    args = parser.parse_args()
    
    print("🎭 Multimodal Sentiment Analysis Deployment")
    print("=" * 50)
    
    # Check dependencies
    docker_available = check_dependencies()
    
    if args.mode in ["docker", "docker-compose"] and not docker_available:
        print("❌ Docker is required for containerized deployment")
        sys.exit(1)
    
    # Install dependencies for local deployment
    if args.mode == "local" and not args.skip_deps:
        install_dependencies()
    
    # Setup directories
    setup_directories()
    
    # Test installation for local deployment
    if args.mode == "local":
        if not test_installation():
            print("❌ Installation test failed")
            sys.exit(1)
    
    # Deploy based on mode
    if args.mode == "local":
        print(f"\n🚀 Starting local deployment on {args.host}:{args.port}")
        print("API will be available at:")
        print(f"  - API: http://{args.host}:{args.port}")
        print(f"  - Docs: http://{args.host}:{args.port}/docs")
        print("\nTo test the deployment, run in another terminal:")
        print("  python test_sdk.py")
        print("\nTo start Streamlit demo:")
        print("  streamlit run app.py")
        
        start_api_server(port=args.port, host=args.host)
        
    elif args.mode == "docker":
        if deploy_docker():
            print("\n✅ Docker deployment successful!")
            print("API is available at: http://localhost:8000")
        else:
            sys.exit(1)
            
    elif args.mode == "docker-compose":
        if deploy_docker_compose():
            print("\n✅ Docker Compose deployment successful!")
            print("Services are available at:")
            print("  - API: http://localhost:8000")
            print("  - Load Balanced: http://localhost:80")
        else:
            sys.exit(1)
    
    # Run tests if not skipped
    if not args.skip_tests and args.mode != "local":
        time.sleep(5)  # Give services time to fully start
        if not run_tests():
            print("⚠️  Deployment successful but tests failed")

if __name__ == "__main__":
    main()
