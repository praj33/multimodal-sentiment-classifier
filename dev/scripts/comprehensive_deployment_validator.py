#!/usr/bin/env python3
"""
Comprehensive Deployment Validator
Validates complete deployment with all endpoints, configuration, and functionality
"""

import os
import sys
import time
import requests
import json
import tempfile
from pathlib import Path
from typing import Dict, Any, List

class ComprehensiveDeploymentValidator:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.errors = []
        self.warnings = []
        self.test_results = {}
        self.session = requests.Session()
        
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
        
    def test_service_availability(self):
        """Test if the service is running and accessible"""
        print("\n🌐 Testing Service Availability")
        print("=" * 40)
        
        try:
            response = self.session.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                self.log_success("Service is accessible")
                self.test_results['service_available'] = True
                return True
            else:
                self.log_error(f"Service returned status {response.status_code}")
                self.test_results['service_available'] = False
                return False
        except requests.RequestException as e:
            self.log_error(f"Cannot connect to service: {e}")
            self.test_results['service_available'] = False
            return False
            
    def test_health_endpoint(self):
        """Test health check endpoint"""
        print("\n🏥 Testing Health Endpoint")
        print("=" * 40)
        
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                health_data = response.json()
                if health_data.get('status') == 'healthy':
                    self.log_success("Health check passed")
                    self.test_results['health_check'] = True
                    return True
                else:
                    self.log_error(f"Health check failed: {health_data}")
                    self.test_results['health_check'] = False
                    return False
            else:
                self.log_error(f"Health endpoint returned status {response.status_code}")
                self.test_results['health_check'] = False
                return False
        except Exception as e:
            self.log_error(f"Health check failed: {e}")
            self.test_results['health_check'] = False
            return False
            
    def test_text_prediction(self):
        """Test text prediction endpoint"""
        print("\n📝 Testing Text Prediction")
        print("=" * 40)
        
        test_texts = [
            "I absolutely love this amazing product!",
            "This is terrible and disappointing.",
            "It's okay, nothing special.",
            "Fantastic experience, highly recommended!",
            "Worst purchase ever, complete waste of money."
        ]
        
        successful_predictions = 0
        total_time = 0
        
        for i, text in enumerate(test_texts, 1):
            try:
                start_time = time.time()
                response = self.session.post(
                    f"{self.base_url}/predict/text",
                    json={"text": text},
                    timeout=30
                )
                processing_time = time.time() - start_time
                total_time += processing_time
                
                if response.status_code == 200:
                    result = response.json()
                    sentiment = result.get('sentiment')
                    confidence = result.get('confidence', 0)
                    
                    if sentiment and confidence > 0:
                        self.log_success(f"Text {i}: {sentiment} ({confidence:.3f}) in {processing_time:.3f}s")
                        successful_predictions += 1
                    else:
                        self.log_warning(f"Text {i}: Invalid response format")
                else:
                    self.log_error(f"Text {i}: HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_error(f"Text {i} prediction failed: {e}")
                
        avg_time = total_time / len(test_texts) if test_texts else 0
        success_rate = successful_predictions / len(test_texts) if test_texts else 0
        
        self.test_results['text_predictions'] = {
            'successful': successful_predictions,
            'total': len(test_texts),
            'success_rate': success_rate,
            'avg_time': avg_time
        }
        
        if success_rate >= 0.8:
            self.log_success(f"Text prediction test passed ({success_rate:.1%} success rate)")
            return True
        else:
            self.log_error(f"Text prediction test failed ({success_rate:.1%} success rate)")
            return False
            
    def test_dashboard_endpoint(self):
        """Test dashboard endpoint"""
        print("\n🎭 Testing Dashboard Endpoint")
        print("=" * 40)
        
        try:
            response = self.session.get(f"{self.base_url}/dashboard", timeout=10)
            if response.status_code == 200:
                content = response.text
                if "Multimodal Sentiment" in content and "dashboard" in content.lower():
                    self.log_success("Dashboard loads successfully")
                    self.test_results['dashboard_available'] = True
                    return True
                else:
                    self.log_warning("Dashboard content may be incomplete")
                    self.test_results['dashboard_available'] = False
                    return False
            else:
                self.log_error(f"Dashboard returned status {response.status_code}")
                self.test_results['dashboard_available'] = False
                return False
        except Exception as e:
            self.log_error(f"Dashboard test failed: {e}")
            self.test_results['dashboard_available'] = False
            return False
            
    def test_analytics_endpoint(self):
        """Test analytics endpoint"""
        print("\n📊 Testing Analytics Endpoint")
        print("=" * 40)
        
        try:
            response = self.session.get(f"{self.base_url}/analytics", timeout=10)
            if response.status_code == 200:
                analytics_data = response.json()
                if isinstance(analytics_data, dict):
                    self.log_success("Analytics endpoint working")
                    self.test_results['analytics_available'] = True
                    return True
                else:
                    self.log_warning("Analytics returned unexpected format")
                    self.test_results['analytics_available'] = False
                    return False
            else:
                self.log_warning(f"Analytics returned status {response.status_code}")
                self.test_results['analytics_available'] = False
                return False
        except Exception as e:
            self.log_warning(f"Analytics test failed: {e}")
            self.test_results['analytics_available'] = False
            return False
            
    def test_streaming_endpoint(self):
        """Test streaming endpoint"""
        print("\n📡 Testing Streaming Endpoint")
        print("=" * 40)
        
        try:
            response = self.session.get(f"{self.base_url}/streaming/test", timeout=10)
            if response.status_code == 200:
                content = response.text
                if "streaming" in content.lower():
                    self.log_success("Streaming test page available")
                    self.test_results['streaming_available'] = True
                    return True
                else:
                    self.log_warning("Streaming page content incomplete")
                    self.test_results['streaming_available'] = False
                    return False
            else:
                self.log_warning(f"Streaming test page returned status {response.status_code}")
                self.test_results['streaming_available'] = False
                return False
        except Exception as e:
            self.log_warning(f"Streaming test failed: {e}")
            self.test_results['streaming_available'] = False
            return False
            
    def test_file_upload_validation(self):
        """Test file upload validation"""
        print("\n📁 Testing File Upload Validation")
        print("=" * 40)
        
        # Test with invalid file
        try:
            # Create a temporary text file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write("This is not an audio or video file")
                temp_file_path = f.name
                
            try:
                with open(temp_file_path, 'rb') as f:
                    files = {'file': ('test.txt', f, 'text/plain')}
                    response = self.session.post(
                        f"{self.base_url}/predict/audio",
                        files=files,
                        timeout=30
                    )
                    
                if response.status_code == 400:
                    self.log_success("File validation working (rejected invalid file)")
                    self.test_results['file_validation'] = True
                    return True
                else:
                    self.log_warning(f"File validation may not be working (status: {response.status_code})")
                    self.test_results['file_validation'] = False
                    return False
                    
            finally:
                os.unlink(temp_file_path)
                
        except Exception as e:
            self.log_warning(f"File validation test failed: {e}")
            self.test_results['file_validation'] = False
            return False
            
    def test_error_handling(self):
        """Test error handling"""
        print("\n🚨 Testing Error Handling")
        print("=" * 40)
        
        error_tests = [
            # Test invalid JSON
            {
                'url': f"{self.base_url}/predict/text",
                'method': 'POST',
                'data': '{"invalid": json}',
                'headers': {'Content-Type': 'application/json'},
                'expected_status': 400,
                'test_name': 'Invalid JSON'
            },
            # Test missing required field
            {
                'url': f"{self.base_url}/predict/text",
                'method': 'POST',
                'json': {},
                'expected_status': 422,
                'test_name': 'Missing required field'
            },
            # Test non-existent endpoint
            {
                'url': f"{self.base_url}/nonexistent",
                'method': 'GET',
                'expected_status': 404,
                'test_name': 'Non-existent endpoint'
            }
        ]
        
        successful_error_tests = 0
        
        for test in error_tests:
            try:
                if test['method'] == 'POST':
                    if 'json' in test:
                        response = self.session.post(test['url'], json=test['json'], timeout=10)
                    else:
                        response = self.session.post(
                            test['url'], 
                            data=test.get('data'),
                            headers=test.get('headers', {}),
                            timeout=10
                        )
                else:
                    response = self.session.get(test['url'], timeout=10)
                    
                if response.status_code == test['expected_status']:
                    self.log_success(f"{test['test_name']}: Correct error handling")
                    successful_error_tests += 1
                else:
                    self.log_warning(f"{test['test_name']}: Expected {test['expected_status']}, got {response.status_code}")
                    
            except Exception as e:
                self.log_warning(f"{test['test_name']}: Test failed - {e}")
                
        self.test_results['error_handling'] = {
            'successful': successful_error_tests,
            'total': len(error_tests)
        }
        
        return successful_error_tests >= len(error_tests) * 0.7  # 70% success rate
        
    def test_performance_benchmarks(self):
        """Test performance benchmarks"""
        print("\n⚡ Testing Performance")
        print("=" * 40)
        
        # Test response times
        response_times = []
        
        for i in range(5):
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}/health", timeout=10)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    response_times.append(response_time)
                    
            except Exception:
                pass
                
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            
            self.test_results['performance'] = {
                'avg_response_time': avg_response_time,
                'max_response_time': max_response_time
            }
            
            if avg_response_time < 1.0:
                self.log_success(f"Good response time: {avg_response_time:.3f}s average")
                return True
            else:
                self.log_warning(f"Slow response time: {avg_response_time:.3f}s average")
                return False
        else:
            self.log_error("Could not measure performance")
            return False
            
    def generate_deployment_report(self):
        """Generate comprehensive deployment report"""
        print("\n📋 Comprehensive Deployment Report")
        print("=" * 60)
        
        # Service status
        print("\n🌐 Service Status:")
        print(f"   Service Available: {'✅ YES' if self.test_results.get('service_available') else '❌ NO'}")
        print(f"   Health Check: {'✅ PASS' if self.test_results.get('health_check') else '❌ FAIL'}")
        
        # Endpoint tests
        print("\n🔗 Endpoint Tests:")
        print(f"   Dashboard: {'✅ WORKING' if self.test_results.get('dashboard_available') else '❌ FAILED'}")
        print(f"   Analytics: {'✅ WORKING' if self.test_results.get('analytics_available') else '⚠️  LIMITED'}")
        print(f"   Streaming: {'✅ WORKING' if self.test_results.get('streaming_available') else '⚠️  LIMITED'}")
        
        # Text prediction results
        text_results = self.test_results.get('text_predictions', {})
        if text_results:
            success_rate = text_results.get('success_rate', 0)
            avg_time = text_results.get('avg_time', 0)
            print(f"\n📝 Text Prediction:")
            print(f"   Success Rate: {success_rate:.1%}")
            print(f"   Average Time: {avg_time:.3f}s")
            
        # Security and validation
        print(f"\n🔒 Security & Validation:")
        print(f"   File Validation: {'✅ WORKING' if self.test_results.get('file_validation') else '⚠️  CHECK'}")
        
        error_handling = self.test_results.get('error_handling', {})
        if error_handling:
            error_rate = error_handling.get('successful', 0) / error_handling.get('total', 1)
            print(f"   Error Handling: {error_rate:.1%} tests passed")
            
        # Performance
        performance = self.test_results.get('performance', {})
        if performance:
            print(f"\n⚡ Performance:")
            print(f"   Average Response: {performance.get('avg_response_time', 0):.3f}s")
            print(f"   Max Response: {performance.get('max_response_time', 0):.3f}s")
            
        # Overall status
        print(f"\n🎯 Overall Status:")
        if not self.errors:
            print("   🎉 DEPLOYMENT SUCCESSFUL - All critical tests passed!")
            print("\n📋 Next Steps:")
            print("   1. Access dashboard: http://localhost:8000/dashboard")
            print("   2. View API docs: http://localhost:8000/docs")
            print("   3. Test endpoints: http://localhost:8000/streaming/test")
        else:
            print(f"   ❌ DEPLOYMENT ISSUES - {len(self.errors)} error(s) found")
            print("\n🔧 Issues to resolve:")
            for error in self.errors[:5]:  # Show first 5 errors
                print(f"   - {error}")
                
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings[:3]:  # Show first 3 warnings
                print(f"   - {warning}")
                
    def run_comprehensive_validation(self):
        """Run complete deployment validation"""
        print("🚀 Starting Comprehensive Deployment Validation")
        print("=" * 70)
        
        # Core service tests
        service_ok = self.test_service_availability()
        if not service_ok:
            self.log_error("Service not available - stopping validation")
            self.generate_deployment_report()
            return False
            
        health_ok = self.test_health_endpoint()
        
        # Endpoint tests
        self.test_dashboard_endpoint()
        self.test_analytics_endpoint()
        self.test_streaming_endpoint()
        
        # Functionality tests
        self.test_text_prediction()
        self.test_file_upload_validation()
        self.test_error_handling()
        self.test_performance_benchmarks()
        
        # Generate final report
        self.generate_deployment_report()
        
        # Return success if no critical errors
        critical_tests = ['service_available', 'health_check']
        critical_passed = all(self.test_results.get(test, False) for test in critical_tests)
        
        return critical_passed and len(self.errors) == 0

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Comprehensive Deployment Validator")
    parser.add_argument("--url", default="http://localhost:8000", 
                       help="Base URL of the service (default: http://localhost:8000)")
    
    args = parser.parse_args()
    
    validator = ComprehensiveDeploymentValidator(args.url)
    success = validator.run_comprehensive_validation()
    
    sys.exit(0 if success else 1)
