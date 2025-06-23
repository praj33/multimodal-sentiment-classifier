#!/usr/bin/env python3
"""
Docker Setup Validation Script
Validates the Docker configuration and environment setup for the multimodal sentiment analysis system.
"""

import os
import sys
import yaml
import subprocess
import json
from pathlib import Path

class DockerSetupValidator:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.errors = []
        self.warnings = []
        
    def log_error(self, message):
        self.errors.append(message)
        print(f"❌ ERROR: {message}")
        
    def log_warning(self, message):
        self.warnings.append(message)
        print(f"⚠️  WARNING: {message}")
        
    def log_success(self, message):
        print(f"✅ {message}")
        
    def check_required_files(self):
        """Check if all required files are present"""
        print("\n🔍 Checking required files...")
        
        required_files = [
            "Dockerfile",
            "docker-compose.yml",
            ".env",
            "config/config.yaml",
            "config/fusion_config.yaml",
            "requirements.txt",
            "api.py"
        ]
        
        for file_path in required_files:
            full_path = self.base_dir / file_path
            if full_path.exists():
                self.log_success(f"Found {file_path}")
            else:
                self.log_error(f"Missing required file: {file_path}")
                
    def validate_dockerfile(self):
        """Validate Dockerfile configuration"""
        print("\n🐳 Validating Dockerfile...")
        
        dockerfile_path = self.base_dir / "Dockerfile"
        if not dockerfile_path.exists():
            self.log_error("Dockerfile not found")
            return
            
        with open(dockerfile_path, 'r') as f:
            dockerfile_content = f.read()
            
        # Check for required dependencies
        required_deps = [
            "ffmpeg",
            "libsndfile1",
            "libgl1-mesa-glx",
            "curl",
            "libmagic1"
        ]
        
        for dep in required_deps:
            if dep in dockerfile_content:
                self.log_success(f"Found dependency: {dep}")
            else:
                self.log_warning(f"Missing dependency: {dep}")
                
        # Check for multi-stage build
        if "FROM python:3.9-slim as builder" in dockerfile_content:
            self.log_success("Multi-stage build configured")
        else:
            self.log_warning("Multi-stage build not found")
            
        # Check for GPU support
        if "FROM production as gpu" in dockerfile_content:
            self.log_success("GPU support configured")
        else:
            self.log_warning("GPU support not configured")
            
    def validate_docker_compose(self):
        """Validate docker-compose.yml configuration"""
        print("\n🔧 Validating docker-compose.yml...")
        
        compose_path = self.base_dir / "docker-compose.yml"
        if not compose_path.exists():
            self.log_error("docker-compose.yml not found")
            return
            
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
                
            # Check health checks
            if 'healthcheck' in cpu_service:
                self.log_success("Health check configured")
            else:
                self.log_warning("Health check not configured")
                
        except yaml.YAMLError as e:
            self.log_error(f"Invalid YAML in docker-compose.yml: {e}")
            
    def validate_environment_config(self):
        """Validate environment configuration"""
        print("\n⚙️  Validating environment configuration...")
        
        # Check .env file
        env_path = self.base_dir / ".env"
        if env_path.exists():
            self.log_success("Found .env file")
            
            with open(env_path, 'r') as f:
                env_content = f.read()
                
            required_env_vars = [
                "API_HOST",
                "API_PORT",
                "DEVICE",
                "ENABLE_GPU"
            ]
            
            for var in required_env_vars:
                if var in env_content:
                    self.log_success(f"Found environment variable: {var}")
                else:
                    self.log_warning(f"Missing environment variable: {var}")
        else:
            self.log_error(".env file not found")
            
        # Check config.yaml
        config_path = self.base_dir / "config" / "config.yaml"
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                    
                self.log_success("config.yaml is valid YAML")
                
                # Check required sections
                required_sections = ['api', 'models', 'fusion', 'deployment']
                for section in required_sections:
                    if section in config:
                        self.log_success(f"Found config section: {section}")
                    else:
                        self.log_warning(f"Missing config section: {section}")
                        
            except yaml.YAMLError as e:
                self.log_error(f"Invalid YAML in config.yaml: {e}")
        else:
            self.log_error("config/config.yaml not found")
            
    def validate_python_dependencies(self):
        """Validate Python dependencies"""
        print("\n🐍 Validating Python dependencies...")
        
        requirements_path = self.base_dir / "requirements.txt"
        if not requirements_path.exists():
            self.log_error("requirements.txt not found")
            return
            
        with open(requirements_path, 'r') as f:
            requirements = f.read()
            
        critical_deps = [
            "fastapi",
            "uvicorn",
            "transformers",
            "torch",
            "librosa",
            "opencv-python",
            "mediapipe"
        ]
        
        for dep in critical_deps:
            if dep in requirements:
                self.log_success(f"Found dependency: {dep}")
            else:
                self.log_error(f"Missing critical dependency: {dep}")
                
    def check_docker_availability(self):
        """Check if Docker is available"""
        print("\n🐳 Checking Docker availability...")
        
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log_success(f"Docker is available: {result.stdout.strip()}")
                return True
            else:
                self.log_warning("Docker command failed")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_warning("Docker is not installed or not in PATH")
            return False
            
    def check_docker_compose_availability(self):
        """Check if Docker Compose is available"""
        print("\n🔧 Checking Docker Compose availability...")
        
        try:
            result = subprocess.run(['docker-compose', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log_success(f"Docker Compose is available: {result.stdout.strip()}")
                return True
            else:
                # Try docker compose (newer syntax)
                result = subprocess.run(['docker', 'compose', 'version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    self.log_success(f"Docker Compose (v2) is available: {result.stdout.strip()}")
                    return True
                else:
                    self.log_warning("Docker Compose command failed")
                    return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_warning("Docker Compose is not installed or not in PATH")
            return False
            
    def generate_report(self):
        """Generate validation report"""
        print("\n📊 Validation Report")
        print("=" * 50)
        
        if not self.errors and not self.warnings:
            print("🎉 All validations passed! Your Docker setup is ready.")
        else:
            if self.errors:
                print(f"\n❌ Found {len(self.errors)} error(s):")
                for error in self.errors:
                    print(f"   - {error}")
                    
            if self.warnings:
                print(f"\n⚠️  Found {len(self.warnings)} warning(s):")
                for warning in self.warnings:
                    print(f"   - {warning}")
                    
        print("\n📋 Next Steps:")
        if self.errors:
            print("   1. Fix the errors listed above")
            print("   2. Re-run this validation script")
        else:
            print("   1. Install Docker Desktop if not already installed")
            print("   2. Run: docker-compose --profile cpu up")
            print("   3. Test the API at http://localhost:8000/health")
            
    def run_validation(self):
        """Run all validations"""
        print("🚀 Starting Docker Setup Validation")
        print("=" * 50)
        
        self.check_required_files()
        self.validate_dockerfile()
        self.validate_docker_compose()
        self.validate_environment_config()
        self.validate_python_dependencies()
        self.check_docker_availability()
        self.check_docker_compose_availability()
        
        self.generate_report()
        
        return len(self.errors) == 0

if __name__ == "__main__":
    validator = DockerSetupValidator()
    success = validator.run_validation()
    sys.exit(0 if success else 1)
