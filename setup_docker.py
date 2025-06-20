# setup_docker.py - Docker setup and troubleshooting script

import subprocess
import sys
import os
import time

def check_docker_installation():
    """Check if Docker is installed and accessible"""
    print("🔍 CHECKING DOCKER INSTALLATION")
    print("=" * 50)
    
    # Check if docker command is available
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker command failed")
            return False
    except FileNotFoundError:
        print("❌ Docker command not found in PATH")
        return False

def check_docker_compose():
    """Check if Docker Compose is available"""
    print("\n🔍 CHECKING DOCKER COMPOSE")
    print("=" * 50)
    
    # Try docker-compose command
    try:
        result = subprocess.run(["docker-compose", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker Compose found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    # Try docker compose (newer syntax)
    try:
        result = subprocess.run(["docker", "compose", "version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker Compose (new syntax) found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Docker Compose not found")
    return False

def check_docker_service():
    """Check if Docker service is running"""
    print("\n🔍 CHECKING DOCKER SERVICE")
    print("=" * 50)
    
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker service is running")
            return True
        else:
            print("❌ Docker service not running")
            print("Error:", result.stderr.strip())
            return False
    except Exception as e:
        print(f"❌ Could not check Docker service: {e}")
        return False

def start_docker_desktop():
    """Try to start Docker Desktop"""
    print("\n🚀 ATTEMPTING TO START DOCKER DESKTOP")
    print("=" * 50)
    
    # Common Docker Desktop paths
    docker_paths = [
        "C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe",
        "C:\\Users\\PC\\AppData\\Local\\Docker\\Docker Desktop.exe",
        "C:\\Program Files (x86)\\Docker\\Docker\\Docker Desktop.exe"
    ]
    
    for path in docker_paths:
        if os.path.exists(path):
            print(f"✅ Found Docker Desktop at: {path}")
            try:
                subprocess.Popen([path])
                print("🔄 Starting Docker Desktop...")
                print("⏳ Please wait 30-60 seconds for Docker to start")
                return True
            except Exception as e:
                print(f"❌ Failed to start Docker Desktop: {e}")
    
    print("❌ Docker Desktop not found in common locations")
    return False

def install_docker_instructions():
    """Provide Docker installation instructions"""
    print("\n📥 DOCKER INSTALLATION INSTRUCTIONS")
    print("=" * 50)
    
    print("""
🔧 TO INSTALL DOCKER DESKTOP:

1. 📥 Download Docker Desktop:
   https://www.docker.com/products/docker-desktop

2. 🏃 Run the installer as Administrator

3. 🔄 Restart your computer after installation

4. 🚀 Start Docker Desktop from Start Menu

5. ⏳ Wait for Docker to fully start (whale icon in system tray)

6. 🧪 Test with: docker --version

🎯 ALTERNATIVE: Use the Python API directly (already working!)
   python start_api.py
""")

def test_docker_deployment():
    """Test Docker deployment if available"""
    print("\n🧪 TESTING DOCKER DEPLOYMENT")
    print("=" * 50)
    
    if not check_docker_installation():
        return False
    
    if not check_docker_service():
        return False
    
    # Try to build the image
    try:
        print("🔨 Building Docker image...")
        result = subprocess.run(["docker", "build", "-t", "multimodal-sentiment:test", "."], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker image built successfully")
        else:
            print("❌ Docker build failed")
            print("Error:", result.stderr.strip())
            return False
    except Exception as e:
        print(f"❌ Docker build error: {e}")
        return False
    
    # Try Docker Compose
    if check_docker_compose():
        try:
            print("🐳 Testing Docker Compose...")
            # Try newer syntax first
            result = subprocess.run(["docker", "compose", "--profile", "cpu", "up", "-d"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                # Try older syntax
                result = subprocess.run(["docker-compose", "--profile", "cpu", "up", "-d"], 
                                      capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Docker Compose deployment successful!")
                print("🌐 API should be available at: http://localhost:8000")
                return True
            else:
                print("❌ Docker Compose failed")
                print("Error:", result.stderr.strip())
                return False
        except Exception as e:
            print(f"❌ Docker Compose error: {e}")
            return False
    
    return False

def main():
    """Main function"""
    print("🐳 DOCKER SETUP AND TROUBLESHOOTING")
    print("=" * 60)
    
    # Check current status
    docker_installed = check_docker_installation()
    compose_available = check_docker_compose()
    service_running = False
    
    if docker_installed:
        service_running = check_docker_service()
    
    # Provide recommendations
    print("\n🎯 RECOMMENDATIONS")
    print("=" * 50)
    
    if not docker_installed:
        print("❌ Docker not installed")
        install_docker_instructions()
        print("\n✅ IMMEDIATE SOLUTION: Use Python API directly")
        print("   python start_api.py")
    elif not service_running:
        print("❌ Docker installed but not running")
        print("🔧 Try starting Docker Desktop manually")
        if start_docker_desktop():
            print("⏳ Waiting for Docker to start...")
            time.sleep(10)
            if check_docker_service():
                print("✅ Docker is now running!")
                test_docker_deployment()
            else:
                print("❌ Docker still not running")
                print("💡 Try starting Docker Desktop manually from Start Menu")
    else:
        print("✅ Docker is installed and running")
        test_docker_deployment()

if __name__ == "__main__":
    main()
