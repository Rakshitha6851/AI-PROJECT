from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env in the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
load_dotenv(env_path)

# Read OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct"


def call_openrouter(prompt, max_tokens=800):
    if not OPENROUTER_API_KEY:
        return "❌ OpenRouter API key not configured. Please set OPENROUTER_API_KEY."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/yourusername/lecture-voice-to-notes-generator",
        "X-Title": "Lecture Voice-to-Notes Generator"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.3
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        return (
            "⚠️ AI service temporarily unavailable. Please try again.\n\n"
            f"Details: {e}"
        )
