#!/usr/bin/env python3
"""
Generate Test Audio and Video Files for Multimodal Sentiment Classifier
Creates sample files with different characteristics to test audio and video classifiers
"""

import os
import numpy as np
import wave
import struct
from pathlib import Path

def create_test_directory():
    """Create test files directory"""
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)
    
    audio_dir = test_dir / "audio"
    video_dir = test_dir / "video"
    audio_dir.mkdir(exist_ok=True)
    video_dir.mkdir(exist_ok=True)
    
    return test_dir, audio_dir, video_dir

def generate_sine_wave_audio(filename, frequency=440, duration=3, sample_rate=44100, amplitude=0.5):
    """Generate a sine wave audio file"""
    frames = int(duration * sample_rate)
    
    # Generate sine wave
    wave_data = []
    for i in range(frames):
        value = int(amplitude * 32767 * np.sin(2 * np.pi * frequency * i / sample_rate))
        wave_data.append(struct.pack('<h', value))
    
    # Write WAV file
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(wave_data))

def generate_noise_audio(filename, duration=3, sample_rate=44100, amplitude=0.3):
    """Generate white noise audio file"""
    frames = int(duration * sample_rate)
    
    # Generate white noise
    wave_data = []
    for i in range(frames):
        value = int(amplitude * 32767 * (np.random.random() - 0.5) * 2)
        wave_data.append(struct.pack('<h', value))
    
    # Write WAV file
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(wave_data))

def generate_chirp_audio(filename, start_freq=200, end_freq=2000, duration=3, sample_rate=44100):
    """Generate a frequency sweep (chirp) audio file"""
    frames = int(duration * sample_rate)
    
    wave_data = []
    for i in range(frames):
        # Linear frequency sweep
        t = i / sample_rate
        freq = start_freq + (end_freq - start_freq) * t / duration
        value = int(0.5 * 32767 * np.sin(2 * np.pi * freq * t))
        wave_data.append(struct.pack('<h', value))
    
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(wave_data))

def create_simple_video_file(filename, width=320, height=240, fps=30, duration=3):
    """Create a simple test video file using OpenCV if available"""
    try:
        import cv2
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
        
        total_frames = fps * duration
        
        for frame_num in range(total_frames):
            # Create a frame with changing colors
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Create different patterns for different sentiment "moods"
            if "positive" in filename.lower():
                # Bright, warm colors
                frame[:, :, 0] = int(255 * (0.5 + 0.5 * np.sin(frame_num * 0.1)))  # Blue
                frame[:, :, 1] = int(255 * (0.7 + 0.3 * np.sin(frame_num * 0.15)))  # Green
                frame[:, :, 2] = int(255 * (0.8 + 0.2 * np.sin(frame_num * 0.2)))   # Red
            elif "negative" in filename.lower():
                # Darker, cooler colors
                frame[:, :, 0] = int(128 * (0.3 + 0.2 * np.sin(frame_num * 0.05)))  # Blue
                frame[:, :, 1] = int(100 * (0.2 + 0.1 * np.sin(frame_num * 0.08)))  # Green
                frame[:, :, 2] = int(80 * (0.1 + 0.1 * np.sin(frame_num * 0.03)))   # Red
            else:
                # Neutral, balanced colors
                frame[:, :, 0] = int(150 * (0.5 + 0.3 * np.sin(frame_num * 0.1)))
                frame[:, :, 1] = int(150 * (0.5 + 0.3 * np.sin(frame_num * 0.1)))
                frame[:, :, 2] = int(150 * (0.5 + 0.3 * np.sin(frame_num * 0.1)))
            
            # Add some geometric patterns
            center_x, center_y = width // 2, height // 2
            radius = int(50 + 30 * np.sin(frame_num * 0.2))
            cv2.circle(frame, (center_x, center_y), radius, (255, 255, 255), 2)
            
            out.write(frame)
        
        out.release()
        print(f"Created video: {filename}")
        
    except ImportError:
        print("OpenCV not available. Creating placeholder video file.")
        # Create a minimal MP4 file header (won't be playable but will test file handling)
        with open(filename, 'wb') as f:
            # Minimal MP4 header
            f.write(b'\x00\x00\x00\x20ftypmp42\x00\x00\x00\x00mp42isom')
            f.write(b'\x00' * 1000)  # Padding to make it a reasonable size

