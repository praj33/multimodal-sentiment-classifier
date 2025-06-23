# validate_deployment.py - Validate deployment readiness

import os
import yaml
from pathlib import Path

def validate_files():
    """Validate that all required files exist"""
    print("📁 VALIDATING DEPLOYMENT FILES")
    print("=" * 40)
    
    required_files = [
        "Dockerfile",
        "docker-compose.yml", 
        ".env",
        "config/config.yaml",
        "requirements.txt",
        "api.py",
        "input_validation.py",
        "streaming_api.py"
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    else:
        print("\n✅ All required files present")
        return True

def validate_config():
    """Validate configuration files"""
    print("\n⚙️ VALIDATING CONFIGURATION")
    print("=" * 40)
    
    # Validate .env file
    try:
        with open('.env', 'r') as f:
            env_content = f.read()
            required_vars = ['API_HOST', 'API_PORT', 'DEVICE', 'MAX_FILE_SIZE_AUDIO']
            
            for var in required_vars:
                if var in env_content:
                    print(f"✅ {var} found in .env")
                else:
                    print(f"❌ {var} missing in .env")
                    return False
    except Exception as e:
        print(f"❌ Error reading .env: {e}")
        return False
    
    # Validate config.yaml
    try:
        with open('config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
            
            required_sections = ['api', 'models', 'fusion', 'validation']
            
            for section in required_sections:
                if section in config:
                    print(f"✅ {section} section found in config.yaml")
                else:
                    print(f"❌ {section} section missing in config.yaml")
                    return False
    except Exception as e:
        print(f"❌ Error reading config.yaml: {e}")
        return False
    
    print("\n✅ Configuration validation passed")
    return True

def validate_directory_structure():
    """Validate directory structure"""
    print("\n📂 VALIDATING DIRECTORY STRUCTURE")
    print("=" * 40)
    
    required_dirs = [
        "classifiers",
        "fusion", 
        "config",
        "logs",
        "dev",
        "sdk/python"
    ]
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/ - MISSING")
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created {directory}/")
    
    print("\n✅ Directory structure validation passed")
    return True

def validate_docker_files():
    """Validate Docker configuration"""
    print("\n🐳 VALIDATING DOCKER CONFIGURATION")
    print("=" * 40)
    
    # Check Dockerfile
    try:
        with open('Dockerfile', 'r') as f:
            dockerfile_content = f.read()
            
            required_elements = ['FROM python:', 'WORKDIR /app', 'COPY requirements.txt', 'EXPOSE 8000']
            
            for element in required_elements:
                if element in dockerfile_content:
                    print(f"✅ {element} found in Dockerfile")
                else:
                    print(f"❌ {element} missing in Dockerfile")
                    return False
    except Exception as e:
        print(f"❌ Error reading Dockerfile: {e}")
        return False
    
    # Check docker-compose.yml
    try:
        with open('docker-compose.yml', 'r') as f:
            compose_content = yaml.safe_load(f)
            
            if 'services' in compose_content:
                print("✅ services section found in docker-compose.yml")
                
                # Check for CPU service
                services = compose_content['services']
                if any('multimodal-sentiment' in service for service in services):
                    print("✅ multimodal-sentiment service found")
                else:
                    print("❌ multimodal-sentiment service missing")
                    return False
            else:
                print("❌ services section missing in docker-compose.yml")
                return False
    except Exception as e:
        print(f"❌ Error reading docker-compose.yml: {e}")
        return False
    
    print("\n✅ Docker configuration validation passed")
    return True

def validate_api_imports():
    """Validate that API can import all required modules"""
    print("\n🔍 VALIDATING API IMPORTS")
    print("=" * 40)
    
    try:
        # Test basic imports
        import sys
        sys.path.append('.')
        
        # Test API imports
        from api import app
        print("✅ Main API imports successfully")
        
        # Test classifier imports
        from classifiers.text_classifier import TextClassifier
        print("✅ Text classifier imports successfully")
        
        from classifiers.audio_classifier import AudioClassifier
        print("✅ Audio classifier imports successfully")
        
        from classifiers.video_classifier import VideoClassifier
        print("✅ Video classifier imports successfully")
        
        # Test fusion import
        from fusion.fusion_engine import FusionEngine
        print("✅ Fusion engine imports successfully")
        
        # Test validation import
        from input_validation import input_validator
        print("✅ Input validation imports successfully")
        
        # Test streaming import
        from streaming_api import streaming_processor
        print("✅ Streaming API imports successfully")
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False
    
    print("\n✅ API import validation passed")
    return True

def main():
    """Main validation function"""
    print("🎯 DEPLOYMENT READINESS VALIDATION")
    print("=" * 60)
    
    validations = [
        validate_files,
        validate_config,
        validate_directory_structure,
        validate_docker_files,
        validate_api_imports
    ]
    
    all_passed = True
    
    for validation in validations:
        if not validation():
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("✅ Deployment is ready for production")
        print("\n🚀 Ready for Day 1 deliverable:")
        print("   docker-compose up --profile cpu")
    else:
        print("❌ SOME VALIDATIONS FAILED!")
        print("Please fix the issues above before deployment")
    
    return all_passed

if __name__ == "__main__":
    main()
