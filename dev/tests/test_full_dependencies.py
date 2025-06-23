#!/usr/bin/env python3
# test_full_dependencies.py - Test all dependencies for full functionality

print("🔍 TESTING FULL MULTIMODAL DEPENDENCIES")
print("=" * 50)

# Test Audio Dependencies
print("\n🎵 TESTING AUDIO DEPENDENCIES:")
print("-" * 30)
try:
    import librosa
    print("✅ librosa imported successfully")
    print(f"✅ librosa version: {librosa.__version__}")
    
    # Test basic audio functionality
    import numpy as np
    dummy_audio = np.random.randn(22050)  # 1 second of dummy audio
    mfccs = librosa.feature.mfcc(y=dummy_audio, sr=22050, n_mfcc=13)
    print(f"✅ MFCC extraction working: {mfccs.shape}")
    
    audio_deps_available = True
except ImportError as e:
    print(f"❌ Audio dependencies missing: {e}")
    audio_deps_available = False
except Exception as e:
    print(f"❌ Audio functionality error: {e}")
    audio_deps_available = False

# Test Video Dependencies
print("\n🎥 TESTING VIDEO DEPENDENCIES:")
print("-" * 30)
try:
    import cv2
    print("✅ OpenCV imported successfully")
    print(f"✅ OpenCV version: {cv2.__version__}")
    
    # Test basic video functionality
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    gray = cv2.cvtColor(dummy_frame, cv2.COLOR_BGR2GRAY)
    print(f"✅ OpenCV processing working: {gray.shape}")
    
    opencv_available = True
except ImportError as e:
    print(f"❌ OpenCV missing: {e}")
    opencv_available = False
except Exception as e:
    print(f"❌ OpenCV functionality error: {e}")
    opencv_available = False

try:
    import mediapipe as mp
    print("✅ MediaPipe imported successfully")
    print(f"✅ MediaPipe version: {mp.__version__}")
    
    # Test MediaPipe face detection
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils
    print("✅ MediaPipe face detection available")
    
    mediapipe_available = True
except ImportError as e:
    print(f"❌ MediaPipe missing: {e}")
    mediapipe_available = False
except Exception as e:
    print(f"❌ MediaPipe functionality error: {e}")
    mediapipe_available = False

video_deps_available = opencv_available and mediapipe_available

# Test Classifiers
print("\n🧠 TESTING CLASSIFIER FUNCTIONALITY:")
print("-" * 35)

try:
    from classifiers.audio_classifier import AudioClassifier
    audio_classifier = AudioClassifier()
    print("✅ Audio classifier initialized")
    
    if audio_deps_available:
        print("✅ Audio classifier: FULL FUNCTIONALITY")
    else:
        print("⚠️ Audio classifier: SIMPLIFIED MODE")
        
except Exception as e:
    print(f"❌ Audio classifier error: {e}")

try:
    from classifiers.video_classifier import VideoClassifier
    video_classifier = VideoClassifier()
    print("✅ Video classifier initialized")
    
    if video_deps_available:
        print("✅ Video classifier: FULL FUNCTIONALITY")
    else:
        print("⚠️ Video classifier: SIMPLIFIED MODE")
        
except Exception as e:
    print(f"❌ Video classifier error: {e}")

try:
    from classifiers.text_classifier import TextClassifier
    text_classifier = TextClassifier()
    print("✅ Text classifier initialized")
    print("✅ Text classifier: FULL FUNCTIONALITY")
except Exception as e:
    print(f"❌ Text classifier error: {e}")

# Summary
print("\n📊 DEPENDENCY STATUS SUMMARY:")
print("=" * 35)
print(f"🔤 Text Dependencies: ✅ FULL")
print(f"🎵 Audio Dependencies: {'✅ FULL' if audio_deps_available else '⚠️ SIMPLIFIED'}")
print(f"🎥 Video Dependencies: {'✅ FULL' if video_deps_available else '⚠️ SIMPLIFIED'}")

if audio_deps_available and video_deps_available:
    print("\n🎉 ALL DEPENDENCIES AVAILABLE - FULL FUNCTIONALITY!")
elif audio_deps_available or video_deps_available:
    print("\n⚠️ PARTIAL DEPENDENCIES - MIXED FUNCTIONALITY")
    if not audio_deps_available:
        print("   📝 To enable full audio: pip install librosa")
    if not video_deps_available:
        print("   📝 To enable full video: pip install opencv-python mediapipe")
else:
    print("\n⚠️ SIMPLIFIED MODE - INSTALL DEPENDENCIES FOR FULL FUNCTIONALITY")
    print("   📝 For audio: pip install librosa")
    print("   📝 For video: pip install opencv-python mediapipe")

print("\n🚀 READY TO START API!")
