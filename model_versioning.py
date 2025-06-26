#!/usr/bin/env python3
"""
Model Versioning System - Day 2 CRITICAL Requirement
Implements the EXACT JSON structure required in feedback:

{
  "sentiment": "positive",
  "confidence": 0.88,
  "model_version": {
    "text": "v1.0",
    "audio": "v1.0",
    "video": "v1.0",
    "fusion": "v1.0"
  }
}
"""

import os
import json
from typing import Dict, Any, Optional, List
from datetime import datetime

class ModelVersionManager:
    """Manages model versions for API responses - Day 2 requirement"""

    def __init__(self):
        # Day 2 EXACT requirement + Advanced Analysis: these version tags MUST appear in responses
        self.model_versions = {
            "text": os.getenv('TEXT_MODEL_VERSION', 'v2.0'),  # Updated to v2.0 for advanced analysis
            "audio": os.getenv('AUDIO_MODEL_VERSION', 'v1.0'),
            "video": os.getenv('VIDEO_MODEL_VERSION', 'v1.0'),
            "fusion": os.getenv('FUSION_MODEL_VERSION', 'v1.0')
        }

    def get_model_version_dict(self, used_models: List[str] = None) -> Dict[str, str]:
        """
        Get model version dictionary for API responses
        Day 2 requirement: EXACT format specified in feedback
        """
        if used_models is None:
            # Return all versions
            return {
                "text": self.model_versions["text"],
                "audio": self.model_versions["audio"],
                "video": self.model_versions["video"],
                "fusion": self.model_versions["fusion"]
            }
        else:
            # Return only versions for models that were used
            version_dict = {}
            for model in used_models:
                if model in self.model_versions:
                    version_dict[model] = self.model_versions[model]
            return version_dict

def format_api_response(sentiment: str, confidence: float, used_models: List[str], **kwargs) -> Dict[str, Any]:
    """
    Format API response with EXACT Day 2 structure
    This is the CRITICAL missing piece from feedback
    """
    version_manager = ModelVersionManager()

    # Day 2 EXACT format requirement
    response = {
        "sentiment": sentiment,
        "confidence": round(confidence, 2),
        "model_version": version_manager.get_model_version_dict(used_models)
    }

    # Add any additional fields
    for key, value in kwargs.items():
        if key not in response:  # Don't override core fields
            response[key] = value

    return response

def format_multimodal_response(
    fused_sentiment: str,
    fused_confidence: float,
    individual_results: List[Dict],
    used_models: List[str],
    **kwargs
) -> Dict[str, Any]:
    """Format multimodal response with Day 2 version structure"""
    version_manager = ModelVersionManager()

    response = {
        "sentiment": fused_sentiment,  # Use 'sentiment' not 'fused_sentiment' for consistency
        "confidence": round(fused_confidence, 2),
        "individual": individual_results,
        "model_version": version_manager.get_model_version_dict(used_models)
    }

    # Add any additional fields
    for key, value in kwargs.items():
        if key not in response:
            response[key] = value

    return response

# Global instance
_version_manager = ModelVersionManager()

def get_version_manager() -> ModelVersionManager:
    """Get global version manager instance"""
    return _version_manager

    def get_model_version(self, model_type: str) -> str:
        """Get version for a specific model type"""
        return self._version_cache.get(model_type, "v1.0")
        
    def get_all_versions(self) -> Dict[str, str]:
        """Get all model versions"""
        return self._version_cache.copy()
        
    def get_version_info(self, model_types: list = None) -> Dict[str, str]:
        """Get version info for specified model types or all models"""
        if model_types is None:
            return self.get_all_versions()
            
        return {
            model_type: self.get_model_version(model_type) 
            for model_type in model_types
        }
        
    def update_model_version(self, model_type: str, version: str):
        """Update version for a specific model type"""
        if model_type in self._version_cache:
            self._version_cache[model_type] = version
        else:
            raise ValueError(f"Unknown model type: {model_type}")
            
    def get_api_response_versions(self, used_models: list = None) -> Dict[str, str]:
        """Get model versions formatted for API responses (Day 2 requirement)"""
        if used_models is None:
            # Return all versions
            return {
                "text": self.get_model_version("text"),
                "audio": self.get_model_version("audio"),
                "video": self.get_model_version("video"),
                "fusion": self.get_model_version("fusion")
            }
        else:
            # Return only versions for models that were actually used
            versions = {}
            for model_type in used_models:
                versions[model_type] = self.get_model_version(model_type)
            return versions
            
    def get_detailed_version_info(self) -> Dict[str, Any]:
        """Get detailed version information including metadata"""
        return {
            "model_versions": self.get_all_versions(),
            "system_info": {
                "api_version": "v2.0",  # Day 2 API version
                "last_updated": datetime.now().isoformat(),
                "validation_enhanced": True,
                "features": [
                    "enhanced_file_validation",
                    "magic_number_verification", 
                    "strict_size_limits",
                    "comprehensive_sanitization"
                ]
            }
        }
        
    def validate_model_versions(self) -> Dict[str, Any]:
        """Validate that all required model versions are available"""
        required_models = ["text", "audio", "video", "fusion"]
        validation_result = {
            "valid": True,
            "missing_versions": [],
            "available_versions": {}
        }
        
        for model_type in required_models:
            version = self.get_model_version(model_type)
            if version:
                validation_result["available_versions"][model_type] = version
            else:
                validation_result["missing_versions"].append(model_type)
                validation_result["valid"] = False
                
        return validation_result

