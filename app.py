import os
import base64
from io import BytesIO
import streamlit as st

# ================= PROJECT IMPORTS =================
from speech_to_text import audio_to_text
from text_analyzer import analyze_and_clean_text
from summarizer import structured_summarize
from quiz_generator import generate_quiz, generate_flashcards

api_key = os.getenv("OPENAI_API_KEY")

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Lecture Voice-to-Notes Generator",
    layout="wide"
)

# ================= GLOBAL STYLING =================
st.markdown(
    """
    <style>
    /* ================= MAIN BACKGROUND ================= */
.stApp {
    background: linear-gradient(135deg, #e0f2ff 0%, #bae6fd 50%, #7dd3fc 100%);
    color: #0f172a !important;
}



    /* ================= FORCE ALL TEXT LIGHT ================= */
   .stApp * {
    color: #0f172a !important; 
    font-weight: 500;
}


    /* ================= HEADERS ================= */
    h1, h2, h3, h4, h5, h6 {
        color: #60a5fa !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(96, 165, 250, 0.3);
    }

    /* ================= QUIZ STYLING ================= */
    .quiz-box .question {
        color: #fbbf24 !important;
        font-weight: 700;
        background: rgba(251, 191, 36, 0.1);
        padding: 8px;
        border-left: 4px solid #fbbf24;
        border-radius: 4px;
        margin: 10px 0;
    }

    .quiz-box .answer {
        color: #4ade80 !important;
        background: rgba(74, 222, 128, 0.1);
        padding: 8px;
        border-left: 4px solid #4ade80;
        border-radius: 4px;
        margin: 5px 0 15px 0;
    }

    /* ================= FILE UPLOADER (MODERN GRADIENT) ================= */
    div[data-testid="stFileUploader"] {
        background: linear-gradient(135deg, rgba(96, 165, 250, 0.15), rgba(139, 92, 246, 0.15));
        border: 2px solid #60a5fa;
        border-radius: 12px;
        padding: 22px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(96, 165, 250, 0.1);
    }

    div[data-testid="stFileUploader"] label,
    div[data-testid="stFileUploader"] span {
        color: #60a5fa !important;
        font-size: 16px;
        font-weight: 600;
    }

    /* ================= BUTTONS ================= */
    button {
        background: linear-gradient(135deg,#8b5cf6);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: 600;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }

    button:hover {
        background: linear-gradient(135deg, #60a5fa, #a78bfa);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(96, 165, 250, 0.6);
    }

    /* ================= DOWNLOAD BUTTON ================= */
    div[data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #10b981, #06b6d4);
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }

    div[data-testid="stDownloadButton"] button:hover {
        background: linear-gradient(135deg, #34d399, #22d3ee);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6);
    }

    /* ================= TEXT INPUTS & CONTAINERS ================= */
    div[data-testid="stTextInput"],
    div[data-testid="stTextArea"],
    textarea {
        background: rgba(30, 41, 59, 0.8) !important;
        color: #e0e7ff !important;
        border: 1px solid #475569 !important;
        border-radius: 8px;
    }

    /* ================= SUBHEADERS ================= */
    .markdown-text-container {
        background: rgba(30, 41, 59, 0.5);
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #60a5fa;
        margin: 10px 0;
    }

    /* ================= SPINNERS ================= */
    .stSpinner {
        color: #60a5fa !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================= BACKGROUND IMAGE =================
def add_bg_from_local(image_file):
    if not os.path.exists(image_file):
        return  # Skip if file doesn't exist
    
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local(r"background.png")

# ================= QUIZ STYLING =================
st.markdown(
    """
    <style>
    .quiz-box {
        background: rgba(30, 41, 59, 0.3);
        padding: 15px;
        border-radius: 8px;
        border: 1px solid rgba(96, 165, 250, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================= HELPERS =================
def style_quiz_output(raw_text):
    html = '<div class="quiz-box">'
    for line in raw_text.split("\n"):
        line = line.strip()
        if line.startswith("Q"):
            html += f'<div class="question">{line}</div>'
        elif line.startswith("A"):
            html += f'<div class="answer">{line}</div>'
    html += "</div>"
    return html


def download_text(filename, text):
    st.download_button(
        label=f"⬇️ Download {filename}",
        data=text,
        file_name=filename,
        mime="text/plain"
    )

# ================= PDF =================
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(summary, quiz, flashcards):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Lecture Summary</b>", styles["Title"]))
    story.append(Paragraph(summary.replace("\n", "<br/>"), styles["Normal"]))
    story.append(Paragraph("<br/><b>Quiz Questions</b>", styles["Title"]))
    story.append(Paragraph(quiz.replace("\n", "<br/>"), styles["Normal"]))
    story.append(Paragraph("<br/><b>Flashcards</b>", styles["Title"]))
    story.append(Paragraph(flashcards.replace("\n", "<br/>"), styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ================= DOCX =================
from docx import Document

def generate_docx(summary, quiz, flashcards):
    doc = Document()
    doc.add_heading("Lecture Summary", level=1)
    doc.add_paragraph(summary)
    doc.add_heading("Quiz Questions", level=1)
    doc.add_paragraph(quiz)
    doc.add_heading("Flashcards", level=1)
    doc.add_paragraph(flashcards)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def generate_combined_text(summary, quiz, flashcards):
    return f"""
LECTURE SUMMARY
----------------
{summary}

QUIZ QUESTIONS
--------------
{quiz}

FLASHCARDS
----------
{flashcards}
"""

# ================= UI =================
st.title("🎙️ AI Lecture Voice-to-Notes Generator")

uploaded_file = st.file_uploader(
    "Upload Lecture Audio (.wav / .mp3 / .m4a)",
    type=["wav", "mp3", "m4a"]
)

if uploaded_file:
    audio_path = os.path.abspath(
        "uploaded_audio." + uploaded_file.name.split(".")[-1]
    )

    with open(audio_path, "wb") as f:
        f.write(uploaded_file.read())

    if st.button("🚀 Generate Notes"):
        with st.spinner("🎤 Transcribing audio..."):
            raw_text = audio_to_text(audio_path)
        
        with st.spinner("🧹 Cleaning and analyzing text..."):
            clean_sentences = analyze_and_clean_text(raw_text)

        st.subheader("📄 Cleaned Lecture Text")
        st.write(" ".join(clean_sentences))

        with st.spinner("📝 Generating summary..."):
            summary = structured_summarize(clean_sentences)
        st.subheader("📝 Structured Summary")
        st.write(summary)
        download_text("summary.txt", summary)

        with st.spinner("❓ Generating quiz questions..."):
            quiz_output = generate_quiz(summary)
        st.subheader("❓ Quiz Questions (AI Generated)")
        st.markdown(style_quiz_output(quiz_output), unsafe_allow_html=True)
        download_text("quiz_questions.txt", quiz_output)

        with st.spinner("🧠 Generating flashcards..."):
            flashcard_output = generate_flashcards(summary)
        st.subheader("🧠 Flashcards (AI Generated)")
        st.write(flashcard_output)
        download_text("flashcards.txt", flashcard_output)

        st.subheader("⬇️ Download Study Materials")

        combined_text = generate_combined_text(
            summary, quiz_output, flashcard_output
        )

        st.download_button("📊 Download Combined Notes (TXT)", combined_text)
        st.download_button("📄 Download Report (PDF)", generate_pdf(summary, quiz_output, flashcard_output))
        st.download_button("📑 Download Report (DOCX)", generate_docx(summary, quiz_output, flashcard_output))

