import streamlit as st
from transformers import pipeline

# Load sentiment analysis model with caching
@st.cache_resource
def load_model():
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=-1  # Use CPU for compatibility on platforms like Render/Streamlit Cloud
    )

# Load the model
classifier = load_model()

# Streamlit page settings
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

# Page Header
st.markdown("## 🎭 Multimodal Sentiment Classifier")
st.markdown("Analyze sentiment from **text** (for now). Audio/video support coming soon in the GPU version 🚀")
st.write("---")

# Text input
text_input = st.text_input("📩 Enter text for sentiment analysis", "")

# Analyze button
if st.button("🔍 Analyze"):
    if text_input.strip() == "":
        st.warning("⚠️ Please enter some text first.")
    else:
        with st.spinner("Analyzing..."):
            result = classifier(text_input)[0]
            sentiment = result['label']
            confidence = result['score'] * 100

            # Emoji and color mapping
            emoji = "😊" if sentiment == "POSITIVE" else "😔"
            color = "green" if sentiment == "POSITIVE" else "red"

            # Display result
            st.markdown(f"""
            <div class="result-box">
                {emoji} <strong>Sentiment:</strong> <span style="color:{color}">{sentiment}</span><br>
                🔒 <strong>Confidence:</strong> {confidence:.2f}%
            </div>
            """, unsafe_allow_html=True)