class ResponseFormatter:
    """Formats API responses with model versioning (Day 2 requirement)"""
    
    def __init__(self, version_manager: ModelVersionManager):
        self.version_manager = version_manager
        
    def format_prediction_response(
        self, 
        sentiment: str, 
        confidence: float, 
        used_models: list,
        additional_data: Dict[str, Any] = None,
        prediction_id: str = None,
        processing_time: float = None
    ) -> Dict[str, Any]:
        """Format prediction response with model versions (Day 2 format)"""
        
        response = {
            "sentiment": sentiment,
            "confidence": round(confidence, 4),
            "model_version": self.version_manager.get_api_response_versions(used_models)
        }
        
        # Add optional fields
        if prediction_id:
            response["prediction_id"] = prediction_id
            
        if processing_time is not None:
            response["processing_time"] = round(processing_time, 4)
            
        # Add any additional data
        if additional_data:
            response.update(additional_data)
            
        return response
        
    def format_multimodal_response(
        self,
        fused_sentiment: str,
        fused_confidence: float,
        individual_results: list,
        used_models: list,
        prediction_id: str = None,
        processing_time: float = None
    ) -> Dict[str, Any]:
        """Format multimodal prediction response with model versions"""
        
        response = {
            "fused_sentiment": fused_sentiment,
            "confidence": round(fused_confidence, 4),
            "individual": individual_results,
            "model_version": self.version_manager.get_api_response_versions(used_models)
        }
        
        # Add optional fields
        if prediction_id:
            response["prediction_id"] = prediction_id
            
        if processing_time is not None:
            response["processing_time"] = round(processing_time, 4)
            
        return response
        
    def format_error_response(
        self,
        error_message: str,
        error_code: str = None,
        details: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Format error response with system version info"""
        
        response = {
            "error": error_message,
            "system_version": {
                "api": "v2.0",
                "validation": "enhanced"
            }
        }
        
        if error_code:
            response["error_code"] = error_code
            
        if details:
            response["details"] = details
            
        return response
        
    def format_health_response(self) -> Dict[str, Any]:
        """Format health check response with version info"""
        
        return {
            "status": "healthy",
            "message": "API is running",
            "version_info": self.version_manager.get_detailed_version_info(),
            "validation": {
                "enhanced_file_validation": True,
                "magic_number_verification": True,
                "strict_size_limits": True,
                "comprehensive_sanitization": True
            }
        }

# Global instances
_version_manager = None
_response_formatter = None

def get_version_manager(config_loader=None) -> ModelVersionManager:
    """Get global version manager instance"""
    global _version_manager
    if _version_manager is None:
        _version_manager = ModelVersionManager(config_loader)
    return _version_manager

def get_response_formatter(config_loader=None) -> ResponseFormatter:
    """Get global response formatter instance"""
    global _response_formatter
    if _response_formatter is None:
        version_manager = get_version_manager(config_loader)
        _response_formatter = ResponseFormatter(version_manager)
    return _response_formatter

def format_api_response(
    sentiment: str,
    confidence: float,
    used_models: list,
    **kwargs
) -> Dict[str, Any]:
    """Convenience function for formatting API responses (Day 2 requirement)"""
    formatter = get_response_formatter()
    return formatter.format_prediction_response(
        sentiment=sentiment,
        confidence=confidence,
        used_models=used_models,
        **kwargs
    )

if __name__ == "__main__":
    # Test the versioning system
    vm = ModelVersionManager()
    print("Model Versions:", vm.get_all_versions())
    
    formatter = ResponseFormatter(vm)
    
    # Test Day 2 response format
    response = formatter.format_prediction_response(
        sentiment="positive",
        confidence=0.88,
        used_models=["text"],
        prediction_id="test_123",
        processing_time=0.045
    )
    
    print("\nDay 2 Response Format:")
    print(json.dumps(response, indent=2))
