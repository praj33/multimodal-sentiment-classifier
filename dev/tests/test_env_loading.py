#!/usr/bin/env python3
"""
Test Environment Variable Loading
Validates that environment variables are properly loaded and override configuration
"""

import os
import sys
import tempfile
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config_loader import ConfigLoader

def test_env_override():
    """Test environment variable overrides"""
    print("🧪 Testing Environment Variable Overrides")
    print("=" * 50)
    
    # Set test environment variables
    test_env_vars = {
        'API_HOST': '127.0.0.1',
        'API_PORT': '9000',
        'API_WORKERS': '2',
        'LOG_LEVEL': 'DEBUG',
        'ENVIRONMENT': 'testing',
        'DEVICE': 'cuda',
        'ENABLE_GPU': 'true',
        'CUDA_VISIBLE_DEVICES': '1',
        'MAX_FILE_SIZE_AUDIO': '25000000',
        'MAX_FILE_SIZE_VIDEO': '50000000',
        'DB_PATH': 'test_logs/test.db',
        'ALLOWED_ORIGINS': 'http://localhost:3000,http://localhost:8080'
    }
    
    # Set environment variables
    original_values = {}
    for key, value in test_env_vars.items():
        original_values[key] = os.environ.get(key)
        os.environ[key] = value
        
    try:
        # Create new config loader to pick up environment variables
        loader = ConfigLoader()
        config = loader.get_config()
        
        # Test API configuration overrides
        api_config = config.get('api', {})
        assert api_config.get('host') == '127.0.0.1', f"Expected host 127.0.0.1, got {api_config.get('host')}"
        assert api_config.get('port') == 9000, f"Expected port 9000, got {api_config.get('port')}"
        assert api_config.get('workers') == 2, f"Expected workers 2, got {api_config.get('workers')}"
        assert api_config.get('log_level') == 'DEBUG', f"Expected log_level DEBUG, got {api_config.get('log_level')}"
        assert api_config.get('environment') == 'testing', f"Expected environment testing, got {api_config.get('environment')}"
        
        print("✅ API configuration overrides working")
        
        # Test deployment configuration overrides
        deployment_config = config.get('deployment', {})
        assert deployment_config.get('device') == 'cuda', f"Expected device cuda, got {deployment_config.get('device')}"
        assert deployment_config.get('enable_gpu') == True, f"Expected enable_gpu True, got {deployment_config.get('enable_gpu')}"
        assert deployment_config.get('cuda_visible_devices') == '1', f"Expected cuda_visible_devices 1, got {deployment_config.get('cuda_visible_devices')}"
        
        print("✅ Deployment configuration overrides working")
        
        # Test file size overrides
        validation_config = config.get('validation', {}).get('file_limits', {})
        assert validation_config.get('audio_max_size') == 25000000, f"Expected audio_max_size 25000000, got {validation_config.get('audio_max_size')}"
        assert validation_config.get('video_max_size') == 50000000, f"Expected video_max_size 50000000, got {validation_config.get('video_max_size')}"
        
        print("✅ File size limit overrides working")
        
        # Test database configuration overrides
        db_config = config.get('database', {})
        assert db_config.get('path') == 'test_logs/test.db', f"Expected db path test_logs/test.db, got {db_config.get('path')}"
        
        print("✅ Database configuration overrides working")
        
        # Test security configuration overrides
        security_config = config.get('security', {})
        expected_origins = ['http://localhost:3000', 'http://localhost:8080']
        assert security_config.get('allowed_origins') == expected_origins, f"Expected origins {expected_origins}, got {security_config.get('allowed_origins')}"
        
        print("✅ Security configuration overrides working")
        
        # Test model device overrides
        models_config = config.get('models', {})
        for model_type in ['text', 'audio', 'video']:
            model_config = models_config.get(model_type, {})
            assert model_config.get('device') == 'cuda', f"Expected {model_type} device cuda, got {model_config.get('device')}"
            
        print("✅ Model device overrides working")
        
        print("\n🎉 All environment variable override tests passed!")
        
    finally:
        # Restore original environment variables
        for key, original_value in original_values.items():
            if original_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = original_value

