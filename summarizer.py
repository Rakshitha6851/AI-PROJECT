import streamlit as st
from openrouter_utils import call_openrouter

def structured_summarize(sentences):
    text = " ".join(sentences)

    prompt = f"""
    You are an intelligent educational assistant.

    STEP 1: Understand the lecture topic and type
    (e.g., theory class, project explanation, machine learning, mathematics, general concept).

    STEP 2: Create a structured summary using ONLY relevant sections.
    Do NOT force sections that do not apply.

    POSSIBLE SECTIONS (choose only what fits):
    - Topic Overview
    - Key Concepts
    - Definitions
    - Workflow / Process
    - Models / Algorithms
    - Examples / Applications
    - Results / Observations
    - Advantages / Limitations
    - Conclusion / Summary

    RULES:
    - Use bullet points
    - Preserve original meaning
    - Do NOT add new information
    - Do NOT hallucinate
    - Keep technical terms accurate

    OUTPUT FORMAT:
    Use clear section headings followed by bullet points.

    Lecture Transcript:
    {text}
    """

    return call_openrouter(prompt, max_tokens=800)


# Backward compatibility
def summarize_text(sentences):
    return structured_summarize(sentences)
