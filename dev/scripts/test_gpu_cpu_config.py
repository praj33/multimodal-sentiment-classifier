#!/usr/bin/env python3
"""
GPU vs CPU Configuration Test
Validates device detection and model loading for both CPU and GPU modes
"""

import os
import sys
import torch
import time
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config_loader import ConfigLoader

class GPUCPUConfigTester:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.test_results = {}
        
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
        
    def check_pytorch_installation(self):
        """Check PyTorch installation and CUDA availability"""
        print("\n🔍 Checking PyTorch Installation")
        print("=" * 40)
        
        try:
            import torch
            self.log_success(f"PyTorch version: {torch.__version__}")
            
            # Check CUDA availability
            if torch.cuda.is_available():
                cuda_version = torch.version.cuda
                gpu_count = torch.cuda.device_count()
                gpu_name = torch.cuda.get_device_name(0) if gpu_count > 0 else "Unknown"
                
                self.log_success(f"CUDA available: {cuda_version}")
                self.log_success(f"GPU count: {gpu_count}")
                self.log_success(f"GPU name: {gpu_name}")
                
                self.test_results['cuda_available'] = True
                self.test_results['gpu_count'] = gpu_count
                self.test_results['gpu_name'] = gpu_name
            else:
                self.log_info("CUDA not available - CPU mode only")
                self.test_results['cuda_available'] = False
                
            return True
        except ImportError as e:
            self.log_error(f"PyTorch not installed: {e}")
            return False
            
    def test_cpu_configuration(self):
        """Test CPU configuration"""
        print("\n💻 Testing CPU Configuration")
        print("=" * 40)
        
        # Set CPU environment variables
        original_device = os.environ.get('DEVICE')
        original_gpu = os.environ.get('ENABLE_GPU')
        
        os.environ['DEVICE'] = 'cpu'
        os.environ['ENABLE_GPU'] = 'false'
        
        try:
            # Load configuration
            loader = ConfigLoader()
            config = loader.get_config()
            
            # Verify CPU settings
            device = loader.get_device()
            gpu_enabled = loader.is_gpu_enabled()
            
            if device == 'cpu':
                self.log_success("Device correctly set to CPU")
            else:
                self.log_error(f"Expected device 'cpu', got '{device}'")
                
            if not gpu_enabled:
                self.log_success("GPU correctly disabled")
            else:
                self.log_error("GPU should be disabled in CPU mode")
                
            # Test model device configuration
            models_config = config.get('models', {})
            for model_type in ['text', 'audio', 'video']:
                model_device = models_config.get(model_type, {}).get('device', 'unknown')
                if model_device == 'cpu':
                    self.log_success(f"{model_type} model device set to CPU")
                else:
                    self.log_warning(f"{model_type} model device is '{model_device}', expected 'cpu'")
                    
            # Test actual model loading (simplified)
            try:
                from classifiers.text_classifier import TextClassifier
                text_classifier = TextClassifier()
                self.log_success("Text classifier loaded successfully in CPU mode")
                
                # Test a simple prediction
                start_time = time.time()
                sentiment, confidence = text_classifier.predict("This is a test message")
                processing_time = time.time() - start_time
                
                self.log_success(f"CPU prediction successful: {sentiment} ({confidence:.3f}) in {processing_time:.3f}s")
                self.test_results['cpu_prediction_time'] = processing_time
                
            except Exception as e:
                self.log_error(f"Failed to load text classifier in CPU mode: {e}")
                
            self.test_results['cpu_config_valid'] = True
            return True
            
        except Exception as e:
            self.log_error(f"CPU configuration test failed: {e}")
            self.test_results['cpu_config_valid'] = False
            return False
        finally:
            # Restore original environment variables
            if original_device:
                os.environ['DEVICE'] = original_device
            else:
                os.environ.pop('DEVICE', None)
                
            if original_gpu:
                os.environ['ENABLE_GPU'] = original_gpu
            else:
                os.environ.pop('ENABLE_GPU', None)
                
    def test_gpu_configuration(self):
        """Test GPU configuration"""
        print("\n🚀 Testing GPU Configuration")
        print("=" * 40)
        
        if not self.test_results.get('cuda_available', False):
            self.log_info("Skipping GPU test - CUDA not available")
            self.test_results['gpu_config_valid'] = False
            return False
            
        # Set GPU environment variables
        original_device = os.environ.get('DEVICE')
        original_gpu = os.environ.get('ENABLE_GPU')
        original_cuda_devices = os.environ.get('CUDA_VISIBLE_DEVICES')
        
        os.environ['DEVICE'] = 'cuda'
        os.environ['ENABLE_GPU'] = 'true'
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'
        
        try:
            # Load configuration
            loader = ConfigLoader()
            config = loader.get_config()
            
            # Verify GPU settings
            device = loader.get_device()
            gpu_enabled = loader.is_gpu_enabled()
            
            if device == 'cuda':
                self.log_success("Device correctly set to CUDA")
            else:
                self.log_error(f"Expected device 'cuda', got '{device}'")
                
            if gpu_enabled:
                self.log_success("GPU correctly enabled")
            else:
                self.log_error("GPU should be enabled in GPU mode")
                
            # Test model device configuration
            models_config = config.get('models', {})
            for model_type in ['text', 'audio', 'video']:
                model_device = models_config.get(model_type, {}).get('device', 'unknown')
                if model_device == 'cuda':
                    self.log_success(f"{model_type} model device set to CUDA")
                else:
                    self.log_warning(f"{model_type} model device is '{model_device}', expected 'cuda'")
                    
            # Test GPU memory and availability
            if torch.cuda.is_available():
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
                self.log_success(f"GPU memory available: {gpu_memory:.1f} GB")
                
                # Test simple tensor operation on GPU
                try:
                    test_tensor = torch.randn(100, 100).cuda()
                    result = torch.matmul(test_tensor, test_tensor.t())
                    self.log_success("GPU tensor operations working")
                    
                    # Clean up GPU memory
                    del test_tensor, result
                    torch.cuda.empty_cache()
                    
                except Exception as e:
                    self.log_error(f"GPU tensor operations failed: {e}")
                    
            self.test_results['gpu_config_valid'] = True
            return True
            
        except Exception as e:
            self.log_error(f"GPU configuration test failed: {e}")
            self.test_results['gpu_config_valid'] = False
            return False
        finally:
            # Restore original environment variables
            if original_device:
                os.environ['DEVICE'] = original_device
            else:
                os.environ.pop('DEVICE', None)
                
            if original_gpu:
                os.environ['ENABLE_GPU'] = original_gpu
            else:
                os.environ.pop('ENABLE_GPU', None)
                
            if original_cuda_devices:
                os.environ['CUDA_VISIBLE_DEVICES'] = original_cuda_devices
            else:
                os.environ.pop('CUDA_VISIBLE_DEVICES', None)
                
    def test_auto_device_detection(self):
        """Test automatic device detection"""
        print("\n🔄 Testing Auto Device Detection")
        print("=" * 40)
        
        # Set auto device mode
        original_device = os.environ.get('DEVICE')
        os.environ['DEVICE'] = 'auto'
        
        try:
            loader = ConfigLoader()
            device = loader.get_device()
            
            if device == 'auto':
                self.log_success("Auto device detection configured")
                
                # Test what device would be selected
                if torch.cuda.is_available():
                    expected_device = 'cuda'
                    self.log_info("Auto detection should select CUDA")
                else:
                    expected_device = 'cpu'
                    self.log_info("Auto detection should select CPU")
                    
                self.test_results['auto_detection_expected'] = expected_device
            else:
                self.log_warning(f"Auto device not working, got '{device}'")
                
            return True
            
        except Exception as e:
            self.log_error(f"Auto device detection test failed: {e}")
            return False
        finally:
            # Restore original environment variable
            if original_device:
                os.environ['DEVICE'] = original_device
            else:
                os.environ.pop('DEVICE', None)
                
    def test_docker_environment_simulation(self):
        """Test Docker environment variable simulation"""
        print("\n🐳 Testing Docker Environment Simulation")
        print("=" * 40)
        
        # Test CPU Docker environment
        cpu_env = {
            'DEVICE': 'cpu',
            'ENABLE_GPU': 'false',
            'ENVIRONMENT': 'production',
            'API_WORKERS': '4'
        }
        
        # Test GPU Docker environment
        gpu_env = {
            'DEVICE': 'cuda',
            'ENABLE_GPU': 'true',
            'CUDA_VISIBLE_DEVICES': '0',
            'ENVIRONMENT': 'production',
            'API_WORKERS': '2'
        }
        
        for env_name, env_vars in [("CPU Docker", cpu_env), ("GPU Docker", gpu_env)]:
            self.log_info(f"Testing {env_name} environment...")
            
            # Set environment variables
            original_values = {}
            for key, value in env_vars.items():
                original_values[key] = os.environ.get(key)
                os.environ[key] = value
                
            try:
                loader = ConfigLoader()
                config = loader.get_config()
                
                # Verify configuration
                device = loader.get_device()
                gpu_enabled = loader.is_gpu_enabled()
                api_workers = config.get('api', {}).get('workers', 0)
                
                expected_device = env_vars['DEVICE']
                expected_gpu = env_vars['ENABLE_GPU'] == 'true'
                expected_workers = int(env_vars['API_WORKERS'])
                
                if device == expected_device:
                    self.log_success(f"{env_name}: Device correctly set to {device}")
                else:
                    self.log_error(f"{env_name}: Expected device {expected_device}, got {device}")
                    
                if gpu_enabled == expected_gpu:
                    self.log_success(f"{env_name}: GPU setting correct ({gpu_enabled})")
                else:
                    self.log_error(f"{env_name}: Expected GPU {expected_gpu}, got {gpu_enabled}")
                    
                if api_workers == expected_workers:
                    self.log_success(f"{env_name}: Workers correctly set to {api_workers}")
                else:
                    self.log_warning(f"{env_name}: Expected {expected_workers} workers, got {api_workers}")
                    
            finally:
                # Restore original environment variables
                for key, original_value in original_values.items():
                    if original_value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = original_value
                        
    def generate_configuration_report(self):
        """Generate configuration test report"""
        print("\n📊 GPU/CPU Configuration Test Report")
        print("=" * 50)
        
        # System capabilities
        print("\n🖥️  System Capabilities:")
        print(f"   CUDA Available: {self.test_results.get('cuda_available', False)}")
        if self.test_results.get('cuda_available'):
            print(f"   GPU Count: {self.test_results.get('gpu_count', 0)}")
            print(f"   GPU Name: {self.test_results.get('gpu_name', 'Unknown')}")
        
        # Configuration tests
        print("\n⚙️  Configuration Tests:")
        print(f"   CPU Configuration: {'✅ PASS' if self.test_results.get('cpu_config_valid') else '❌ FAIL'}")
        print(f"   GPU Configuration: {'✅ PASS' if self.test_results.get('gpu_config_valid') else '❌ FAIL' if self.test_results.get('cuda_available') else '⏭️  SKIP (No CUDA)'}")
        
        # Performance
        if 'cpu_prediction_time' in self.test_results:
            print(f"\n⚡ Performance:")
            print(f"   CPU Prediction Time: {self.test_results['cpu_prediction_time']:.3f}s")
            
        # Recommendations
        print("\n💡 Recommendations:")
        if self.test_results.get('cuda_available'):
            print("   ✅ GPU available - use GPU deployment for better performance")
            print("   📋 Docker command: docker-compose --profile gpu up")
        else:
            print("   💻 GPU not available - use CPU deployment")
            print("   📋 Docker command: docker-compose --profile cpu up")
            
        if not self.errors:
            print("\n🎉 All configuration tests passed!")
        else:
            print(f"\n❌ Found {len(self.errors)} error(s) - please review configuration")
            
    def run_configuration_test(self):
        """Run complete GPU/CPU configuration test"""
        print("🚀 Starting GPU/CPU Configuration Test")
        print("=" * 60)
        
        # Check PyTorch installation
        if not self.check_pytorch_installation():
            return False
            
        # Test CPU configuration
        self.test_cpu_configuration()
        
        # Test GPU configuration (if available)
        self.test_gpu_configuration()
        
        # Test auto device detection
        self.test_auto_device_detection()
        
        # Test Docker environment simulation
        self.test_docker_environment_simulation()
        
        # Generate report
        self.generate_configuration_report()
        
        return len(self.errors) == 0

if __name__ == "__main__":
    tester = GPUCPUConfigTester()
    success = tester.run_configuration_test()
    sys.exit(0 if success else 1)
