#!/usr/bin/env python3
"""
Validation Middleware for Multimodal Sentiment Analysis API
Day 2 requirement: Comprehensive validation middleware with detailed error responses
"""

import time
import json
import logging
from typing import Dict, Any, Optional
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from model_versioning import get_response_formatter

class ValidationMiddleware(BaseHTTPMiddleware):
    """Comprehensive validation middleware for all API endpoints"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.response_formatter = get_response_formatter()
        self.logger = logging.getLogger(__name__)
        
        # Rate limiting storage (simple in-memory for demo)
        self.request_counts = {}
        self.rate_limit_window = 60  # 1 minute
        self.max_requests_per_minute = 100
        
    async def dispatch(self, request: Request, call_next):
        """Main middleware dispatch method"""
        start_time = time.time()
        
        try:
            # Pre-request validation
            await self._validate_request(request)
            
            # Process request
            response = await call_next(request)
            
            # Post-request processing
            processing_time = time.time() - start_time
            await self._log_request(request, response, processing_time)
            
            return response
            
        except HTTPException as e:
            # Handle validation errors with enhanced error responses
            processing_time = time.time() - start_time
            return await self._handle_validation_error(request, e, processing_time)
            
        except Exception as e:
            # Handle unexpected errors
            processing_time = time.time() - start_time
            return await self._handle_unexpected_error(request, e, processing_time)
            
    async def _validate_request(self, request: Request):
        """Validate incoming request"""
        # Rate limiting validation
        await self._check_rate_limit(request)
        
        # Content-Type validation for POST requests
        if request.method == "POST":
            await self._validate_content_type(request)
            
        # Request size validation
        await self._validate_request_size(request)
        
        # Security headers validation
        await self._validate_security_headers(request)
        
    async def _check_rate_limit(self, request: Request):
        """Check rate limiting"""
        client_ip = self._get_client_ip(request)
        current_time = time.time()
        
        # Clean old entries
        self.request_counts = {
            ip: [(timestamp, count) for timestamp, count in requests 
                 if current_time - timestamp < self.rate_limit_window]
            for ip, requests in self.request_counts.items()
        }
        
        # Count requests for this IP
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = []
            
        recent_requests = len(self.request_counts[client_ip])
        
        if recent_requests >= self.max_requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Maximum {self.max_requests_per_minute} requests per minute allowed."
            )
            
        # Add current request
        self.request_counts[client_ip].append((current_time, 1))
        
    async def _validate_content_type(self, request: Request):
        """Validate Content-Type for POST requests"""
        content_type = request.headers.get("content-type", "")
        
        # Allow multipart/form-data for file uploads
        if request.url.path.startswith("/predict/"):
            if not (content_type.startswith("multipart/form-data") or 
                   content_type.startswith("application/json")):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid Content-Type. Expected 'multipart/form-data' for file uploads or 'application/json' for text."
                )
        elif content_type and not content_type.startswith("application/json"):
            raise HTTPException(
                status_code=400,
                detail="Invalid Content-Type. Expected 'application/json'."
            )
            
    async def _validate_request_size(self, request: Request):
        """Validate request size"""
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                size = int(content_length)
                max_size = 52428800  # 50MB (Day 2 requirement)
                
                if size > max_size:
                    size_mb = size / (1024 * 1024)
                    max_mb = max_size / (1024 * 1024)
                    raise HTTPException(
                        status_code=413,
                        detail=f"Request too large ({size_mb:.1f}MB). Maximum allowed: {max_mb:.0f}MB"
                    )
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid Content-Length header"
                )
                
    async def _validate_security_headers(self, request: Request):
        """Validate security-related headers"""
        # Check for potentially malicious headers
        suspicious_headers = [
            "x-forwarded-host",
            "x-real-ip", 
            "x-forwarded-for"
        ]
        
        for header in suspicious_headers:
            value = request.headers.get(header, "")
            if value and any(char in value for char in ["<", ">", "script", "javascript"]):
                raise HTTPException(
                    status_code=400,
                    detail="Potentially malicious header detected"
                )
                
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        # Check for forwarded headers first
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
            
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
            
        # Fallback to direct client
        return request.client.host if request.client else "unknown"
        
    async def _handle_validation_error(self, request: Request, error: HTTPException, processing_time: float):
        """Handle validation errors with enhanced error responses"""
        error_response = self.response_formatter.format_error_response(
            error_message=error.detail,
            error_code=f"VALIDATION_ERROR_{error.status_code}",
            details={
                "endpoint": str(request.url.path),
                "method": request.method,
                "processing_time": round(processing_time, 4),
                "timestamp": time.time()
            }
        )
        
        # Log the validation error
        self.logger.warning(
            f"Validation error: {error.status_code} - {error.detail} - "
            f"Path: {request.url.path} - IP: {self._get_client_ip(request)}"
        )
        
        return JSONResponse(
            status_code=error.status_code,
            content=error_response
        )
        
    async def _handle_unexpected_error(self, request: Request, error: Exception, processing_time: float):
        """Handle unexpected errors"""
        error_response = self.response_formatter.format_error_response(
            error_message="Internal server error occurred",
            error_code="INTERNAL_SERVER_ERROR",
            details={
                "endpoint": str(request.url.path),
                "method": request.method,
                "processing_time": round(processing_time, 4),
                "timestamp": time.time()
            }
        )
        
        # Log the unexpected error
        self.logger.error(
            f"Unexpected error: {str(error)} - "
            f"Path: {request.url.path} - IP: {self._get_client_ip(request)}",
            exc_info=True
        )
        
        return JSONResponse(
            status_code=500,
            content=error_response
        )
        
    async def _log_request(self, request: Request, response: Response, processing_time: float):
        """Log request details"""
        if response.status_code >= 400:
            log_level = logging.WARNING if response.status_code < 500 else logging.ERROR
        else:
            log_level = logging.INFO
            
        self.logger.log(
            log_level,
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {processing_time:.4f}s - "
            f"IP: {self._get_client_ip(request)}"
        )

class RequestValidationHelper:
    """Helper class for additional request validation"""
    
    @staticmethod
    def validate_json_payload(payload: Dict[str, Any], required_fields: list = None) -> Dict[str, Any]:
        """Validate JSON payload structure"""
        if not isinstance(payload, dict):
            raise HTTPException(
                status_code=400,
                detail="Request body must be a JSON object"
            )
            
        if required_fields:
            missing_fields = [field for field in required_fields if field not in payload]
            if missing_fields:
                raise HTTPException(
                    status_code=422,
                    detail=f"Missing required fields: {', '.join(missing_fields)}"
                )
                
        return payload
        
    @staticmethod
    def validate_query_parameters(params: Dict[str, Any], allowed_params: list = None) -> Dict[str, Any]:
        """Validate query parameters"""
        if allowed_params:
            invalid_params = [param for param in params.keys() if param not in allowed_params]
            if invalid_params:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid query parameters: {', '.join(invalid_params)}"
                )
                
        return params
        
    @staticmethod
    def sanitize_string_parameter(value: str, max_length: int = 1000) -> str:
        """Sanitize string parameters"""
        if not isinstance(value, str):
            raise HTTPException(
                status_code=400,
                detail="Parameter must be a string"
            )
            
        if len(value) > max_length:
            raise HTTPException(
                status_code=400,
                detail=f"Parameter too long. Maximum length: {max_length}"
            )
            
        # Remove potentially dangerous characters
        sanitized = ''.join(char for char in value if ord(char) >= 32 or char in '\t\n\r')
        
        return sanitized.strip()

# Middleware configuration
def configure_validation_middleware(app):
    """Configure validation middleware for the FastAPI app"""
    app.add_middleware(ValidationMiddleware)
    
    # Add CORS headers middleware
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure based on environment
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

if __name__ == "__main__":
    # Test the validation helper
    helper = RequestValidationHelper()
    
    # Test JSON validation
    try:
        test_payload = {"text": "Hello world"}
        validated = helper.validate_json_payload(test_payload, ["text"])
        print("JSON validation passed:", validated)
    except HTTPException as e:
        print("JSON validation failed:", e.detail)
        
    # Test parameter sanitization
    try:
        sanitized = helper.sanitize_string_parameter("Hello <script>alert('test')</script> world")
        print("Sanitized parameter:", sanitized)
    except HTTPException as e:
        print("Parameter sanitization failed:", e.detail)
