from faster_whisper import WhisperModel
import streamlit as st

# Load model once with caching
@st.cache_resource
def load_whisper_model():
    return WhisperModel("tiny", compute_type="int8")

@st.cache_data
def audio_to_text(audio_path):
    model = load_whisper_model()
    segments, info = model.transcribe(audio_path)

    text = " ".join(segment.text for segment in segments)

    return text
