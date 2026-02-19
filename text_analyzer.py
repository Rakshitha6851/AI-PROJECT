import re
import streamlit as st
from difflib import SequenceMatcher

# Common ML / DS term corrections
TERM_MAP = {
    "time cities": "time series",
    "mission learning": "machine learning",
    "expert data analysis": "exploratory data analysis",
    "prepositing": "preprocessing",
    "stream": "streamlit",
    "mean square": "mean squared",
    "mean absolute square": "mean absolute error",
}

def correct_terms(sentence):
    s = sentence.lower()
    for wrong, correct in TERM_MAP.items():
        s = s.replace(wrong, correct)
    return s.capitalize()

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

@st.cache_data
def analyze_and_clean_text(text):
    # 1. Normalize spacing (DO NOT lowercase whole text permanently)
    text = re.sub(r"\s+", " ", text).strip()

    # 2. Sentence split (preserve structure)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    cleaned = []
    for s in sentences:
        if len(s.split()) < 6:
            continue

        s = correct_terms(s)

        # 3. Remove near-duplicates
        if not any(similarity(s, prev) > 0.88 for prev in cleaned):
            cleaned.append(s)

    return cleaned
