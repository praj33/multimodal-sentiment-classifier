# input_validation.py - Day 2 Requirement: Strict input validation and sanitization

import re
import hashlib
import os
from typing import Optional, Dict, Any, List
from fastapi import HTTPException, UploadFile

# Optional imports with fallbacks
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False

try:
    import bleach
    BLEACH_AVAILABLE = True
except ImportError:
    BLEACH_AVAILABLE = False

class InputValidator:
    """Enhanced input validation and sanitization"""
    
    def __init__(self):
        # File size limits (in bytes) - Day 2 STRICT requirement: 50MB max
        self.MAX_FILE_SIZES = {
            'audio': 50 * 1024 * 1024,  # 50MB EXACTLY (Day 2 requirement)
            'video': 50 * 1024 * 1024,  # 50MB EXACTLY (Day 2 requirement)
            'image': 10 * 1024 * 1024,   # 10MB
        }

        # Load from environment if available
        self.MAX_FILE_SIZES['audio'] = int(os.getenv('MAX_FILE_SIZE_AUDIO', 50 * 1024 * 1024))
        self.MAX_FILE_SIZES['video'] = int(os.getenv('MAX_FILE_SIZE_VIDEO', 50 * 1024 * 1024))
        
        # Allowed file types (Day 2 STRICT requirements: audio: wav/mp3/ogg, video: mp4/mov)
        self.ALLOWED_MIME_TYPES = {
            'audio': [
                'audio/wav', 'audio/wave', 'audio/x-wav',  # WAV (Day 2 required)
                'audio/mpeg', 'audio/mp3',                 # MP3 (Day 2 required)
                'audio/ogg', 'audio/ogg; codecs=vorbis',   # OGG (Day 2 required)
                'audio/mp4', 'audio/m4a'                   # M4A (additional)
            ],
            'video': [
                'video/mp4', 'video/mpeg',                 # MP4 (Day 2 required)
                'video/quicktime',                         # MOV (Day 2 required)
                'video/x-msvideo', 'video/avi'             # AVI (additional)
            ],
            'image': [
                'image/jpeg', 'image/jpg', 'image/png',
                'image/gif', 'image/bmp', 'image/webp'
            ]
        }

        # Allowed file extensions (Day 2 STRICT requirements)
        self.ALLOWED_EXTENSIONS = {
            'audio': ['.wav', '.mp3', '.ogg', '.m4a'],     # Day 2: wav/mp3/ogg REQUIRED + m4a
            'video': ['.mp4', '.mov', '.avi'],             # Day 2: mp4/mov REQUIRED + avi
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        }

        # Text validation limits (Day 2 requirement: sanitize text length)
        self.MAX_TEXT_LENGTH = int(os.getenv('MAX_TEXT_LENGTH', 10000))
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
        """Validate and sanitize text input with Day 2 enhanced security"""
        if not isinstance(text, str):
            raise HTTPException(
                status_code=400,
                detail="Text input must be a string. Received: " + str(type(text).__name__)
            )

        # Check length (Day 2: enhanced feedback)
        if len(text) < self.MIN_TEXT_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Text input too short. Minimum length: {self.MIN_TEXT_LENGTH} character(s)"
            )

        if len(text) > self.MAX_TEXT_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Text input too long ({len(text)} characters). Maximum allowed: {self.MAX_TEXT_LENGTH} characters"
            )

        # Check for malicious patterns (Day 2: enhanced security)
        for pattern in self.MALICIOUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                raise HTTPException(
                    status_code=400,
                    detail="Text contains potentially malicious content. Please remove any script tags or executable code."
                )

        # Sanitize HTML/script content
        if BLEACH_AVAILABLE:
            sanitized_text = bleach.clean(text, tags=[], attributes={}, strip=True)
        else:
            # Basic HTML tag removal if bleach is not available
            sanitized_text = re.sub(r'<[^>]+>', '', text)

        # Remove excessive whitespace and normalize
        sanitized_text = re.sub(r'\s+', ' ', sanitized_text).strip()

        # Additional Day 2 sanitization: remove control characters
        sanitized_text = ''.join(char for char in sanitized_text if ord(char) >= 32 or char in '\t\n\r')

        if not sanitized_text:
            raise HTTPException(
                status_code=400,
                detail="Text input is empty after sanitization. Please provide meaningful text content."
            )

        return sanitized_text
    
    def validate_file_upload(self, file: UploadFile, file_type: str) -> Dict[str, Any]:
        """Validate uploaded file with enhanced Day 2 requirements"""
        if not file:
            raise HTTPException(
                status_code=400,
                detail="No file provided. Please upload a valid file."
            )

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No filename provided. Please ensure the file has a valid name."
            )

        # Validate file type category
        if file_type not in self.ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file category: {file_type}. Supported categories: {', '.join(self.ALLOWED_MIME_TYPES.keys())}"
            )

        # Check file extension (Day 2: strict validation)
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in self.ALLOWED_EXTENSIONS[file_type]:
            allowed_exts = ', '.join(self.ALLOWED_EXTENSIONS[file_type])
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file extension '{file_ext}' for {file_type}. Allowed extensions: {allowed_exts}"
            )
        
        # Read file content for validation
        file_content = file.file.read()
        file.file.seek(0)  # Reset file pointer

        # Check file size (Day 2: enhanced validation with detailed feedback)
        file_size = len(file_content)
        if file_size == 0:
            raise HTTPException(
                status_code=400,
                detail="File is empty. Please upload a valid file with content."
            )

        max_size_bytes = self.MAX_FILE_SIZES[file_type]
        if file_size > max_size_bytes:
            max_size_mb = max_size_bytes / (1024 * 1024)
            current_size_mb = file_size / (1024 * 1024)
            raise HTTPException(
                status_code=413,  # Payload Too Large
                detail=f"File too large ({current_size_mb:.1f}MB). Maximum allowed size for {file_type}: {max_size_mb:.0f}MB"
            )
        
        # Day 2: Enhanced MIME type validation with magic number verification
        detected_mime = file.content_type  # Default to browser-provided MIME type
        magic_validation_passed = False

        if MAGIC_AVAILABLE:
            try:
                detected_mime = magic.from_buffer(file_content, mime=True)
                if detected_mime not in self.ALLOWED_MIME_TYPES[file_type]:
                    # Try to get more specific error message
                    allowed_types = ', '.join(self.ALLOWED_MIME_TYPES[file_type])
                    raise HTTPException(
                        status_code=400,
                        detail=f"File content validation failed. Detected MIME type: '{detected_mime}' is not allowed for {file_type}. Allowed types: {allowed_types}"
                    )
                magic_validation_passed = True
            except HTTPException:
                raise  # Re-raise HTTP exceptions
            except Exception as e:
                # Fallback to browser-provided MIME type with warning
                detected_mime = file.content_type or "application/octet-stream"
                # Continue with basic validation below

        # Enhanced magic number validation (Day 2 requirement)
        if not magic_validation_passed:
            magic_number_valid = self._validate_magic_numbers(file_content, file_type, file_ext)
            if not magic_number_valid:
                raise HTTPException(
                    status_code=400,
                    detail=f"File header validation failed. The file does not appear to be a valid {file_type} file."
                )

        # Basic MIME type validation (fallback)
        if not magic_validation_passed and file.content_type:
            if file.content_type not in self.ALLOWED_MIME_TYPES[file_type]:
                allowed_types = ', '.join(self.ALLOWED_MIME_TYPES[file_type])
                raise HTTPException(
                    status_code=400,
                    detail=f"File type '{file.content_type}' not allowed for {file_type}. Allowed types: {allowed_types}"
                )
        
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
    
    def _validate_magic_numbers(self, content: bytes, file_type: str, file_ext: str) -> bool:
        """Validate file magic numbers (Day 2 requirement)"""
        if len(content) < 12:  # Need at least 12 bytes for most magic numbers
            return False

        # Define magic number signatures for supported file types
        magic_signatures = {
            'audio': {
                '.wav': [
                    b'RIFF',  # WAV files start with RIFF
                    b'WAVE'   # Should contain WAVE somewhere in header
                ],
                '.mp3': [
                    b'\xff\xfb',  # MP3 frame header
                    b'\xff\xfa',  # MP3 frame header
                    b'\xff\xf3',  # MP3 frame header
                    b'\xff\xf2',  # MP3 frame header
                    b'ID3'        # ID3 tag
                ],
                '.ogg': [
                    b'OggS'       # OGG container
                ],
                '.m4a': [
                    b'ftyp',      # MP4/M4A container
                    b'ftypM4A'    # M4A specific
                ]
            },
            'video': {
                '.mp4': [
                    b'ftyp',      # MP4 container
                    b'ftypmp4',   # MP4 specific
                    b'ftypisom'   # ISO MP4
                ],
                '.mov': [
                    b'ftyp',      # QuickTime container
                    b'ftypqt',    # QuickTime specific
                    b'moov'       # QuickTime movie atom
                ],
                '.avi': [
                    b'RIFF',      # AVI files start with RIFF
                    b'AVI '       # Should contain AVI in header
                ]
            }
        }

        if file_type not in magic_signatures or file_ext not in magic_signatures[file_type]:
            return True  # No specific validation for this type

        # Check magic numbers
        header = content[:64]  # Check first 64 bytes
        required_signatures = magic_signatures[file_type][file_ext]

        for signature in required_signatures:
            if signature in header:
                return True

        return False

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
                if BLEACH_AVAILABLE:
                    clean_value = bleach.clean(value, tags=[], attributes={}, strip=True)
                else:
                    clean_value = re.sub(r'<[^>]+>', '', value)  # Basic HTML removal
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
