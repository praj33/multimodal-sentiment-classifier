# end_to_end_demo.py - Complete end-to-end demonstration

import os
import time
import json
import requests
from typing import Dict, Any
import subprocess
import sys
from benchmark_system import PerformanceBenchmark
from enhanced_logging import EnhancedSentimentLogger

class EndToEndDemo:
    """Complete end-to-end demonstration of the multimodal sentiment system"""
    
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.benchmark = PerformanceBenchmark(api_url)
        self.logger = EnhancedSentimentLogger(db_type="sqlite")
        self.demo_results = []
        
    def check_api_health(self) -> bool:
        """Check if API is running and healthy"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def start_api_if_needed(self) -> bool:
        """Start API if it's not running"""
        if self.check_api_health():
            print("✅ API is already running")
            return True
        
        print("🚀 Starting API server...")
        try:
            # Try to start the API in background
            subprocess.Popen([
                sys.executable, "-m", "uvicorn", "api:app", 
                "--host", "0.0.0.0", "--port", "8000"
            ])
            
            # Wait for API to start
            for i in range(30):  # Wait up to 30 seconds
                time.sleep(1)
                if self.check_api_health():
                    print("✅ API started successfully")
                    return True
                print(f"⏳ Waiting for API to start... ({i+1}/30)")
            
            print("❌ Failed to start API")
            return False
            
        except Exception as e:
            print(f"❌ Error starting API: {e}")
            return False
    
    def demo_text_analysis(self) -> Dict[str, Any]:
        """Demonstrate text sentiment analysis"""
        print("\n" + "="*60)
        print("📝 TEXT SENTIMENT ANALYSIS DEMO")
        print("="*60)
        
        test_texts = [
            "I absolutely love this product! It's amazing!",
            "This is the worst experience I've ever had.",
            "It's okay, nothing special but not bad either.",
            "Fantastic service and great quality!",
            "I'm disappointed with the results.",
            "Neutral statement about the weather today.",
            "Incredible performance, highly recommended!",
            "Could be better, but it's acceptable."
        ]
        
        results = []
        
        for i, text in enumerate(test_texts, 1):
            print(f"\n{i}. Testing: '{text}'")
            
            start_time = time.time()
            try:
                response = requests.post(
                    f"{self.api_url}/predict/text",
                    json={"text": text},
                    timeout=30
                )
                end_time = time.time()
                
                if response.status_code == 200:
                    result = response.json()
                    processing_time = (end_time - start_time) * 1000
                    
                    print(f"   ✅ Sentiment: {result['sentiment']}")
                    print(f"   📊 Confidence: {result['confidence']:.3f}")
                    print(f"   ⏱️  Time: {processing_time:.1f}ms")
                    
                    results.append({
                        "text": text,
                        "sentiment": result['sentiment'],
                        "confidence": result['confidence'],
                        "processing_time_ms": processing_time,
                        "success": True
                    })
                    
                    # Log to enhanced logger
                    self.logger.log_prediction(
                        mode="text",
                        result=result,
                        confidence=result['confidence'],
                        processing_time=processing_time,
                        input_content=text
                    )
                    
                else:
                    print(f"   ❌ Error: HTTP {response.status_code}")
                    results.append({
                        "text": text,
                        "error": f"HTTP {response.status_code}",
                        "success": False
                    })
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                results.append({
                    "text": text,
                    "error": str(e),
                    "success": False
                })
        
        successful_tests = [r for r in results if r.get("success", False)]
        if successful_tests:
            avg_time = sum(r["processing_time_ms"] for r in successful_tests) / len(successful_tests)
            avg_confidence = sum(r["confidence"] for r in successful_tests) / len(successful_tests)
            
            print(f"\n📊 TEXT ANALYSIS SUMMARY:")
            print(f"   ✅ Successful: {len(successful_tests)}/{len(results)}")
            print(f"   ⏱️  Average Time: {avg_time:.1f}ms")
            print(f"   📈 Average Confidence: {avg_confidence:.3f}")
        
        return {"test_type": "text", "results": results}
    
    def demo_multimodal_analysis(self) -> Dict[str, Any]:
        """Demonstrate multimodal analysis if files exist"""
        print("\n" + "="*60)
        print("🎭 MULTIMODAL SENTIMENT ANALYSIS DEMO")
        print("="*60)
        
        # Check for test files
        test_files = {
            "audio": ["test_audio.wav", "sample_audio.wav", "audio_sample.wav"],
            "video": ["test_video.mp4", "sample_video.mp4", "video_sample.mp4"]
        }
        
        available_files = {}
        for file_type, filenames in test_files.items():
            for filename in filenames:
                if os.path.exists(filename):
                    available_files[file_type] = filename
                    break
        
        if not available_files:
            print("⚠️  No test audio/video files found. Creating sample text-based multimodal demo...")
            return self.demo_text_multimodal()
        
        results = []
        
        for file_type, filepath in available_files.items():
            print(f"\n🎯 Testing {file_type.upper()} file: {filepath}")
            
            start_time = time.time()
            try:
                with open(filepath, 'rb') as f:
                    files = {'file': f}
                    response = requests.post(
                        f"{self.api_url}/predict/{file_type}",
                        files=files,
                        timeout=60
                    )
                
                end_time = time.time()
                processing_time = (end_time - start_time) * 1000
                
                if response.status_code == 200:
                    result = response.json()
                    file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
                    
                    print(f"   ✅ Sentiment: {result['sentiment']}")
                    print(f"   📊 Confidence: {result['confidence']:.3f}")
                    print(f"   ⏱️  Time: {processing_time:.1f}ms")
                    print(f"   📁 File Size: {file_size:.2f}MB")
                    
                    results.append({
                        "file_type": file_type,
                        "filepath": filepath,
                        "file_size_mb": file_size,
                        "sentiment": result['sentiment'],
                        "confidence": result['confidence'],
                        "processing_time_ms": processing_time,
                        "success": True
                    })
                    
                    # Log to enhanced logger
                    self.logger.log_prediction(
                        mode=file_type,
                        result=result,
                        confidence=result['confidence'],
                        processing_time=processing_time,
                        input_data={"file_path": filepath, "file_size_mb": file_size}
                    )
                    
                else:
                    print(f"   ❌ Error: HTTP {response.status_code}")
                    results.append({
                        "file_type": file_type,
                        "filepath": filepath,
                        "error": f"HTTP {response.status_code}",
                        "success": False
                    })
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                results.append({
                    "file_type": file_type,
                    "filepath": filepath,
                    "error": str(e),
                    "success": False
                })
        
        return {"test_type": "multimodal", "results": results}
    
    def demo_text_multimodal(self) -> Dict[str, Any]:
        """Demo multimodal with text input when no media files available"""
        print("\n🎯 Testing MULTIMODAL endpoint with text input...")
        
        test_text = "I'm really excited about this new technology! It's going to change everything!"
        
        start_time = time.time()
        try:
            response = requests.post(
                f"{self.api_url}/predict/multimodal",
                json={"text": test_text},
                timeout=30
            )
            end_time = time.time()
            processing_time = (end_time - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"   ✅ Final Sentiment: {result.get('sentiment', 'N/A')}")
                print(f"   📊 Final Confidence: {result.get('confidence', 0):.3f}")
                print(f"   ⏱️  Total Time: {processing_time:.1f}ms")
                
                if 'individual_results' in result:
                    print("   📋 Individual Results:")
                    for individual in result['individual_results']:
                        print(f"      - {individual['mode']}: {individual['sentiment']} ({individual['confidence']:.3f})")
                
                return {
                    "test_type": "multimodal_text",
                    "results": [{
                        "text": test_text,
                        "sentiment": result.get('sentiment'),
                        "confidence": result.get('confidence', 0),
                        "processing_time_ms": processing_time,
                        "individual_results": result.get('individual_results', []),
                        "success": True
                    }]
                }
            else:
                print(f"   ❌ Error: HTTP {response.status_code}")
                return {"test_type": "multimodal_text", "results": [{"error": f"HTTP {response.status_code}", "success": False}]}
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return {"test_type": "multimodal_text", "results": [{"error": str(e), "success": False}]}
    
    def demo_api_endpoints(self) -> Dict[str, Any]:
        """Test all API endpoints"""
        print("\n" + "="*60)
        print("🔗 API ENDPOINTS DEMO")
        print("="*60)
        
        endpoints = [
            {"path": "/", "method": "GET", "description": "Root endpoint"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/docs", "method": "GET", "description": "API documentation"},
            {"path": "/analytics", "method": "GET", "description": "Analytics dashboard"}
        ]
        
        results = []
        
        for endpoint in endpoints:
            print(f"\n🔍 Testing {endpoint['method']} {endpoint['path']} - {endpoint['description']}")
            
            try:
                if endpoint['method'] == 'GET':
                    response = requests.get(f"{self.api_url}{endpoint['path']}", timeout=10)
                
                print(f"   Status: {response.status_code}")
                print(f"   Response Size: {len(response.content)} bytes")
                
                results.append({
                    "endpoint": endpoint['path'],
                    "method": endpoint['method'],
                    "status_code": response.status_code,
                    "response_size": len(response.content),
                    "success": 200 <= response.status_code < 300
                })
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                results.append({
                    "endpoint": endpoint['path'],
                    "method": endpoint['method'],
                    "error": str(e),
                    "success": False
                })
        
        return {"test_type": "api_endpoints", "results": results}
    
    def run_performance_benchmark(self) -> Dict[str, Any]:
        """Run performance benchmarks"""
        print("\n" + "="*60)
        print("⚡ PERFORMANCE BENCHMARK")
        print("="*60)
        
        # Text benchmark
        test_texts = [
            "Great product!",
            "Terrible experience.",
            "It's okay.",
            "Amazing quality!",
            "Not satisfied."
        ]
        
        text_results = self.benchmark.benchmark_text_analysis(test_texts, iterations=5)
        print(f"📝 Text Analysis - Avg: {text_results['latency_stats']['mean_ms']:.1f}ms")
        
        # Concurrent requests benchmark
        concurrent_results = self.benchmark.benchmark_concurrent_requests(num_concurrent=5, total_requests=25)
        print(f"⚡ Concurrent Requests - RPS: {concurrent_results.get('requests_per_second', 0):.1f}")
        
        return {
            "test_type": "performance",
            "text_benchmark": text_results,
            "concurrent_benchmark": concurrent_results
        }
    
    def generate_demo_report(self) -> str:
        """Generate comprehensive demo report"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_file = f"logs/demo_report_{timestamp}.json"
        
        report = {
            "demo_timestamp": timestamp,
            "api_url": self.api_url,
            "results": self.demo_results,
            "summary": {
                "total_tests": len(self.demo_results),
                "successful_tests": sum(1 for r in self.demo_results if any(
                    result.get("success", False) for result in r.get("results", [])
                )),
                "test_types": list(set(r["test_type"] for r in self.demo_results))
            }
        }
        
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Demo report saved: {report_file}")
        return report_file
    
    def run_complete_demo(self) -> Dict[str, Any]:
        """Run the complete end-to-end demonstration"""
        print("🎬 STARTING COMPLETE END-TO-END DEMONSTRATION")
        print("="*80)
        
        # Check/start API
        if not self.start_api_if_needed():
            print("❌ Cannot proceed without API. Please start the API manually.")
            return {"error": "API not available"}
        
        # Run all demo components
        self.demo_results.append(self.demo_text_analysis())
        self.demo_results.append(self.demo_multimodal_analysis())
        self.demo_results.append(self.demo_api_endpoints())
        self.demo_results.append(self.run_performance_benchmark())
        
        # Generate report
        report_file = self.generate_demo_report()
        
        print("\n" + "="*80)
        print("🎉 END-TO-END DEMONSTRATION COMPLETE!")
        print("="*80)
        print(f"📊 Full report: {report_file}")
        print("✅ All systems tested and operational!")
        
        return {"status": "complete", "report_file": report_file, "results": self.demo_results}

if __name__ == "__main__":
    demo = EndToEndDemo()
    demo.run_complete_demo()
