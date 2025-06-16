# sdk/python/sentiment_sdk.py

import requests
import os
from typing import Dict, Any, Union

class SentimentAnalyzer:
    """
    Python SDK for Multimodal Sentiment Analysis API

    This class provides a convenient interface to interact with the sentiment analysis service.
    """

    def __init__(self, api_url: str = "http://127.0.0.1:8000", timeout: int = 30):
        """
        Initialize the SentimentAnalyzer

        Args:
            api_url: Base URL of the sentiment analysis API
            timeout: Request timeout in seconds
        """
        self.api_url = api_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text input

        Args:
            text: Text to analyze

        Returns:
            dict: Analysis result with sentiment, confidence, and metadata
        """
        response = self.session.post(
            f"{self.api_url}/predict/text",
            json={"text": text},
            timeout=self.timeout
        )

        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")

        return response.json()

    def analyze_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        Analyze sentiment of audio file

        Args:
            audio_path: Path to audio file

        Returns:
            dict: Analysis result with sentiment, confidence, and metadata
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        with open(audio_path, "rb") as f:
            response = self.session.post(
                f"{self.api_url}/predict/audio",
                files={"file": (os.path.basename(audio_path), f)},
                timeout=self.timeout
            )

        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")

        return response.json()

    def analyze_video(self, video_path: str) -> Dict[str, Any]:
        """
        Analyze sentiment of video file

        Args:
            video_path: Path to video file

        Returns:
            dict: Analysis result with sentiment, confidence, and metadata
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        with open(video_path, "rb") as f:
            response = self.session.post(
                f"{self.api_url}/predict/video",
                files={"file": (os.path.basename(video_path), f)},
                timeout=self.timeout
            )

        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")

        return response.json()

    def analyze_multimodal(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze sentiment using multiple modalities

        Args:
            file_path: Path to media file (audio/video)

        Returns:
            dict: Analysis result with fused sentiment and individual modality results
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "rb") as f:
            response = self.session.post(
                f"{self.api_url}/predict/multimodal",
                files={"file": (os.path.basename(file_path), f)},
                timeout=self.timeout
            )

        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")

        return response.json()

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get prediction statistics from the API

        Returns:
            dict: Statistics including sentiment distribution, processing times, etc.
        """
        response = self.session.get(
            f"{self.api_url}/analytics/stats",
            timeout=self.timeout
        )

        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")

        return response.json()

    def get_recent_predictions(self, limit: int = 50, mode: str = None, sentiment: str = None) -> list:
        """
        Get recent predictions with optional filtering

        Args:
            limit: Maximum number of predictions to return
            mode: Filter by prediction mode (text, audio, video, multimodal)
            sentiment: Filter by sentiment (positive, negative, neutral)

        Returns:
            list: List of recent predictions
        """
        params = {"limit": limit}
        if mode:
            params["mode"] = mode
        if sentiment:
            params["sentiment"] = sentiment

        response = self.session.get(
            f"{self.api_url}/analytics/predictions",
            params=params,
            timeout=self.timeout
        )

        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")

        return response.json()

    def start_session(self, user_id: str = None) -> str:
        """
        Start a new logging session

        Args:
            user_id: Optional user identifier

        Returns:
            str: Session ID
        """
        params = {}
        if user_id:
            params["user_id"] = user_id

        response = self.session.post(
            f"{self.api_url}/analytics/session/start",
            params=params,
            timeout=self.timeout
        )

        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")

        return response.json()["session_id"]

    def end_session(self, session_id: str):
        """
        End a logging session

        Args:
            session_id: Session ID to end
        """
        response = self.session.post(
            f"{self.api_url}/analytics/session/{session_id}/end",
            timeout=self.timeout
        )

        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")

    def health_check(self) -> bool:
        """
        Check if the API is healthy and responsive

        Returns:
            bool: True if API is healthy, False otherwise
        """
        try:
            response = self.session.get(f"{self.api_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False

# Convenience function for backward compatibility
def analyze_sentiment(input_data: Union[str, os.PathLike], mode: str = "text", api_url: str = "http://127.0.0.1:8000") -> Dict[str, Any]:
    """
    Convenience function to analyze sentiment

    Args:
        input_data: Text string or file path
        mode: Analysis mode (text, audio, video, multimodal)
        api_url: API base URL

    Returns:
        dict: Analysis result
    """
    analyzer = SentimentAnalyzer(api_url=api_url)

    if mode == "text":
        return analyzer.analyze_text(input_data)
    elif mode == "audio":
        return analyzer.analyze_audio(input_data)
    elif mode == "video":
        return analyzer.analyze_video(input_data)
    elif mode == "multimodal":
        return analyzer.analyze_multimodal(input_data)
    else:
        raise ValueError("Invalid mode. Choose from: text, audio, video, multimodal")