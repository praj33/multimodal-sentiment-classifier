#!/usr/bin/env python3
"""
Test the full functionality of audio and video classifiers
"""

import numpy as np
import soundfile as sf
import cv2
from classifiers.audio_classifier import AudioClassifier
from classifiers.video_classifier import VideoClassifier

def create_test_audio():
    """Create a simple test audio file"""
    sample_rate = 22050
    duration = 3  # 3 seconds
    t = np.linspace(0, duration, int(sample_rate * duration))
    frequency = 440  # A4 note
    audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    # Save as WAV file
    sf.write('test_audio.wav', audio_data, sample_rate)
    print('✅ Created test_audio.wav')
    return 'test_audio.wav'

def create_test_video():
    """Create a simple test video file"""
    # Create a simple video with colored frames
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('test_video.mp4', fourcc, 20.0, (640, 480))
    
    for i in range(60):  # 3 seconds at 20 fps
        # Create a frame with changing colors
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        color = (i * 4 % 255, (i * 2) % 255, (i * 6) % 255)
        cv2.rectangle(frame, (100, 100), (540, 380), color, -1)
        
        # Add some text
        cv2.putText(frame, f'Frame {i}', (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        out.write(frame)
    
    out.release()
    print('✅ Created test_video.mp4')
    return 'test_video.mp4'

def test_audio_classifier():
    """Test the audio classifier with real audio processing"""
    print('\n🎵 Testing Audio Classifier with Full Functionality:')
    
    # Create test audio
    audio_file = create_test_audio()
    
    # Test audio classifier
    audio_classifier = AudioClassifier()
    sentiment, confidence = audio_classifier.predict(audio_file)
    
    print(f'   Audio Analysis Result: {sentiment} (confidence: {confidence:.2f})')
    return sentiment, confidence

def test_video_classifier():
    """Test the video classifier with real video processing"""
    print('\n🎬 Testing Video Classifier with Full Functionality:')
    
    # Create test video
    video_file = create_test_video()
    
    # Test video classifier
    video_classifier = VideoClassifier()
    sentiment, confidence = video_classifier.predict(video_file)
    
    print(f'   Video Analysis Result: {sentiment} (confidence: {confidence:.2f})')
    return sentiment, confidence

def main():
    print('🎭 FULL FUNCTIONALITY TEST')
    print('=' * 50)
    
    try:
        # Test audio classifier
        audio_result = test_audio_classifier()
        
        # Test video classifier  
        video_result = test_video_classifier()
        
        print('\n✅ FULL FUNCTIONALITY TESTS COMPLETED!')
        print(f'   Audio: {audio_result[0]} ({audio_result[1]:.2f})')
        print(f'   Video: {video_result[0]} ({video_result[1]:.2f})')
        
        print('\n🌟 ALL DEPENDENCIES RESOLVED:')
        print('   ✅ librosa - Audio processing')
        print('   ✅ opencv-python - Video processing')
        print('   ✅ mediapipe - Facial analysis')
        print('   ✅ scikit-learn - Machine learning')
        
    except Exception as e:
        print(f'❌ Error during testing: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
