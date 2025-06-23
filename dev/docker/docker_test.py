# docker_test.py - Test Docker deployment

import subprocess
import time
import requests
import sys

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n🔧 {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success: {description}")
            if result.stdout:
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Failed: {description}")
            print(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_docker_deployment():
    """Test Docker deployment process"""
    print("🚀 TESTING DOCKER DEPLOYMENT")
    print("=" * 50)
    
    # Test 1: Build Docker image
    if not run_command("docker build -t multimodal-sentiment:test .", "Building Docker image"):
        return False
    
    # Test 2: Start container
    if not run_command("docker run -d --name sentiment-test -p 8002:8000 multimodal-sentiment:test", "Starting container"):
        return False
    
    # Test 3: Wait for container to start
    print("\n⏳ Waiting for container to start...")
    time.sleep(10)
    
    # Test 4: Check container status
    if not run_command("docker ps | grep sentiment-test", "Checking container status"):
        return False
    
    # Test 5: Test API health
    try:
        print("\n🔍 Testing API health...")
        response = requests.get("http://localhost:8002/health", timeout=10)
        if response.status_code == 200:
            print("✅ API health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API health check failed: {e}")
        return False
    
    # Test 6: Test text prediction
    try:
        print("\n🧪 Testing text prediction...")
        response = requests.post(
            "http://localhost:8002/predict/text",
            json={"text": "Docker deployment test!"},
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            print("✅ Text prediction test passed")
            print(f"Result: {result['sentiment']} ({result['confidence']:.2f})")
        else:
            print(f"❌ Text prediction test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Text prediction test failed: {e}")
        return False
    
    # Cleanup
    print("\n🧹 Cleaning up...")
    run_command("docker stop sentiment-test", "Stopping container")
    run_command("docker rm sentiment-test", "Removing container")
    
    print("\n🎉 DOCKER DEPLOYMENT TEST COMPLETED SUCCESSFULLY!")
    return True

def test_docker_compose():
    """Test Docker Compose deployment"""
    print("\n🐳 TESTING DOCKER COMPOSE DEPLOYMENT")
    print("=" * 50)
    
    # Test 1: Start with Docker Compose
    if not run_command("docker-compose --profile cpu up -d", "Starting with Docker Compose"):
        return False
    
    # Test 2: Wait for services
    print("\n⏳ Waiting for services to start...")
    time.sleep(15)
    
    # Test 3: Check services
    if not run_command("docker-compose ps", "Checking services status"):
        return False
    
    # Test 4: Test API
    try:
        print("\n🔍 Testing Docker Compose API...")
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("✅ Docker Compose API test passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Docker Compose API test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Docker Compose API test failed: {e}")
        return False
    
    # Cleanup
    print("\n🧹 Cleaning up Docker Compose...")
    run_command("docker-compose down", "Stopping Docker Compose")
    
    print("\n🎉 DOCKER COMPOSE TEST COMPLETED SUCCESSFULLY!")
    return True

if __name__ == "__main__":
    print("🎯 DOCKER DEPLOYMENT TESTING SUITE")
    print("=" * 60)
    
    # Check if Docker is available
    if not run_command("docker --version", "Checking Docker installation"):
        print("❌ Docker is not available. Please install Docker first.")
        sys.exit(1)
    
    # Check if Docker Compose is available
    if not run_command("docker-compose --version", "Checking Docker Compose installation"):
        print("❌ Docker Compose is not available. Please install Docker Compose first.")
        sys.exit(1)
    
    # Run tests
    success = True
    
    # Test individual Docker build
    if not test_docker_deployment():
        success = False
    
    # Test Docker Compose
    if not test_docker_compose():
        success = False
    
    if success:
        print("\n🏆 ALL DOCKER TESTS PASSED!")
        print("✅ Docker deployment is ready for production")
    else:
        print("\n❌ SOME DOCKER TESTS FAILED!")
        print("Please check the errors above and fix them")
        sys.exit(1)
