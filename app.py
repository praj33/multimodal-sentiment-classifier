import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=-1)

classifier = load_model()

# UI setup
st.set_page_config(
    page_title="🎭 Multimodal Sentiment Classifier",
    page_icon="💬",
    layout="centered"
)

st.title("🎭 Multimodal Sentiment Classifier")
st.markdown("Analyze sentiment from text (for now). Audio/video coming soon in the GPU version!")

user_input = st.text_input("Enter text for sentiment analysis")

if st.button("🔍 Analyze"):
    if user_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        result = classifier(user_input)[0]
        label_map = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
        sentiment = label_map.get(result["label"], result["label"])
        confidence = round(result["score"] * 100, 2)

        if sentiment == "Positive":
            st.success(f"😊 Sentiment: {sentiment} — Confidence: {confidence}%")
        elif sentiment == "Negative":
            st.error(f"😠 Sentiment: {sentiment} — Confidence: {confidence}%")
        else:
            st.info(f"😐 Sentiment: {sentiment} — Confidence: {confidence}%")