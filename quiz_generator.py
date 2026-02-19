import re
import streamlit as st
from openrouter_utils import call_openrouter


def format_quiz_output(raw_text):
    """
    Ensures Q and A are always on separate lines
    """

    lines = []
    pairs = re.findall(r"(Q\d+\. .*?)(?:\s+A\d+\. )(.*)", raw_text, re.DOTALL)

    if pairs:
        for i, (q, a) in enumerate(pairs, 1):
            lines.append(q.strip())
            lines.append(f"A{i}. {a.strip()}")
            lines.append("")
        return "\n".join(lines)

    # If already correctly formatted
    return raw_text.strip()


@st.cache_data
def generate_quiz(summary_text):
    prompt = f"""
    You are an experienced university examiner.

    TASK:
    Generate EXACTLY 5 quiz questions based on the summary below.

    COGNITIVE RULES (VERY IMPORTANT):
    - Do NOT copy or rephrase sentences from the summary
    - Questions must test understanding (WHY, HOW, COMPARE, PURPOSE)
    - Each question must be conceptually DIFFERENT from the summary wording
    - Avoid using the same sentence structure as the summary

    FORMAT RULES (MANDATORY):
    Q1. <question>
    A1. <answer>

    Q2. <question>
    A2. <answer>

    Q3. <question>
    A3. <answer>

    Q4. <question>
    A4. <answer>

    Q5. <question>
    A5. <answer>

    ANSWER RULES:
    - Answers must be short (1–2 lines)
    - Answers must be derived ONLY from the summary
    - No new facts

    Summary:
    {summary_text}
    """

    raw_output = call_openrouter(prompt, max_tokens=600)
    return raw_output


def generate_flashcards(summary_text):
    """
    Generate flashcards using OpenRouter
    """

    prompt = f"""
    You are an AI study assistant.

    Convert the structured summary below into 5 study flashcards.

    RULES:
    - Each flashcard should have a clear title
    - Answers should be concise bullet points
    - Do NOT hallucinate

    OUTPUT FORMAT:
    Flashcard 1:
    Title:
    Points:
    - point

    Structured Summary:
    {summary_text}
    """

    return call_openrouter(prompt, max_tokens=500)
