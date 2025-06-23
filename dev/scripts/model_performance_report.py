# model_performance_report.py - Comprehensive model performance benchmarking

import time
import psutil
import statistics
import json
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any
import os

class ModelPerformanceBenchmark:
    """Comprehensive model performance benchmarking and reporting"""
    
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.results = {}
        
    def benchmark_text_latency(self, iterations: int = 100) -> Dict[str, Any]:
        """Benchmark text analysis latency"""
        print(f"📝 Benchmarking Text Analysis Latency ({iterations} iterations)...")
        
        test_texts = [
            "I love this product!",
            "This is terrible.",
            "It's okay, nothing special.",
            "Amazing quality and service!",
            "Could be much better.",
            "Absolutely fantastic experience!",
            "Disappointing results overall.",
            "Neutral opinion about this."
        ]
        
        latencies = []
        errors = 0
        
        for i in range(iterations):
            text = test_texts[i % len(test_texts)]
            
            start_time = time.perf_counter()
            try:
                response = requests.post(
                    f"{self.api_url}/predict/text",
                    json={"text": text},
                    timeout=10
                )
                end_time = time.perf_counter()
                
                if response.status_code == 200:
                    latency_ms = (end_time - start_time) * 1000
                    latencies.append(latency_ms)
                else:
                    errors += 1
                    
            except Exception as e:
                errors += 1
                end_time = time.perf_counter()
        
        if latencies:
            return {
                "test_type": "text_latency",
                "iterations": iterations,
                "successful_requests": len(latencies),
                "failed_requests": errors,
                "success_rate": len(latencies) / iterations * 100,
                "latency_stats": {
                    "min_ms": min(latencies),
                    "max_ms": max(latencies),
                    "mean_ms": statistics.mean(latencies),
                    "median_ms": statistics.median(latencies),
                    "std_dev_ms": statistics.stdev(latencies) if len(latencies) > 1 else 0,
                    "p95_ms": self._percentile(latencies, 95),
                    "p99_ms": self._percentile(latencies, 99)
                }
            }
        else:
            return {"test_type": "text_latency", "error": "All requests failed"}
    
    def benchmark_concurrent_load(self, concurrent_users: int = 10, requests_per_user: int = 10) -> Dict[str, Any]:
        """Benchmark concurrent load handling"""
        print(f"⚡ Benchmarking Concurrent Load ({concurrent_users} users, {requests_per_user} req/user)...")
        
        test_text = "Concurrent load testing message for performance evaluation."
        total_requests = concurrent_users * requests_per_user
        
        def make_request():
            start_time = time.perf_counter()
            try:
                response = requests.post(
                    f"{self.api_url}/predict/text",
                    json={"text": test_text},
                    timeout=30
                )
                end_time = time.perf_counter()
                
                return {
                    "latency_ms": (end_time - start_time) * 1000,
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
            except Exception as e:
                end_time = time.perf_counter()
                return {
                    "latency_ms": (end_time - start_time) * 1000,
                    "error": str(e),
                    "success": False
                }
        
        start_time = time.perf_counter()
        
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(make_request) for _ in range(total_requests)]
            results = [future.result() for future in as_completed(futures)]
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        successful_results = [r for r in results if r["success"]]
        failed_results = [r for r in results if not r["success"]]
        
        if successful_results:
            latencies = [r["latency_ms"] for r in successful_results]
            
            return {
                "test_type": "concurrent_load",
                "concurrent_users": concurrent_users,
                "total_requests": total_requests,
                "total_time_seconds": total_time,
                "requests_per_second": total_requests / total_time,
                "successful_requests": len(successful_results),
                "failed_requests": len(failed_results),
                "success_rate": len(successful_results) / total_requests * 100,
                "latency_stats": {
                    "min_ms": min(latencies),
                    "max_ms": max(latencies),
                    "mean_ms": statistics.mean(latencies),
                    "median_ms": statistics.median(latencies),
                    "p95_ms": self._percentile(latencies, 95),
                    "p99_ms": self._percentile(latencies, 99)
                }
            }
        else:
            return {"test_type": "concurrent_load", "error": "All requests failed"}
    
    def benchmark_memory_usage(self, duration_seconds: int = 60) -> Dict[str, Any]:
        """Monitor memory usage during sustained load"""
        print(f"💾 Benchmarking Memory Usage ({duration_seconds}s duration)...")
        
        memory_samples = []
        cpu_samples = []
        
        def monitor_resources():
            start_time = time.time()
            while time.time() - start_time < duration_seconds:
                memory_samples.append(psutil.virtual_memory().percent)
                cpu_samples.append(psutil.cpu_percent(interval=1))
                time.sleep(1)
        
        def generate_load():
            """Generate sustained load during monitoring"""
            end_time = time.time() + duration_seconds
            while time.time() < end_time:
                try:
                    requests.post(
                        f"{self.api_url}/predict/text",
                        json={"text": "Memory usage test message"},
                        timeout=5
                    )
                    time.sleep(0.1)  # 10 RPS
                except:
                    pass
        
        # Start monitoring and load generation
        monitor_thread = threading.Thread(target=monitor_resources)
        load_thread = threading.Thread(target=generate_load)
        
        monitor_thread.start()
        load_thread.start()
        
        monitor_thread.join()
        load_thread.join()
        
        if memory_samples and cpu_samples:
            return {
                "test_type": "memory_usage",
                "duration_seconds": duration_seconds,
                "memory_stats": {
                    "min_percent": min(memory_samples),
                    "max_percent": max(memory_samples),
                    "mean_percent": statistics.mean(memory_samples),
                    "samples": len(memory_samples)
                },
                "cpu_stats": {
                    "min_percent": min(cpu_samples),
                    "max_percent": max(cpu_samples),
                    "mean_percent": statistics.mean(cpu_samples),
                    "samples": len(cpu_samples)
                }
            }
        else:
            return {"test_type": "memory_usage", "error": "No samples collected"}
    
    def benchmark_multimodal_performance(self) -> Dict[str, Any]:
        """Benchmark multimodal fusion performance"""
        print("🎭 Benchmarking Multimodal Fusion Performance...")
        
        # Create test files
        self._create_test_files()
        
        results = {}
        
        # Test audio analysis
        try:
            with open('test_audio.wav', 'rb') as f:
                start_time = time.perf_counter()
                response = requests.post(
                    f"{self.api_url}/predict/audio",
                    files={'file': f},
                    timeout=30
                )
                end_time = time.perf_counter()
                
                if response.status_code == 200:
                    results["audio"] = {
                        "latency_ms": (end_time - start_time) * 1000,
                        "success": True,
                        "result": response.json()
                    }
                else:
                    results["audio"] = {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            results["audio"] = {"success": False, "error": str(e)}
        
        # Test video analysis
        try:
            with open('test_video.mp4', 'rb') as f:
                start_time = time.perf_counter()
                response = requests.post(
                    f"{self.api_url}/predict/video",
                    files={'file': f},
                    timeout=30
                )
                end_time = time.perf_counter()
                
                if response.status_code == 200:
                    results["video"] = {
                        "latency_ms": (end_time - start_time) * 1000,
                        "success": True,
                        "result": response.json()
                    }
                else:
                    results["video"] = {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            results["video"] = {"success": False, "error": str(e)}
        
        # Test multimodal fusion
        try:
            with open('test_video.mp4', 'rb') as f:
                start_time = time.perf_counter()
                response = requests.post(
                    f"{self.api_url}/predict/multimodal",
                    files={'file': f},
                    timeout=30
                )
                end_time = time.perf_counter()
                
                if response.status_code == 200:
                    results["multimodal"] = {
                        "latency_ms": (end_time - start_time) * 1000,
                        "success": True,
                        "result": response.json()
                    }
                else:
                    results["multimodal"] = {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            results["multimodal"] = {"success": False, "error": str(e)}
        
        # Cleanup test files
        self._cleanup_test_files()
        
        return {"test_type": "multimodal_performance", "results": results}
    
    def _create_test_files(self):
        """Create test audio and video files"""
        # Create mock audio file
        with open('test_audio.wav', 'wb') as f:
            f.write(b'RIFF' + (1000).to_bytes(4, 'little') + b'WAVE' + b'\x00' * 100)
        
        # Create mock video file
        with open('test_video.mp4', 'wb') as f:
            f.write(b'\x00\x00\x00\x20ftypmp42' + b'\x00' * 500)
    
    def _cleanup_test_files(self):
        """Clean up test files"""
        for file in ['test_audio.wav', 'test_video.mp4']:
            try:
                os.remove(file)
            except:
                pass
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile"""
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]
    
    def run_comprehensive_benchmark(self) -> Dict[str, Any]:
        """Run all benchmarks and generate comprehensive report"""
        print("🚀 RUNNING COMPREHENSIVE MODEL PERFORMANCE BENCHMARK")
        print("=" * 70)
        
        # Check API health
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code != 200:
                return {"error": "API not healthy"}
        except:
            return {"error": "API not accessible"}
        
        benchmark_results = {}
        
        # Run all benchmarks
        benchmark_results["text_latency"] = self.benchmark_text_latency(100)
        benchmark_results["concurrent_load"] = self.benchmark_concurrent_load(10, 10)
        benchmark_results["memory_usage"] = self.benchmark_memory_usage(30)
        benchmark_results["multimodal_performance"] = self.benchmark_multimodal_performance()
        
        # Generate summary
        summary = self._generate_summary(benchmark_results)
        benchmark_results["summary"] = summary
        
        # Save results
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"logs/model_performance_report_{timestamp}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(benchmark_results, f, indent=2)
        
        print(f"\n📊 Performance report saved: {filename}")
        return benchmark_results
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate performance summary"""
        summary = {
            "overall_status": "healthy",
            "key_metrics": {},
            "recommendations": []
        }
        
        # Text latency summary
        if "text_latency" in results and "latency_stats" in results["text_latency"]:
            text_stats = results["text_latency"]["latency_stats"]
            summary["key_metrics"]["text_mean_latency_ms"] = text_stats["mean_ms"]
            summary["key_metrics"]["text_p95_latency_ms"] = text_stats["p95_ms"]
            
            if text_stats["mean_ms"] > 500:
                summary["recommendations"].append("Text analysis latency is high (>500ms)")
        
        # Concurrent load summary
        if "concurrent_load" in results and "requests_per_second" in results["concurrent_load"]:
            rps = results["concurrent_load"]["requests_per_second"]
            summary["key_metrics"]["requests_per_second"] = rps
            
            if rps < 10:
                summary["recommendations"].append("Low throughput (<10 RPS)")
        
        # Memory usage summary
        if "memory_usage" in results and "memory_stats" in results["memory_usage"]:
            memory_stats = results["memory_usage"]["memory_stats"]
            summary["key_metrics"]["peak_memory_percent"] = memory_stats["max_percent"]
            
            if memory_stats["max_percent"] > 80:
                summary["recommendations"].append("High memory usage (>80%)")
        
        if not summary["recommendations"]:
            summary["recommendations"].append("All metrics within acceptable ranges")
        
        return summary

if __name__ == "__main__":
    benchmark = ModelPerformanceBenchmark()
    results = benchmark.run_comprehensive_benchmark()
    
    print("\n🎯 BENCHMARK SUMMARY:")
    if "summary" in results:
        summary = results["summary"]
        print(f"Overall Status: {summary['overall_status']}")
        print("Key Metrics:")
        for metric, value in summary["key_metrics"].items():
            print(f"  - {metric}: {value}")
        print("Recommendations:")
        for rec in summary["recommendations"]:
            print(f"  - {rec}")
