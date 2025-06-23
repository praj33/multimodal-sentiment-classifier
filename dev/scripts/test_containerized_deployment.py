#!/usr/bin/env python3
"""
Containerized Deployment Test Script
Tests Docker deployment configuration and provides setup instructions
"""

import os
import sys
import subprocess
import time
import requests
import yaml
from pathlib import Path

class ContainerizedDeploymentTester:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.errors = []
        self.warnings = []
        self.docker_available = False
        
    def log_error(self, message):
        self.errors.append(message)
        print(f"❌ ERROR: {message}")
        
    def log_warning(self, message):
        self.warnings.append(message)
        print(f"⚠️  WARNING: {message}")
        
    def log_success(self, message):
        print(f"✅ {message}")
        
    def log_info(self, message):
        print(f"ℹ️  {message}")
        
    def check_docker_availability(self):
        """Check if Docker is available and running"""
        print("\n🐳 Checking Docker Availability")
        print("=" * 40)
        
        try:
            # Check if docker command exists
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log_success(f"Docker installed: {result.stdout.strip()}")
                
                # Check if Docker daemon is running
                try:
                    result = subprocess.run(['docker', 'info'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        self.log_success("Docker daemon is running")
                        self.docker_available = True
                        return True
                    else:
                        self.log_warning("Docker daemon is not running")
                        return False
                except subprocess.TimeoutExpired:
                    self.log_warning("Docker daemon check timed out")
                    return False
            else:
                self.log_warning("Docker command failed")
                return False
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_warning("Docker is not installed or not in PATH")
            return False
            
    def check_docker_compose_availability(self):
        """Check if Docker Compose is available"""
        print("\n🔧 Checking Docker Compose Availability")
        print("=" * 40)
        
        try:
            # Try docker-compose command
            result = subprocess.run(['docker-compose', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log_success(f"Docker Compose available: {result.stdout.strip()}")
                return True
            else:
                # Try docker compose (newer syntax)
                result = subprocess.run(['docker', 'compose', 'version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    self.log_success(f"Docker Compose (v2) available: {result.stdout.strip()}")
                    return True
                else:
                    self.log_warning("Docker Compose command failed")
                    return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_warning("Docker Compose is not installed")
            return False
            
    def validate_docker_files(self):
        """Validate Docker configuration files"""
        print("\n📋 Validating Docker Configuration Files")
        print("=" * 40)
        
        # Check Dockerfile
        dockerfile_path = self.base_dir / "Dockerfile"
        if dockerfile_path.exists():
            self.log_success("Dockerfile found")
            
            with open(dockerfile_path, 'r') as f:
                dockerfile_content = f.read()
                
            # Check for multi-stage build
            if "FROM python:3.9-slim as builder" in dockerfile_content:
                self.log_success("Multi-stage build configured")
            else:
                self.log_warning("Multi-stage build not found")
                
            # Check for health check
            if "HEALTHCHECK" in dockerfile_content:
                self.log_success("Health check configured")
            else:
                self.log_warning("Health check not configured")
                
        else:
            self.log_error("Dockerfile not found")
            
        # Check docker-compose.yml
        compose_path = self.base_dir / "docker-compose.yml"
        if compose_path.exists():
            self.log_success("docker-compose.yml found")
            
            try:
                with open(compose_path, 'r') as f:
                    compose_config = yaml.safe_load(f)
                    
                # Check services
                services = compose_config.get('services', {})
                if 'multimodal-sentiment-api' in services:
                    self.log_success("CPU service configured")
                else:
                    self.log_error("CPU service not found")
                    
                if 'multimodal-sentiment-api-gpu' in services:
                    self.log_success("GPU service configured")
                else:
                    self.log_warning("GPU service not found")
                    
                # Check profiles
                cpu_service = services.get('multimodal-sentiment-api', {})
                if 'cpu' in cpu_service.get('profiles', []):
                    self.log_success("CPU profile configured")
                else:
                    self.log_warning("CPU profile not configured")
                    
            except yaml.YAMLError as e:
                self.log_error(f"Invalid YAML in docker-compose.yml: {e}")
        else:
            self.log_error("docker-compose.yml not found")
            
    def test_docker_build(self):
        """Test Docker image build process"""
        if not self.docker_available:
            self.log_warning("Skipping Docker build test - Docker not available")
            return False
            
        print("\n🏗️  Testing Docker Build Process")
        print("=" * 40)
        
        try:
            # Build CPU image
            self.log_info("Building CPU image...")
            result = subprocess.run([
                'docker', 'build', 
                '--target', 'production',
                '-t', 'multimodal-sentiment:cpu-test',
                '.'
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.log_success("CPU image built successfully")
                
                # Clean up test image
                subprocess.run(['docker', 'rmi', 'multimodal-sentiment:cpu-test'], 
                             capture_output=True)
                return True
            else:
                self.log_error(f"CPU image build failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_error("Docker build timed out")
            return False
        except Exception as e:
            self.log_error(f"Docker build error: {e}")
            return False
            
    def test_docker_compose_deployment(self):
        """Test Docker Compose deployment"""
        if not self.docker_available:
            self.log_warning("Skipping Docker Compose test - Docker not available")
            return False
            
        print("\n🚀 Testing Docker Compose Deployment")
        print("=" * 40)
        
        try:
            # Start services
            self.log_info("Starting services with docker-compose...")
            result = subprocess.run([
                'docker-compose', '--profile', 'cpu', 'up', '-d'
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                self.log_success("Services started successfully")
                
                # Wait for service to be ready
                self.log_info("Waiting for service to be ready...")
                time.sleep(30)
                
                # Test health endpoint
                try:
                    response = requests.get("http://localhost:8000/health", timeout=10)
                    if response.status_code == 200:
                        health_data = response.json()
                        if health_data.get('status') == 'healthy':
                            self.log_success("Health check passed")
                            deployment_success = True
                        else:
                            self.log_error("Health check failed")
                            deployment_success = False
                    else:
                        self.log_error(f"Health endpoint returned status {response.status_code}")
                        deployment_success = False
                except requests.RequestException as e:
                    self.log_error(f"Failed to connect to service: {e}")
                    deployment_success = False
                
                # Stop services
                self.log_info("Stopping services...")
                subprocess.run(['docker-compose', '--profile', 'cpu', 'down'], 
                             capture_output=True, text=True, timeout=60)
                
                return deployment_success
            else:
                self.log_error(f"Failed to start services: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_error("Docker Compose deployment timed out")
            return False
        except Exception as e:
            self.log_error(f"Docker Compose deployment error: {e}")
            return False
            
    def provide_docker_installation_instructions(self):
        """Provide Docker installation instructions"""
        print("\n📋 Docker Installation Instructions")
        print("=" * 50)
        
        print("\n🪟 For Windows:")
        print("1. Download Docker Desktop from: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe")
        print("2. Run the installer as Administrator")
        print("3. Restart your computer")
        print("4. Start Docker Desktop")
        print("5. Re-run this script")
        
        print("\n🐧 For Linux:")
        print("1. Update package index: sudo apt-get update")
        print("2. Install Docker: sudo apt-get install docker.io")
        print("3. Start Docker: sudo systemctl start docker")
        print("4. Enable Docker: sudo systemctl enable docker")
        print("5. Add user to docker group: sudo usermod -aG docker $USER")
        print("6. Log out and back in")
        
        print("\n🍎 For macOS:")
        print("1. Download Docker Desktop from: https://desktop.docker.com/mac/main/amd64/Docker.dmg")
        print("2. Install Docker Desktop")
        print("3. Start Docker Desktop")
        print("4. Re-run this script")
        
    def generate_deployment_report(self):
        """Generate deployment test report"""
        print("\n📊 Deployment Test Report")
        print("=" * 50)
        
        if not self.errors and not self.warnings:
            print("🎉 All deployment tests passed! Your containerized setup is ready.")
            print("\n🚀 Next Steps:")
            print("   1. Run: docker-compose --profile cpu up -d")
            print("   2. Access: http://localhost:8000/dashboard")
            print("   3. Test API: http://localhost:8000/docs")
        else:
            if self.errors:
                print(f"\n❌ Found {len(self.errors)} error(s):")
                for error in self.errors:
                    print(f"   - {error}")
                    
            if self.warnings:
                print(f"\n⚠️  Found {len(self.warnings)} warning(s):")
                for warning in self.warnings:
                    print(f"   - {warning}")
                    
        if not self.docker_available:
            print("\n📋 Docker Setup Required:")
            print("   Docker is not installed or not running.")
            print("   Please install Docker Desktop and try again.")
            
    def run_deployment_test(self):
        """Run complete deployment test"""
        print("🚀 Starting Containerized Deployment Test")
        print("=" * 60)
        
        # Check Docker availability
        docker_available = self.check_docker_availability()
        compose_available = self.check_docker_compose_availability()
        
        # Validate configuration files
        self.validate_docker_files()
        
        if docker_available and compose_available:
            # Test Docker build
            build_success = self.test_docker_build()
            
            if build_success:
                # Test deployment
                deployment_success = self.test_docker_compose_deployment()
            else:
                deployment_success = False
        else:
            # Provide installation instructions
            self.provide_docker_installation_instructions()
            
        # Generate report
        self.generate_deployment_report()
        
        return len(self.errors) == 0

if __name__ == "__main__":
    tester = ContainerizedDeploymentTester()
    success = tester.run_deployment_test()
    sys.exit(0 if success else 1)
