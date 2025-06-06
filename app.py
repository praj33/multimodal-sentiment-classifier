import streamlit as st
from transformers import pipeline

# Load model with caching
@st.cache_resource
def load_model():
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=-1
    )

# Load pipeline
classifier = load_model()

# Set page config with emoji and dark mode preference
st.set_page_config(
    page_title="🎭 Multimodal Sentiment Classifier",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .stButton>button {
        background-color: #e11d48;
        color: white;
        padding: 0.6em 1.5em;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.1em;
    }
    .stButton>button:hover {
        background-color: #be123c;
        color: white;
    }
    .result-box {
        background-color: #1f2937;
        color: white;
        padding: 1em;
        border-radius: 12px;
        margin-top: 1em;
        font-size: 1.1em;
    }
    </style>
""", unsafe_allow_html=True)

# Header with emoji
st.markdown("## 🎭 Multimodal Sentiment Classifier")
st.markdown("Analyze sentiment from **text** (for now). Audio/video coming soon in the GPU version 🚀")
st.write("---")

# Input
text_input = st.text_input("📩 Enter text for sentiment analysis", "")

# Button
if st.button("🔍 Analyze"):
    if text_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        result = classifier(text_input)[0]
        sentiment = result['label']
        confidence = result['score'] * 100

        # Emoji mapping
        emoji = "😊" if sentiment == "POSITIVE" else "😔"
        color = "green" if sentiment == "POSITIVE" else "red"

        st.markdown(f"""
        <div class="result-box">
            {emoji} <strong>Sentiment:</strong> <span style="color:{color}">{sentiment}</span>  
            <br>
            🔒 <strong>Confidence:</strong> {confidence:.2f}%
        </div>
        """, unsafe_allow_html=True)