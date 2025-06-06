# sdk/python/sentiment_sdk.py

import requests

API_URL = "http://127.0.0.1:8000"

def analyze_sentiment(input_data, mode="text"):
    if mode == "text":
        response = requests.post(
            f"{API_URL}/predict/text",
            json={"text": input_data}
        )
    elif mode == "audio":
        with open(input_data, "rb") as f:
            response = requests.post(
                f"{API_URL}/predict/audio",
                files={"file": (input_data, f)}
            )
    elif mode == "video":
        with open(input_data, "rb") as f:
            response = requests.post(
                f"{API_URL}/predict/video",
                files={"file": (input_data, f)}
            )
    elif mode == "multimodal":
        with open(input_data, "rb") as f:
            response = requests.post(
                f"{API_URL}/predict/multimodal",
                files={"file": (input_data, f)}
            )
    else:
        raise ValueError("Invalid mode. Choose from text, audio, video, multimodal.")

    if response.status_code != 200:
        raise Exception(f"API error: {response.text}")

    return response.json()