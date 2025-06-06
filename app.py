import streamlit as st
from transformers import pipeline
import torch

# Load sentiment pipeline (text only for now)
@st.cache_resource
def load_model():
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=-1  # Use CPU
    )

classifier = load_model()

# UI
st.set_page_config(page_title="Multimodal Sentiment Classifier", layout="centered")
st.title("🎭 Multimodal Sentiment Classifier")
st.markdown("Analyze sentiment from text (for now). Audio/video coming soon in the GPU version!")

# Text Input
text_input = st.text_area("Enter text for sentiment analysis", placeholder="I love this project!")

if st.button("Analyze"):
    if text_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("Analyzing..."):
            result = classifier(text_input)[0]
            st.success(f"**Sentiment:** {result['label']} — **Confidence:** {round(result['score'] * 100, 2)}%")