def test_config_methods():
    """Test configuration loader methods"""
    print("\n🧪 Testing Configuration Loader Methods")
    print("=" * 50)
    
    loader = ConfigLoader()
    
    # Test get method with dot notation
    api_host = loader.get('api.host')
    assert api_host is not None, "api.host should not be None"
    print(f"✅ get('api.host') = {api_host}")
    
    # Test get method with default value
    non_existent = loader.get('non.existent.key', 'default_value')
    assert non_existent == 'default_value', f"Expected default_value, got {non_existent}"
    print("✅ get() with default value working")
    
    # Test specific config getters
    api_config = loader.get_api_config()
    assert isinstance(api_config, dict), "API config should be a dictionary"
    print("✅ get_api_config() working")
    
    model_config = loader.get_model_config()
    assert isinstance(model_config, dict), "Model config should be a dictionary"
    print("✅ get_model_config() working")
    
    text_model_config = loader.get_model_config('text')
    assert isinstance(text_model_config, dict), "Text model config should be a dictionary"
    print("✅ get_model_config('text') working")
    
    deployment_config = loader.get_deployment_config()
    assert isinstance(deployment_config, dict), "Deployment config should be a dictionary"
    print("✅ get_deployment_config() working")
    
    # Test utility methods
    device = loader.get_device()
    assert device in ['cpu', 'cuda', 'auto'], f"Device should be cpu, cuda, or auto, got {device}"
    print(f"✅ get_device() = {device}")
    
    gpu_enabled = loader.is_gpu_enabled()
    assert isinstance(gpu_enabled, bool), "GPU enabled should be boolean"
    print(f"✅ is_gpu_enabled() = {gpu_enabled}")
    
    print("\n🎉 All configuration method tests passed!")

def test_validation():
    """Test configuration validation"""
    print("\n🧪 Testing Configuration Validation")
    print("=" * 50)
    
    loader = ConfigLoader()
    
    # Test validation
    is_valid = loader.validate_config()
    print(f"✅ Configuration validation: {'PASSED' if is_valid else 'FAILED'}")
    
    if is_valid:
        print("✅ Configuration is valid")
    else:
        print("❌ Configuration validation failed")
        
    return is_valid

def test_docker_env_simulation():
    """Simulate Docker environment variables"""
    print("\n🧪 Testing Docker Environment Simulation")
    print("=" * 50)
    
    # Simulate typical Docker environment variables
    docker_env_vars = {
        'ENVIRONMENT': 'production',
        'LOG_LEVEL': 'INFO',
        'API_WORKERS': '4',
        'DEVICE': 'cpu',
        'ENABLE_GPU': 'false'
    }
    
    # Set environment variables
    original_values = {}
    for key, value in docker_env_vars.items():
        original_values[key] = os.environ.get(key)
        os.environ[key] = value
        
    try:
        loader = ConfigLoader()
        config = loader.get_config()
        
        # Verify Docker-like configuration
        api_config = config.get('api', {})
        deployment_config = config.get('deployment', {})
        
        assert api_config.get('environment') == 'production'
        assert api_config.get('log_level') == 'INFO'
        assert api_config.get('workers') == 4
        assert deployment_config.get('device') == 'cpu'
        assert deployment_config.get('enable_gpu') == False
        
        print("✅ Docker environment simulation successful")
        
        # Print summary
        loader.print_config_summary()
        
    finally:
        # Restore original environment variables
        for key, original_value in original_values.items():
            if original_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = original_value

def main():
    """Run all tests"""
    print("🚀 Starting Environment Variable Loading Tests")
    print("=" * 60)
    
    try:
        test_config_methods()
        test_env_override()
        test_docker_env_simulation()
        
        # Final validation
        is_valid = test_validation()
        
        if is_valid:
            print("\n🎉 ALL TESTS PASSED! Environment variable loading is working correctly.")
            return True
        else:
            print("\n❌ VALIDATION FAILED! Please check configuration files.")
            return False
            
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
