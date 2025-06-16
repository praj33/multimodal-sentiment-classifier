# benchmark_system.py - Comprehensive latency and performance benchmarking

import time
import psutil
import json
import statistics
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
import aiohttp
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

class PerformanceBenchmark:
    """Comprehensive performance benchmarking system"""
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.results = []
        self.system_metrics = []
        
    def measure_system_resources(self) -> Dict[str, float]:
        """Measure current system resource usage"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_used_mb": psutil.virtual_memory().used / (1024 * 1024),
            "disk_usage_percent": psutil.disk_usage('/').percent,
            "timestamp": time.time()
        }
    
    def benchmark_text_analysis(self, texts: List[str], iterations: int = 10) -> Dict[str, Any]:
        """Benchmark text analysis performance"""
        print(f"🔍 Benchmarking text analysis with {len(texts)} samples, {iterations} iterations...")
        
        results = []
        system_metrics = []
        
        for i in range(iterations):
            for text in texts:
                start_time = time.time()
                start_metrics = self.measure_system_resources()
                
                try:
                    response = requests.post(
                        f"{self.api_base_url}/predict/text",
                        json={"text": text},
                        timeout=30
                    )
                    
                    end_time = time.time()
                    end_metrics = self.measure_system_resources()
                    
                    latency_ms = (end_time - start_time) * 1000
                    
                    if response.status_code == 200:
                        result_data = response.json()
                        results.append({
                            "iteration": i + 1,
                            "text_length": len(text),
                            "latency_ms": latency_ms,
                            "confidence": result_data.get("confidence", 0),
                            "sentiment": result_data.get("sentiment", "unknown"),
                            "success": True
                        })
                    else:
                        results.append({
                            "iteration": i + 1,
                            "text_length": len(text),
                            "latency_ms": latency_ms,
                            "error": f"HTTP {response.status_code}",
                            "success": False
                        })
                    
                    system_metrics.append({
                        "start": start_metrics,
                        "end": end_metrics,
                        "cpu_delta": end_metrics["cpu_percent"] - start_metrics["cpu_percent"],
                        "memory_delta": end_metrics["memory_used_mb"] - start_metrics["memory_used_mb"]
                    })
                    
                except Exception as e:
                    end_time = time.time()
                    latency_ms = (end_time - start_time) * 1000
                    results.append({
                        "iteration": i + 1,
                        "text_length": len(text),
                        "latency_ms": latency_ms,
                        "error": str(e),
                        "success": False
                    })
        
        return self._analyze_results(results, system_metrics, "text")
    
    def benchmark_audio_analysis(self, audio_files: List[str], iterations: int = 5) -> Dict[str, Any]:
        """Benchmark audio analysis performance"""
        print(f"🎵 Benchmarking audio analysis with {len(audio_files)} files, {iterations} iterations...")
        
        results = []
        system_metrics = []
        
        for i in range(iterations):
            for audio_file in audio_files:
                if not os.path.exists(audio_file):
                    print(f"⚠️ Audio file not found: {audio_file}")
                    continue
                    
                start_time = time.time()
                start_metrics = self.measure_system_resources()
                
                try:
                    with open(audio_file, 'rb') as f:
                        files = {'file': f}
                        response = requests.post(
                            f"{self.api_base_url}/predict/audio",
                            files=files,
                            timeout=60
                        )
                    
                    end_time = time.time()
                    end_metrics = self.measure_system_resources()
                    
                    latency_ms = (end_time - start_time) * 1000
                    file_size_mb = os.path.getsize(audio_file) / (1024 * 1024)
                    
                    if response.status_code == 200:
                        result_data = response.json()
                        results.append({
                            "iteration": i + 1,
                            "file_size_mb": file_size_mb,
                            "latency_ms": latency_ms,
                            "confidence": result_data.get("confidence", 0),
                            "sentiment": result_data.get("sentiment", "unknown"),
                            "success": True
                        })
                    else:
                        results.append({
                            "iteration": i + 1,
                            "file_size_mb": file_size_mb,
                            "latency_ms": latency_ms,
                            "error": f"HTTP {response.status_code}",
                            "success": False
                        })
                    
                    system_metrics.append({
                        "start": start_metrics,
                        "end": end_metrics,
                        "cpu_delta": end_metrics["cpu_percent"] - start_metrics["cpu_percent"],
                        "memory_delta": end_metrics["memory_used_mb"] - start_metrics["memory_used_mb"]
                    })
                    
                except Exception as e:
                    end_time = time.time()
                    latency_ms = (end_time - start_time) * 1000
                    results.append({
                        "iteration": i + 1,
                        "file_size_mb": os.path.getsize(audio_file) / (1024 * 1024) if os.path.exists(audio_file) else 0,
                        "latency_ms": latency_ms,
                        "error": str(e),
                        "success": False
                    })
        
        return self._analyze_results(results, system_metrics, "audio")
    
    def benchmark_video_analysis(self, video_files: List[str], iterations: int = 3) -> Dict[str, Any]:
        """Benchmark video analysis performance"""
        print(f"🎥 Benchmarking video analysis with {len(video_files)} files, {iterations} iterations...")
        
        results = []
        system_metrics = []
        
        for i in range(iterations):
            for video_file in video_files:
                if not os.path.exists(video_file):
                    print(f"⚠️ Video file not found: {video_file}")
                    continue
                    
                start_time = time.time()
                start_metrics = self.measure_system_resources()
                
                try:
                    with open(video_file, 'rb') as f:
                        files = {'file': f}
                        response = requests.post(
                            f"{self.api_base_url}/predict/video",
                            files=files,
                            timeout=120
                        )
                    
                    end_time = time.time()
                    end_metrics = self.measure_system_resources()
                    
                    latency_ms = (end_time - start_time) * 1000
                    file_size_mb = os.path.getsize(video_file) / (1024 * 1024)
                    
                    if response.status_code == 200:
                        result_data = response.json()
                        results.append({
                            "iteration": i + 1,
                            "file_size_mb": file_size_mb,
                            "latency_ms": latency_ms,
                            "confidence": result_data.get("confidence", 0),
                            "sentiment": result_data.get("sentiment", "unknown"),
                            "success": True
                        })
                    else:
                        results.append({
                            "iteration": i + 1,
                            "file_size_mb": file_size_mb,
                            "latency_ms": latency_ms,
                            "error": f"HTTP {response.status_code}",
                            "success": False
                        })
                    
                    system_metrics.append({
                        "start": start_metrics,
                        "end": end_metrics,
                        "cpu_delta": end_metrics["cpu_percent"] - start_metrics["cpu_percent"],
                        "memory_delta": end_metrics["memory_used_mb"] - start_metrics["memory_used_mb"]
                    })
                    
                except Exception as e:
                    end_time = time.time()
                    latency_ms = (end_time - start_time) * 1000
                    results.append({
                        "iteration": i + 1,
                        "file_size_mb": os.path.getsize(video_file) / (1024 * 1024) if os.path.exists(video_file) else 0,
                        "latency_ms": latency_ms,
                        "error": str(e),
                        "success": False
                    })
        
        return self._analyze_results(results, system_metrics, "video")
    
    def benchmark_concurrent_requests(self, num_concurrent: int = 10, total_requests: int = 100) -> Dict[str, Any]:
        """Benchmark concurrent request handling"""
        print(f"⚡ Benchmarking concurrent requests: {num_concurrent} concurrent, {total_requests} total...")
        
        test_texts = [
            "I love this product!",
            "This is terrible.",
            "It's okay, nothing special.",
            "Amazing experience!",
            "Could be better."
        ]
        
        results = []
        start_time = time.time()
        
        def make_request(text: str) -> Dict[str, Any]:
            request_start = time.time()
            try:
                response = requests.post(
                    f"{self.api_base_url}/predict/text",
                    json={"text": text},
                    timeout=30
                )
                request_end = time.time()
                
                return {
                    "latency_ms": (request_end - request_start) * 1000,
                    "status_code": response.status_code,
                    "success": response.status_code == 200,
                    "response_data": response.json() if response.status_code == 200 else None
                }
            except Exception as e:
                request_end = time.time()
                return {
                    "latency_ms": (request_end - request_start) * 1000,
                    "error": str(e),
                    "success": False
                }
        
        with ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            futures = []
            for i in range(total_requests):
                text = test_texts[i % len(test_texts)]
                future = executor.submit(make_request, text)
                futures.append(future)
            
            for future in as_completed(futures):
                results.append(future.result())
        
        end_time = time.time()
        total_time = end_time - start_time
        
        successful_requests = [r for r in results if r["success"]]
        failed_requests = [r for r in results if not r["success"]]
        
        if successful_requests:
            latencies = [r["latency_ms"] for r in successful_requests]
            
            return {
                "test_type": "concurrent",
                "total_requests": total_requests,
                "concurrent_users": num_concurrent,
                "total_time_seconds": total_time,
                "requests_per_second": total_requests / total_time,
                "successful_requests": len(successful_requests),
                "failed_requests": len(failed_requests),
                "success_rate": len(successful_requests) / total_requests * 100,
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
            return {
                "test_type": "concurrent",
                "total_requests": total_requests,
                "successful_requests": 0,
                "failed_requests": len(failed_requests),
                "success_rate": 0,
                "error": "All requests failed"
            }
    
    def _analyze_results(self, results: List[Dict], system_metrics: List[Dict], test_type: str) -> Dict[str, Any]:
        """Analyze benchmark results"""
        successful_results = [r for r in results if r.get("success", False)]
        failed_results = [r for r in results if not r.get("success", False)]
        
        if not successful_results:
            return {
                "test_type": test_type,
                "total_tests": len(results),
                "successful_tests": 0,
                "failed_tests": len(failed_results),
                "success_rate": 0,
                "error": "All tests failed"
            }
        
        latencies = [r["latency_ms"] for r in successful_results]
        confidences = [r["confidence"] for r in successful_results if "confidence" in r]
        
        analysis = {
            "test_type": test_type,
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(results),
            "successful_tests": len(successful_results),
            "failed_tests": len(failed_results),
            "success_rate": len(successful_results) / len(results) * 100,
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
        
        if confidences:
            analysis["confidence_stats"] = {
                "min": min(confidences),
                "max": max(confidences),
                "mean": statistics.mean(confidences),
                "median": statistics.median(confidences)
            }
        
        if system_metrics:
            cpu_deltas = [m["cpu_delta"] for m in system_metrics]
            memory_deltas = [m["memory_delta"] for m in system_metrics]
            
            analysis["system_impact"] = {
                "avg_cpu_increase": statistics.mean(cpu_deltas),
                "avg_memory_increase_mb": statistics.mean(memory_deltas),
                "max_cpu_increase": max(cpu_deltas),
                "max_memory_increase_mb": max(memory_deltas)
            }
        
        return analysis
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile"""
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]
    
    def save_results(self, results: Dict[str, Any], filename: str = None):
        """Save benchmark results to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/benchmark_results_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📊 Benchmark results saved to: {filename}")
        return filename
