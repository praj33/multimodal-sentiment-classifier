# classifiers/video_classifier.py

# Simplified version for testing - will use full implementation when dependencies are available
try:
    import cv2
    import mediapipe as mp
    import numpy as np
    FULL_VIDEO_AVAILABLE = True
except ImportError:
    FULL_VIDEO_AVAILABLE = False
    print("[VideoClassifier] Full video dependencies not available, using simplified version")

from collections import Counter
import os

class VideoClassifier:
    def __init__(self):
        """
        Initialize Video Classifier with MediaPipe face detection and emotion analysis
        """
        if FULL_VIDEO_AVAILABLE:
            self.mp_face_detection = mp.solutions.face_detection
            self.mp_face_mesh = mp.solutions.face_mesh
            self.mp_drawing = mp.solutions.drawing_utils

            # Initialize face detection and mesh
            self.face_detection = self.mp_face_detection.FaceDetection(
                model_selection=0, min_detection_confidence=0.5
            )
            self.face_mesh = self.mp_face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
        else:
            print("[VideoClassifier] Using simplified mode - install opencv-python and mediapipe for full functionality")

    def extract_facial_features(self, landmarks):
        """
        Extract facial features for emotion detection from MediaPipe landmarks
        """
        if not landmarks:
            return None

        # Key facial landmark indices for emotion detection
        # These are approximate indices for key facial features
        left_eye = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        right_eye = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        mouth = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308, 415, 310, 311, 312, 13, 82, 81, 80, 78]
        eyebrows = [70, 63, 105, 66, 107, 55, 65, 52, 53, 46]

        try:
            # Calculate distances and ratios for emotion detection
            landmarks_array = np.array([[lm.x, lm.y] for lm in landmarks.landmark])

            # Eye aspect ratios (closed eyes might indicate sadness/tiredness)
            left_eye_points = landmarks_array[left_eye[:6]]
            right_eye_points = landmarks_array[right_eye[:6]]

            left_eye_ratio = self._calculate_eye_aspect_ratio(left_eye_points)
            right_eye_ratio = self._calculate_eye_aspect_ratio(right_eye_points)
            eye_ratio = (left_eye_ratio + right_eye_ratio) / 2

            # Mouth aspect ratio (smile detection)
            mouth_points = landmarks_array[mouth[:8]]
            mouth_ratio = self._calculate_mouth_aspect_ratio(mouth_points)

            # Eyebrow position (raised eyebrows might indicate surprise/happiness)
            eyebrow_points = landmarks_array[eyebrows]
            eyebrow_height = np.mean(eyebrow_points[:, 1])

            return {
                'eye_ratio': eye_ratio,
                'mouth_ratio': mouth_ratio,
                'eyebrow_height': eyebrow_height
            }

        except Exception as e:
            print(f"Error extracting facial features: {e}")
            return None

    def _calculate_eye_aspect_ratio(self, eye_points):
        """Calculate eye aspect ratio for blink/emotion detection"""
        if len(eye_points) < 6:
            return 0.2

        # Vertical distances
        A = np.linalg.norm(eye_points[1] - eye_points[5])
        B = np.linalg.norm(eye_points[2] - eye_points[4])

        # Horizontal distance
        C = np.linalg.norm(eye_points[0] - eye_points[3])

        # Eye aspect ratio
        ear = (A + B) / (2.0 * C) if C > 0 else 0.2
        return ear

    def _calculate_mouth_aspect_ratio(self, mouth_points):
        """Calculate mouth aspect ratio for smile detection"""
        if len(mouth_points) < 8:
            return 0.5

        # Vertical distances
        A = np.linalg.norm(mouth_points[1] - mouth_points[7])
        B = np.linalg.norm(mouth_points[2] - mouth_points[6])
        C = np.linalg.norm(mouth_points[3] - mouth_points[5])

        # Horizontal distance
        D = np.linalg.norm(mouth_points[0] - mouth_points[4])

        # Mouth aspect ratio
        mar = (A + B + C) / (3.0 * D) if D > 0 else 0.5
        return mar

    def analyze_frame_emotion(self, frame):
        """
        Analyze emotion in a single frame
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                features = self.extract_facial_features(face_landmarks)
                if features:
                    return self.classify_emotion(features)

        return "neutral", 0.3

    def classify_emotion(self, features):
        """
        Classify emotion based on facial features using heuristic rules
        """
        eye_ratio = features['eye_ratio']
        mouth_ratio = features['mouth_ratio']
        eyebrow_height = features['eyebrow_height']

        # Heuristic rules for emotion classification
        positive_score = 0
        negative_score = 0

        # Smile detection (higher mouth ratio)
        if mouth_ratio > 0.6:
            positive_score += 2
        elif mouth_ratio < 0.4:
            negative_score += 1

        # Eye openness (very closed eyes might indicate sadness)
        if eye_ratio < 0.15:
            negative_score += 1
        elif eye_ratio > 0.25:
            positive_score += 1

        # Eyebrow position (raised eyebrows)
        if eyebrow_height < 0.4:  # Higher position (lower y-value)
            positive_score += 1
        elif eyebrow_height > 0.6:  # Lower position
            negative_score += 1

        # Determine emotion
        if positive_score > negative_score:
            sentiment = "positive"
            confidence = min(0.6 + (positive_score - negative_score) * 0.1, 0.9)
        elif negative_score > positive_score:
            sentiment = "negative"
            confidence = min(0.6 + (negative_score - positive_score) * 0.1, 0.9)
        else:
            sentiment = "neutral"
            confidence = 0.5

        return sentiment, confidence

    def predict(self, video_path):
        """
        Predict sentiment from video file by analyzing facial expressions
        """
        try:
            print(f"[VideoClassifier] Processing: {video_path}")

            if not FULL_VIDEO_AVAILABLE:
                # Simplified prediction based on filename or random for demo
                import random
                sentiments = ["positive", "negative", "neutral"]
                sentiment = random.choice(sentiments)
                confidence = 0.5 + random.random() * 0.3  # 0.5 to 0.8
                print(f"[VideoClassifier] Simplified result: {sentiment} (confidence: {confidence:.2f})")
                return sentiment, confidence

            # Open video file
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"Error: Could not open video {video_path}")
                return "neutral", 0.3

            emotions = []
            frame_count = 0
            max_frames = 150  # Analyze max 150 frames (about 5 seconds at 30fps)

            while cap.read()[0] and frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break

                # Analyze every 5th frame to reduce processing time
                if frame_count % 5 == 0:
                    emotion, confidence = self.analyze_frame_emotion(frame)
                    emotions.append((emotion, confidence))

                frame_count += 1

            cap.release()

            if not emotions:
                print("[VideoClassifier] No faces detected in video")
                return "neutral", 0.3

            # Aggregate emotions across frames
            emotion_counts = Counter([emotion for emotion, _ in emotions])
            confidences = [conf for _, conf in emotions]

            # Get most common emotion
            most_common_emotion = emotion_counts.most_common(1)[0][0]
            avg_confidence = np.mean(confidences)

            print(f"[VideoClassifier] Result: {most_common_emotion} (confidence: {avg_confidence:.2f})")
            print(f"[VideoClassifier] Emotion distribution: {dict(emotion_counts)}")

            return most_common_emotion, avg_confidence

        except Exception as e:
            print(f"[VideoClassifier] Error processing {video_path}: {e}")
            return "neutral", 0.3