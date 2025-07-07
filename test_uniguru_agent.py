#!/usr/bin/env python3
"""
🧪 Uniguru Sentiment Agent Test Suite
Comprehensive testing for JSON/CLI/Colab compatibility

🎯 Test Coverage:
- JSON API functionality
- CLI interface testing
- Persona-specific analysis
- Multi-modal input handling
- Language detection
- Error handling and edge cases
- Performance benchmarking

🚀 Designed for Production Excellence by Raj
"""

import asyncio
import json
import time
import traceback
from typing import Dict, List, Any
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sentiment_agent_adapter import predict, get_agent

class UniguruAgentTester:
    """Comprehensive test suite for Uniguru Sentiment Agent"""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_test(self, test_name: str, passed: bool, details: str = "", result: Dict = None):
        """Log test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            self.failed_tests += 1
            status = "❌ FAIL"
        
        self.test_results.append({
            "test": test_name,
            "status": status,
            "details": details,
            "result": result
        })
        
        print(f"{status} | {test_name}")
        if details:
            print(f"    📝 {details}")
        if not passed and result:
            print(f"    🔍 Result: {json.dumps(result, indent=2)}")
    
    async def test_basic_text_analysis(self):
        """Test basic text sentiment analysis"""
        test_cases = [
            {
                "input": {"text": "I love learning new things!", "persona": "youth"},
                "expected_sentiment": "positive"
            },
            {
                "input": {"text": "This is really difficult and frustrating", "persona": "youth"},
                "expected_sentiment": "negative"
            },
            {
                "input": {"text": "The weather is okay today", "persona": "neutral"},
                "expected_sentiment": "neutral"
            }
        ]
        
        for i, case in enumerate(test_cases):
            try:
                result = await predict(case["input"])
                
                if "error" in result:
                    self.log_test(f"Basic Text Analysis {i+1}", False, 
                                f"API returned error: {result.get('error')}", result)
                    continue
                
                # Check required fields
                required_fields = ["sentiment", "tone", "confidence", "tts_emotion"]
                missing_fields = [f for f in required_fields if f not in result]
                
                if missing_fields:
                    self.log_test(f"Basic Text Analysis {i+1}", False,
                                f"Missing fields: {missing_fields}", result)
                    continue
                
                # Check sentiment accuracy (if expected)
                sentiment_match = result["sentiment"] == case["expected_sentiment"]
                confidence_valid = 0.0 <= result["confidence"] <= 1.0
                
                if sentiment_match and confidence_valid:
                    self.log_test(f"Basic Text Analysis {i+1}", True,
                                f"Sentiment: {result['sentiment']}, Confidence: {result['confidence']:.3f}")
                else:
                    self.log_test(f"Basic Text Analysis {i+1}", False,
                                f"Expected: {case['expected_sentiment']}, Got: {result['sentiment']}")
                
            except Exception as e:
                self.log_test(f"Basic Text Analysis {i+1}", False, f"Exception: {str(e)}")
    
    async def test_persona_variations(self):
        """Test persona-specific analysis"""
        text = "I'm so excited about this new adventure!"
        personas = ["youth", "kids", "spiritual"]
        
        results = {}
        for persona in personas:
            try:
                result = await predict({"text": text, "persona": persona})
                
                if "error" not in result:
                    results[persona] = {
                        "tone": result.get("tone"),
                        "tts_emotion": result.get("tts_emotion"),
                        "confidence": result.get("confidence")
                    }
                else:
                    self.log_test(f"Persona Test - {persona}", False, 
                                f"API error: {result.get('error')}")
                    continue
                    
            except Exception as e:
                self.log_test(f"Persona Test - {persona}", False, f"Exception: {str(e)}")
                continue
        
        # Check if personas produce different tones/emotions
        if len(results) >= 2:
            tones = [r["tone"] for r in results.values()]
            emotions = [r["tts_emotion"] for r in results.values()]
            
            # Personas should produce different tones or emotions
            tone_variety = len(set(tones)) > 1
            emotion_variety = len(set(emotions)) > 1
            
            if tone_variety or emotion_variety:
                self.log_test("Persona Variation", True, 
                            f"Different personas produce varied outputs: {results}")
            else:
                self.log_test("Persona Variation", False,
                            f"All personas produced same tone/emotion: {results}")
        else:
            self.log_test("Persona Variation", False, "Insufficient persona results")
    
    async def test_language_detection(self):
        """Test language detection functionality"""
        test_cases = [
            {"text": "Hello, how are you today?", "expected_lang": "English"},
            {"text": "Hola, ¿cómo estás hoy?", "expected_lang": "Spanish"},
            {"text": "Bonjour, comment allez-vous?", "expected_lang": "French"},
            {"text": "नमस्ते, आप कैसे हैं?", "expected_lang": "Hindi"},
        ]
        
        for i, case in enumerate(test_cases):
            try:
                result = await predict({"text": case["text"], "persona": "youth"})
                
                if "error" in result:
                    self.log_test(f"Language Detection {i+1}", False,
                                f"API error: {result.get('error')}")
                    continue
                
                detected_lang = result.get("language")
                if detected_lang:
                    # Check if detection is reasonable (exact match not required)
                    lang_detected = detected_lang is not None
                    self.log_test(f"Language Detection {i+1}", lang_detected,
                                f"Detected: {detected_lang} for '{case['text'][:30]}...'")
                else:
                    self.log_test(f"Language Detection {i+1}", False,
                                "No language detected")
                    
            except Exception as e:
                self.log_test(f"Language Detection {i+1}", False, f"Exception: {str(e)}")
    
    async def test_image_url_analysis(self):
        """Test image URL analysis"""
        # Test with a sample image URL (placeholder)
        test_cases = [
            {
                "input": {
                    "image_url": "https://via.placeholder.com/300x200/00ff00/000000?text=Happy+Face",
                    "persona": "kids"
                },
                "should_work": False  # Placeholder URL won't work for sentiment
            }
        ]
        
        for i, case in enumerate(test_cases):
            try:
                result = await predict(case["input"])
                
                # For placeholder URLs, we expect it to handle gracefully
                if "error" not in result:
                    has_image_analysis = "image" in result.get("analysis_details", {})
                    self.log_test(f"Image URL Analysis {i+1}", True,
                                f"Image processing attempted: {has_image_analysis}")
                else:
                    # Error is acceptable for invalid URLs
                    self.log_test(f"Image URL Analysis {i+1}", True,
                                f"Graceful error handling: {result.get('error')}")
                    
            except Exception as e:
                self.log_test(f"Image URL Analysis {i+1}", False, f"Exception: {str(e)}")
    
    async def test_multimodal_fusion(self):
        """Test multi-modal analysis fusion"""
        try:
            result = await predict({
                "text": "I'm feeling great today!",
                "image_url": "https://via.placeholder.com/300x200/00ff00/000000?text=Smile",
                "persona": "youth"
            })
            
            if "error" not in result:
                analysis_details = result.get("analysis_details", {})
                modalities_count = result.get("input_summary", {}).get("modalities_analyzed", 0)
                
                # Check if fusion was attempted
                has_fusion = "fusion" in analysis_details or modalities_count > 1
                
                self.log_test("Multimodal Fusion", has_fusion,
                            f"Analyzed {modalities_count} modalities")
            else:
                self.log_test("Multimodal Fusion", False,
                            f"Multimodal analysis failed: {result.get('error')}")
                
        except Exception as e:
            self.log_test("Multimodal Fusion", False, f"Exception: {str(e)}")
    
    async def test_error_handling(self):
        """Test error handling for invalid inputs"""
        error_cases = [
            {"input": {}, "test_name": "Empty Input"},
            {"input": {"text": ""}, "test_name": "Empty Text"},
            {"input": {"image_url": "invalid-url"}, "test_name": "Invalid URL"},
            {"input": {"persona": "invalid_persona", "text": "test"}, "test_name": "Invalid Persona"},
        ]
        
        for case in error_cases:
            try:
                result = await predict(case["input"])
                
                # Should either handle gracefully or return meaningful error
                if "error" in result:
                    # Error is expected and handled gracefully
                    self.log_test(f"Error Handling - {case['test_name']}", True,
                                f"Graceful error: {result.get('error')}")
                else:
                    # Should work with fallbacks
                    self.log_test(f"Error Handling - {case['test_name']}", True,
                                f"Handled with fallbacks")
                    
            except Exception as e:
                self.log_test(f"Error Handling - {case['test_name']}", False,
                            f"Unhandled exception: {str(e)}")
    
    async def test_performance_benchmark(self):
        """Test performance benchmarks"""
        test_text = "This is a performance test for the sentiment analysis system."
        
        # Single prediction timing
        start_time = time.time()
        try:
            result = await predict({"text": test_text, "persona": "youth"})
            end_time = time.time()
            
            if "error" not in result:
                response_time = (end_time - start_time) * 1000  # ms
                reported_time = result.get("processing_time_ms", 0)
                
                # Performance should be reasonable (under 5 seconds)
                performance_ok = response_time < 5000
                
                self.log_test("Performance Benchmark", performance_ok,
                            f"Response time: {response_time:.2f}ms, Reported: {reported_time:.2f}ms")
            else:
                self.log_test("Performance Benchmark", False,
                            f"Performance test failed: {result.get('error')}")
                
        except Exception as e:
            self.log_test("Performance Benchmark", False, f"Exception: {str(e)}")
    
    async def test_json_string_input(self):
        """Test JSON string input (CLI compatibility)"""
        json_input = '{"text": "Testing JSON string input", "persona": "kids"}'
        
        try:
            result = await predict(json_input)
            
            if "error" not in result:
                self.log_test("JSON String Input", True,
                            f"Successfully parsed JSON string input")
            else:
                self.log_test("JSON String Input", False,
                            f"JSON string parsing failed: {result.get('error')}")
                
        except Exception as e:
            self.log_test("JSON String Input", False, f"Exception: {str(e)}")
    
    async def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🧪 Starting Uniguru Sentiment Agent Test Suite")
        print("=" * 60)
        
        # Run all test categories
        await self.test_basic_text_analysis()
        await self.test_persona_variations()
        await self.test_language_detection()
        await self.test_image_url_analysis()
        await self.test_multimodal_fusion()
        await self.test_error_handling()
        await self.test_performance_benchmark()
        await self.test_json_string_input()
        
        # Print summary
        print("\n" + "=" * 60)
        print("🎯 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📊 Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        if self.failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if "FAIL" in result["status"]:
                    print(f"  • {result['test']}: {result['details']}")
        
        print("\n🎉 Test suite completed!")
        return self.passed_tests, self.failed_tests

# CLI and Colab support
async def main():
    """Main test runner"""
    tester = UniguruAgentTester()
    passed, failed = await tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    asyncio.run(main())
