# run_sentiment.py

import argparse
from classifiers.text_classifier import TextClassifier
from classifiers.audio_classifier import AudioClassifier
from classifiers.video_classifier import VideoClassifier
from fusion.fusion_engine import FusionEngine

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input file")
    parser.add_argument("--mode", choices=["text", "audio", "video", "multimodal"], required=True)
    args = parser.parse_args()          

    results = []

    if args.mode == "text" or args.mode == "multimodal":
        text_model = TextClassifier()
        sentiment, score = text_model.predict("I love this project!")  # Dummy input for now
        results.append((sentiment, score))

    if args.mode == "audio" or args.mode == "multimodal":
        audio_model = AudioClassifier()
        sentiment, score = audio_model.predict(args.input)
        results.append((sentiment, score))

    if args.mode == "video" or args.mode == "multimodal":
        video_model = VideoClassifier()
        sentiment, score = video_model.predict(args.input)
        results.append((sentiment, score))

    if args.mode == "multimodal":
        fusion = FusionEngine()
        final_sentiment, confidence = fusion.predict(results)
        print(f"Fused Sentiment: {final_sentiment} (Confidence: {confidence:.2f})")
    else:
        sentiment, score = results[0]
        print(f"Sentiment: {sentiment} (Confidence: {score:.2f})")

if __name__ == "__main__":
    main()