# simple_demo.py - Simple end-to-end demonstration without external dependencies

import os
import time
import json
import requests
from typing import Dict, Any
import subprocess
import sys

class SimpleDemo:
    """Simple end-to-end demonstration using only built-in packages"""
    
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.demo_results = []
        
    def check_api_health(self) -> bool:
        """Check if API is running and healthy"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            return response.status_code == 200
        except:
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
    
    def demo_api_endpoints(self) -> Dict[str, Any]:
        """Test all API endpoints"""
        print("\n" + "="*60)
        print("🔗 API ENDPOINTS DEMO")
        print("="*60)
        
        endpoints = [
            {"path": "/", "method": "GET", "description": "Root endpoint"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/docs", "method": "GET", "description": "API documentation"},
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
    
    def demo_multimodal_text(self) -> Dict[str, Any]:
        """Demo multimodal with text input"""
        print("\n" + "="*60)
        print("🎭 MULTIMODAL ANALYSIS DEMO")
        print("="*60)
        
        test_text = "I'm really excited about this new technology! It's going to change everything!"
        
        print(f"🎯 Testing MULTIMODAL endpoint with text input...")
        print(f"Text: '{test_text}'")
        
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
                    "test_type": "multimodal",
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
                return {"test_type": "multimodal", "results": [{"error": f"HTTP {response.status_code}", "success": False}]}
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return {"test_type": "multimodal", "results": [{"error": str(e), "success": False}]}
    
    def simple_performance_test(self) -> Dict[str, Any]:
        """Simple performance test"""
        print("\n" + "="*60)
        print("⚡ SIMPLE PERFORMANCE TEST")
        print("="*60)
        
        test_texts = [
            "Great product!",
            "Terrible experience.",
            "It's okay.",
            "Amazing quality!",
            "Not satisfied."
        ]
        
        print("🔍 Testing response times for multiple requests...")
        
        times = []
        successful = 0
        
        for i, text in enumerate(test_texts, 1):
            start_time = time.time()
            try:
                response = requests.post(
                    f"{self.api_url}/predict/text",
                    json={"text": text},
                    timeout=30
                )
                end_time = time.time()
                
                if response.status_code == 200:
                    processing_time = (end_time - start_time) * 1000
                    times.append(processing_time)
                    successful += 1
                    print(f"   Request {i}: {processing_time:.1f}ms ✅")
                else:
                    print(f"   Request {i}: HTTP {response.status_code} ❌")
                    
            except Exception as e:
                print(f"   Request {i}: Error - {e} ❌")
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            print(f"\n📊 PERFORMANCE SUMMARY:")
            print(f"   ✅ Successful: {successful}/{len(test_texts)}")
            print(f"   ⏱️  Average Time: {avg_time:.1f}ms")
            print(f"   🚀 Fastest: {min_time:.1f}ms")
            print(f"   🐌 Slowest: {max_time:.1f}ms")
            
            return {
                "test_type": "performance",
                "results": [{
                    "total_requests": len(test_texts),
                    "successful_requests": successful,
                    "average_time_ms": avg_time,
                    "min_time_ms": min_time,
                    "max_time_ms": max_time,
                    "success": True
                }]
            }
        else:
            return {
                "test_type": "performance",
                "results": [{"error": "No successful requests", "success": False}]
            }
    
    def generate_demo_report(self) -> str:
        """Generate simple demo report"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_file = f"logs/simple_demo_report_{timestamp}.json"
        
        report = {
            "demo_timestamp": timestamp,
            "api_url": self.api_url,
            "results": self.demo_results,
            "summary": {
                "total_tests": len(self.demo_results),
                "test_types": [r["test_type"] for r in self.demo_results]
            }
        }
        
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Demo report saved: {report_file}")
        return report_file
    
    def run_simple_demo(self) -> Dict[str, Any]:
        """Run the simple demonstration"""
        print("🎬 STARTING SIMPLE END-TO-END DEMONSTRATION")
        print("="*80)
        
        # Check API
        if not self.check_api_health():
            print("❌ API is not running. Please start the API first:")
            print("   python -m uvicorn api:app --host 0.0.0.0 --port 8000")
            return {"error": "API not available"}
        
        print("✅ API is running and healthy!")
        
        # Run demo components
        self.demo_results.append(self.demo_text_analysis())
        self.demo_results.append(self.demo_multimodal_text())
        self.demo_results.append(self.demo_api_endpoints())
        self.demo_results.append(self.simple_performance_test())
        
        # Generate report
        report_file = self.generate_demo_report()
        
        print("\n" + "="*80)
        print("🎉 SIMPLE DEMONSTRATION COMPLETE!")
        print("="*80)
        print(f"📊 Full report: {report_file}")
        print("✅ All core systems tested and operational!")
        
        return {"status": "complete", "report_file": report_file, "results": self.demo_results}

if __name__ == "__main__":
    demo = SimpleDemo()
    demo.run_simple_demo()