def main():
    """Generate all test files"""
    print("🎵 Generating test audio and video files...")
    
    test_dir, audio_dir, video_dir = create_test_directory()
    
    # Generate audio test files
    print("\n📻 Creating audio test files...")
    
    # Positive sentiment audio (higher frequency, more harmonious)
    generate_sine_wave_audio(
        str(audio_dir / "positive_happy_tone.wav"),
        frequency=880,  # Higher pitch
        duration=4,
        amplitude=0.6
    )
    
    # Negative sentiment audio (lower frequency, more dissonant)
    generate_sine_wave_audio(
        str(audio_dir / "negative_sad_tone.wav"),
        frequency=220,  # Lower pitch
        duration=4,
        amplitude=0.4
    )
    
    # Neutral sentiment audio (mid-range frequency)
    generate_sine_wave_audio(
        str(audio_dir / "neutral_calm_tone.wav"),
        frequency=440,  # Standard A note
        duration=4,
        amplitude=0.5
    )
    
    # Energetic/excited audio (frequency sweep)
    generate_chirp_audio(
        str(audio_dir / "positive_excited_sweep.wav"),
        start_freq=400,
        end_freq=1200,
        duration=3
    )
    
    # Chaotic/stressed audio (noise)
    generate_noise_audio(
        str(audio_dir / "negative_stressed_noise.wav"),
        duration=3,
        amplitude=0.3
    )
    
    # Mixed emotions (complex waveform)
    generate_chirp_audio(
        str(audio_dir / "neutral_mixed_emotions.wav"),
        start_freq=800,
        end_freq=200,
        duration=4
    )
    
    print(f"✅ Created {len(list(audio_dir.glob('*.wav')))} audio files")
    
    # Generate video test files
    print("\n🎬 Creating video test files...")
    
    video_files = [
        "positive_bright_video.mp4",
        "negative_dark_video.mp4", 
        "neutral_balanced_video.mp4",
        "positive_energetic_video.mp4",
        "negative_gloomy_video.mp4"
    ]
    
    for video_file in video_files:
        create_simple_video_file(str(video_dir / video_file))
    
    print(f"✅ Created {len(video_files)} video files")
    
    # Create a test script
    test_script_content = '''#!/usr/bin/env python3
"""
Test Script for Audio and Video Classifiers
Run this to test your classifiers with the generated files
"""

import requests
import os
from pathlib import Path

def test_audio_files():
    """Test all audio files"""
    audio_dir = Path("test_files/audio")
    
    print("🎵 Testing Audio Classifier...")
    for audio_file in audio_dir.glob("*.wav"):
        print(f"\\nTesting: {audio_file.name}")
        
        try:
            with open(audio_file, 'rb') as f:
                files = {'file': (audio_file.name, f, 'audio/wav')}
                response = requests.post('http://localhost:8000/predict/audio', files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"  Sentiment: {result.get('sentiment', 'unknown')}")
                    print(f"  Confidence: {result.get('confidence', 0):.3f}")
                else:
                    print(f"  Error: {response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")

def test_video_files():
    """Test all video files"""
    video_dir = Path("test_files/video")
    
    print("\\n🎬 Testing Video Classifier...")
    for video_file in video_dir.glob("*.mp4"):
        print(f"\\nTesting: {video_file.name}")
        
        try:
            with open(video_file, 'rb') as f:
                files = {'file': (video_file.name, f, 'video/mp4')}
                response = requests.post('http://localhost:8000/predict/video', files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"  Sentiment: {result.get('sentiment', 'unknown')}")
                    print(f"  Confidence: {result.get('confidence', 0):.3f}")
                else:
                    print(f"  Error: {response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    print("🧪 Testing Multimodal Sentiment Classifiers")
    print("Make sure your server is running on http://localhost:8000")
    
    test_audio_files()
    test_video_files()
    
    print("\\n✅ Testing complete!")
'''
    
    with open(test_dir / "test_classifiers.py", 'w') as f:
        f.write(test_script_content)
    
    # Create README for test files
    readme_content = f'''# Test Files for Multimodal Sentiment Classifier

This directory contains generated test files for testing your audio and video classifiers.

## 📁 Directory Structure
```
test_files/
├── audio/                          # Audio test files (.wav)
│   ├── positive_happy_tone.wav     # High frequency, bright tone
│   ├── positive_excited_sweep.wav  # Frequency sweep (energetic)
│   ├── negative_sad_tone.wav       # Low frequency, subdued tone
│   ├── negative_stressed_noise.wav # White noise (chaotic)
│   ├── neutral_calm_tone.wav       # Mid-range frequency
│   └── neutral_mixed_emotions.wav  # Complex waveform
├── video/                          # Video test files (.mp4)
│   ├── positive_bright_video.mp4   # Bright, warm colors
│   ├── positive_energetic_video.mp4# Dynamic, vibrant patterns
│   ├── negative_dark_video.mp4     # Dark, cool colors
│   ├── negative_gloomy_video.mp4   # Subdued, low contrast
│   └── neutral_balanced_video.mp4  # Balanced, neutral tones
└── test_classifiers.py             # Test script
```

## 🧪 How to Test

1. **Start your server:**
   ```bash
   python start_server.py
   ```

2. **Run the test script:**
   ```bash
   python test_files/test_classifiers.py
   ```

3. **Manual testing via API:**
   ```bash
   # Test audio file
   curl -X POST "http://localhost:8000/predict/audio" \\
        -F "file=@test_files/audio/positive_happy_tone.wav"
   
   # Test video file
   curl -X POST "http://localhost:8000/predict/video" \\
        -F "file=@test_files/video/positive_bright_video.mp4"
   ```

4. **Test via Web Dashboard:**
   - Open http://localhost:8000/dashboard
   - Upload the test files using the interface

## 📊 Expected Results

The classifiers should detect different sentiment patterns based on:

### Audio Features:
- **Positive**: Higher frequencies, harmonious tones
- **Negative**: Lower frequencies, noise, dissonance  
- **Neutral**: Mid-range frequencies, balanced patterns

### Video Features:
- **Positive**: Bright colors, dynamic movement
- **Negative**: Dark colors, low contrast
- **Neutral**: Balanced colors, steady patterns

## 🔧 Customization

You can modify `generate_test_files.py` to create additional test files with different characteristics.
'''
    
    with open(test_dir / "README.md", 'w') as f:
        f.write(readme_content)
    
    print(f"\n🎉 Test file generation complete!")
    print(f"📁 Files created in: {test_dir.absolute()}")
    print(f"📊 Audio files: {len(list(audio_dir.glob('*.wav')))}")
    print(f"🎬 Video files: {len(list(video_dir.glob('*.mp4')))}")
    print(f"\n🧪 To test your classifiers:")
    print(f"   1. Start your server: python start_server.py")
    print(f"   2. Run tests: python {test_dir}/test_classifiers.py")
    print(f"   3. Or use the web dashboard: http://localhost:8000/dashboard")

if __name__ == "__main__":
    main()
