# input_validation.py - Enhanced input validation and sanitization

import re
import magic
import hashlib
from typing import Optional, Dict, Any, List
from fastapi import HTTPException, UploadFile
import bleach
import os

class InputValidator:
    """Enhanced input validation and sanitization"""
    
    def __init__(self):
        # File size limits (in bytes)
        self.MAX_FILE_SIZES = {
            'audio': 50 * 1024 * 1024,  # 50MB
            'video': 100 * 1024 * 1024,  # 100MB
            'image': 10 * 1024 * 1024,   # 10MB
        }
        
        # Allowed file types
        self.ALLOWED_MIME_TYPES = {
            'audio': [
                'audio/wav', 'audio/wave', 'audio/x-wav',
                'audio/mpeg', 'audio/mp3',
                'audio/mp4', 'audio/m4a',
                'audio/ogg', 'audio/webm'
            ],
            'video': [
                'video/mp4', 'video/mpeg', 'video/quicktime',
                'video/x-msvideo', 'video/avi',
                'video/webm', 'video/ogg'
            ],
            'image': [
                'image/jpeg', 'image/jpg', 'image/png',
                'image/gif', 'image/bmp', 'image/webp'
            ]
        }
        
        # Allowed file extensions
        self.ALLOWED_EXTENSIONS = {
            'audio': ['.wav', '.mp3', '.m4a', '.ogg', '.webm'],
            'video': ['.mp4', '.avi', '.mov', '.webm', '.ogg'],
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        }
        
        # Text validation limits
        self.MAX_TEXT_LENGTH = 10000
        self.MIN_TEXT_LENGTH = 1
        
        # Malicious patterns to detect
        self.MALICIOUS_PATTERNS = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'vbscript:',
            r'onload\s*=',
            r'onerror\s*=',
            r'onclick\s*=',
            r'eval\s*\(',
            r'exec\s*\(',
            r'system\s*\(',
            r'shell_exec\s*\(',
        ]
    
    def validate_text_input(self, text: str) -> str:
        """Validate and sanitize text input"""
        if not isinstance(text, str):
            raise HTTPException(status_code=400, detail="Text input must be a string")
        
        # Check length
        if len(text) < self.MIN_TEXT_LENGTH:
            raise HTTPException(status_code=400, detail="Text input too short")
        
        if len(text) > self.MAX_TEXT_LENGTH:
            raise HTTPException(status_code=400, detail=f"Text input too long (max {self.MAX_TEXT_LENGTH} characters)")
        
        # Check for malicious patterns
        for pattern in self.MALICIOUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                raise HTTPException(status_code=400, detail="Text contains potentially malicious content")
        
        # Sanitize HTML/script content
        sanitized_text = bleach.clean(text, tags=[], attributes={}, strip=True)
        
        # Remove excessive whitespace
        sanitized_text = re.sub(r'\s+', ' ', sanitized_text).strip()
        
        if not sanitized_text:
            raise HTTPException(status_code=400, detail="Text input is empty after sanitization")
        
        return sanitized_text
    
    def validate_file_upload(self, file: UploadFile, file_type: str) -> Dict[str, Any]:
        """Validate uploaded file"""
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Validate file type
        if file_type not in self.ALLOWED_MIME_TYPES:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_type}")
        
        # Check file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in self.ALLOWED_EXTENSIONS[file_type]:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file extension. Allowed: {', '.join(self.ALLOWED_EXTENSIONS[file_type])}"
            )
        
        # Read file content for validation
        file_content = file.file.read()
        file.file.seek(0)  # Reset file pointer
        
        # Check file size
        file_size = len(file_content)
        if file_size == 0:
            raise HTTPException(status_code=400, detail="File is empty")
        
        if file_size > self.MAX_FILE_SIZES[file_type]:
            max_size_mb = self.MAX_FILE_SIZES[file_type] / (1024 * 1024)
            raise HTTPException(
                status_code=400, 
                detail=f"File too large. Maximum size: {max_size_mb}MB"
            )
        
        # Validate MIME type using python-magic
        try:
            detected_mime = magic.from_buffer(file_content, mime=True)
            if detected_mime not in self.ALLOWED_MIME_TYPES[file_type]:
                raise HTTPException(
                    status_code=400, 
                    detail=f"File content doesn't match expected type. Detected: {detected_mime}"
                )
        except Exception as e:
            # Fallback validation if magic fails
            pass
        
        # Generate file hash for deduplication
        file_hash = hashlib.sha256(file_content).hexdigest()
        
        # Check for malicious file signatures
        if self._is_malicious_file(file_content):
            raise HTTPException(status_code=400, detail="File contains potentially malicious content")
        
        return {
            "filename": file.filename,
            "size": file_size,
            "mime_type": detected_mime if 'detected_mime' in locals() else file.content_type,
            "hash": file_hash,
            "extension": file_ext
        }
    
    def _is_malicious_file(self, content: bytes) -> bool:
        """Check for malicious file signatures"""
        # Check for executable signatures
        malicious_signatures = [
            b'\x4d\x5a',  # PE executable
            b'\x7f\x45\x4c\x46',  # ELF executable
            b'\xfe\xed\xfa',  # Mach-O executable
            b'#!/bin/sh',  # Shell script
            b'#!/bin/bash',  # Bash script
            b'<?php',  # PHP script
        ]
        
        content_start = content[:100].lower()
        
        for signature in malicious_signatures:
            if signature in content_start:
                return True
        
        # Check for suspicious strings in content
        suspicious_strings = [
            b'eval(',
            b'exec(',
            b'system(',
            b'shell_exec(',
            b'passthru(',
            b'<script',
            b'javascript:',
        ]
        
        for suspicious in suspicious_strings:
            if suspicious in content_start:
                return True
        
        return False
    
    def validate_api_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate API parameters"""
        validated_params = {}
        
        for key, value in params.items():
            # Sanitize parameter names
            clean_key = re.sub(r'[^a-zA-Z0-9_]', '', key)
            if not clean_key:
                continue
            
            # Validate parameter values
            if isinstance(value, str):
                # Sanitize string values
                clean_value = bleach.clean(value, tags=[], attributes={}, strip=True)
                clean_value = re.sub(r'[<>"\']', '', clean_value)
                validated_params[clean_key] = clean_value
            elif isinstance(value, (int, float)):
                # Validate numeric values
                if -1000000 <= value <= 1000000:  # Reasonable range
                    validated_params[clean_key] = value
            elif isinstance(value, bool):
                validated_params[clean_key] = value
        
        return validated_params
    
    def validate_confidence_threshold(self, threshold: float) -> float:
        """Validate confidence threshold parameter"""
        if not isinstance(threshold, (int, float)):
            raise HTTPException(status_code=400, detail="Confidence threshold must be a number")
        
        if not 0.0 <= threshold <= 1.0:
            raise HTTPException(status_code=400, detail="Confidence threshold must be between 0.0 and 1.0")
        
        return float(threshold)
    
    def validate_batch_size(self, batch_size: int) -> int:
        """Validate batch processing size"""
        if not isinstance(batch_size, int):
            raise HTTPException(status_code=400, detail="Batch size must be an integer")
        
        if not 1 <= batch_size <= 100:
            raise HTTPException(status_code=400, detail="Batch size must be between 1 and 100")
        
        return batch_size
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe storage"""
        # Remove path traversal attempts
        filename = os.path.basename(filename)
        
        # Remove dangerous characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Limit length
        if len(filename) > 255:
            name, ext = os.path.splitext(filename)
            filename = name[:250] + ext
        
        # Ensure filename is not empty
        if not filename or filename == '.':
            filename = 'unnamed_file'
        
        return filename
    
    def rate_limit_check(self, client_ip: str, endpoint: str) -> bool:
        """Basic rate limiting check (implement with Redis in production)"""
        # This is a placeholder - implement proper rate limiting with Redis
        # For now, just return True (no rate limiting)
        return True

# Global validator instance
input_validator = InputValidator()
