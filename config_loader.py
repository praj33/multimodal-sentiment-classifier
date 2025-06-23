#!/usr/bin/env python3
"""
Enhanced Configuration Loader for Multimodal Sentiment Analysis
Handles .env files, config.yaml, and environment variable overrides for Docker deployment
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("Warning: python-dotenv not available. Environment variables will be loaded from system only.")

class ConfigLoader:
    """Enhanced configuration loader with environment variable support"""
    
    def __init__(self, config_dir: str = "config", env_file: str = ".env"):
        self.config_dir = Path(config_dir)
        self.env_file = Path(env_file)
        self.config = {}
        
        # Load configuration in order of precedence
        self._load_env_file()
        self._load_yaml_config()
        self._apply_env_overrides()
        
    def _load_env_file(self):
        """Load .env file if available"""
        if self.env_file.exists():
            if DOTENV_AVAILABLE:
                load_dotenv(self.env_file)
                print(f"✅ Loaded environment variables from {self.env_file}")
            else:
                print(f"⚠️  .env file found but python-dotenv not available")
        else:
            print(f"⚠️  .env file not found at {self.env_file}")
            
    def _load_yaml_config(self):
        """Load main configuration from YAML"""
        config_file = self.config_dir / "config.yaml"
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    self.config = yaml.safe_load(f)
                print(f"✅ Loaded configuration from {config_file}")
            except yaml.YAMLError as e:
                print(f"❌ Error loading {config_file}: {e}")
                self.config = {}
        else:
            print(f"❌ Configuration file not found: {config_file}")
            self.config = {}
            
    def _apply_env_overrides(self):
        """Apply environment variable overrides to configuration"""
        # API configuration overrides
        if os.getenv('API_HOST'):
            self._set_nested_value(['api', 'host'], os.getenv('API_HOST'))
            
        if os.getenv('API_PORT'):
            try:
                self._set_nested_value(['api', 'port'], int(os.getenv('API_PORT')))
            except ValueError:
                print(f"⚠️  Invalid API_PORT value: {os.getenv('API_PORT')}")
                
        if os.getenv('API_WORKERS'):
            try:
                self._set_nested_value(['api', 'workers'], int(os.getenv('API_WORKERS')))
            except ValueError:
                print(f"⚠️  Invalid API_WORKERS value: {os.getenv('API_WORKERS')}")
                
        if os.getenv('LOG_LEVEL'):
            self._set_nested_value(['api', 'log_level'], os.getenv('LOG_LEVEL'))
            
        if os.getenv('ENVIRONMENT'):
            self._set_nested_value(['api', 'environment'], os.getenv('ENVIRONMENT'))
            
        # Device configuration overrides
        if os.getenv('DEVICE'):
            device = os.getenv('DEVICE').lower()
            self._set_nested_value(['deployment', 'device'], device)
            # Also update individual model devices
            for model_type in ['text', 'audio', 'video']:
                self._set_nested_value(['models', model_type, 'device'], device)
                
        if os.getenv('ENABLE_GPU'):
            enable_gpu = os.getenv('ENABLE_GPU').lower() in ['true', '1', 'yes']
            self._set_nested_value(['deployment', 'enable_gpu'], enable_gpu)
            
        if os.getenv('CUDA_VISIBLE_DEVICES'):
            self._set_nested_value(['deployment', 'cuda_visible_devices'], os.getenv('CUDA_VISIBLE_DEVICES'))
            
        # File size limits
        if os.getenv('MAX_FILE_SIZE_AUDIO'):
            try:
                self._set_nested_value(['validation', 'file_limits', 'audio_max_size'], 
                                     int(os.getenv('MAX_FILE_SIZE_AUDIO')))
            except ValueError:
                print(f"⚠️  Invalid MAX_FILE_SIZE_AUDIO value: {os.getenv('MAX_FILE_SIZE_AUDIO')}")
                
        if os.getenv('MAX_FILE_SIZE_VIDEO'):
            try:
                self._set_nested_value(['validation', 'file_limits', 'video_max_size'], 
                                     int(os.getenv('MAX_FILE_SIZE_VIDEO')))
            except ValueError:
                print(f"⚠️  Invalid MAX_FILE_SIZE_VIDEO value: {os.getenv('MAX_FILE_SIZE_VIDEO')}")
                
        # Database configuration
        if os.getenv('DB_PATH'):
            self._set_nested_value(['database', 'path'], os.getenv('DB_PATH'))
            
        # Security configuration
        if os.getenv('ALLOWED_ORIGINS'):
            origins = os.getenv('ALLOWED_ORIGINS').split(',')
            self._set_nested_value(['security', 'allowed_origins'], origins)
            
        print("✅ Applied environment variable overrides")
        
    def _set_nested_value(self, keys: list, value: Any):
        """Set a nested dictionary value using a list of keys"""
        current = self.config
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value
        
    def get_config(self) -> Dict[str, Any]:
        """Get the complete configuration"""
        return self.config
        
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation (e.g., 'api.host')"""
        keys = key_path.split('.')
        current = self.config
        
        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default
            
    def get_api_config(self) -> Dict[str, Any]:
        """Get API-specific configuration"""
        return self.config.get('api', {})
        
    def get_model_config(self, model_type: str = None) -> Dict[str, Any]:
        """Get model configuration"""
        models_config = self.config.get('models', {})
        if model_type:
            return models_config.get(model_type, {})
        return models_config
        
    def get_deployment_config(self) -> Dict[str, Any]:
        """Get deployment-specific configuration"""
        return self.config.get('deployment', {})
        
    def is_gpu_enabled(self) -> bool:
        """Check if GPU is enabled"""
        return self.get('deployment.enable_gpu', False)
        
    def get_device(self) -> str:
        """Get the configured device (cpu/cuda)"""
        return self.get('deployment.device', 'cpu')
        
    def validate_config(self) -> bool:
        """Validate the configuration"""
        required_sections = ['api', 'models', 'deployment']
        missing_sections = []
        
        for section in required_sections:
            if section not in self.config:
                missing_sections.append(section)
                
        if missing_sections:
            print(f"❌ Missing required configuration sections: {missing_sections}")
            return False
            
        # Validate API configuration
        api_config = self.get_api_config()
        if not api_config.get('host') or not api_config.get('port'):
            print("❌ API host and port must be configured")
            return False
            
        print("✅ Configuration validation passed")
        return True
        
    def print_config_summary(self):
        """Print a summary of the current configuration"""
        print("\n📋 Configuration Summary:")
        print("=" * 40)
        
        # API settings
        api_config = self.get_api_config()
        print(f"🌐 API: {api_config.get('host', 'N/A')}:{api_config.get('port', 'N/A')}")
        print(f"🔧 Environment: {api_config.get('environment', 'N/A')}")
        print(f"📊 Log Level: {api_config.get('log_level', 'N/A')}")
        print(f"👥 Workers: {api_config.get('workers', 'N/A')}")
        
        # Device settings
        deployment_config = self.get_deployment_config()
        print(f"💻 Device: {deployment_config.get('device', 'N/A')}")
        print(f"🚀 GPU Enabled: {deployment_config.get('enable_gpu', False)}")
        
        # Model settings
        models_config = self.get_model_config()
        enabled_models = []
        for model_type in ['text', 'audio', 'video']:
            if models_config.get(model_type, {}).get('enabled', False):
                enabled_models.append(model_type)
        print(f"🤖 Enabled Models: {', '.join(enabled_models) if enabled_models else 'None'}")
        
        print("=" * 40)

# Global configuration instance
_config_loader = None

def get_config_loader() -> ConfigLoader:
    """Get the global configuration loader instance"""
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader()
    return _config_loader

def get_config() -> Dict[str, Any]:
    """Get the complete configuration (backward compatibility)"""
    return get_config_loader().get_config()

def load_config() -> Dict[str, Any]:
    """Load configuration (backward compatibility)"""
    return get_config()

if __name__ == "__main__":
    # Test the configuration loader
    loader = ConfigLoader()
    
    if loader.validate_config():
        loader.print_config_summary()
    else:
        print("❌ Configuration validation failed")
        exit(1)
