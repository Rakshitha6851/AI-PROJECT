# 🎙️ AI Lecture Voice-to-Notes Generator

An intelligent web application that converts lecture audio into comprehensive study materials using AI. Transcribe audio, generate structured summaries, quiz questions, and flashcards automatically.

## ✨ Features

- **Audio Transcription**: Convert .wav, .mp3, and .m4a files to text using advanced Whisper AI
- **Text Cleaning & Analysis**: Automatically clean and analyze transcribed text
- **AI-Powered Summarization**: Generate structured summaries with relevant sections
- **Quiz Generation**: Create 5 conceptual quiz questions with answers
- **Flashcard Creation**: Generate study flashcards from the content
- **Multiple Export Formats**: Download notes as TXT, PDF, or DOCX
- **Modern UI**: Beautiful gradient interface with responsive design

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd voice_to_text
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # or
   source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API key**
   
   Create a `.env` file in the project root:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```
   
   Get your API key from [OpenRouter](https://openrouter.ai/)

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   
   Navigate to `http://localhost:8501`

## 📖 Usage

1. **Upload Audio**: Click the file uploader and select a lecture audio file (.wav, .mp3, or .m4a)
2. **Generate Notes**: Click the "🚀 Generate Notes" button
3. **Wait for Processing**: The app will:
   - Transcribe the audio (may take time for long files)
   - Clean and analyze the text
   - Generate AI-powered summary, quiz, and flashcards
4. **Download Materials**: Use the download buttons to save your study materials

## 🛠️ Dependencies

- **streamlit**: Web app framework
- **torch**: PyTorch for AI models
- **faster-whisper**: Fast Whisper transcription
- **python-dotenv**: Environment variable management
- **requests**: HTTP requests for API calls
- **python-docx**: Word document generation
- **reportlab**: PDF generation
- **numpy, regex**: Text processing

## 🔧 Configuration

### API Configuration

The app uses OpenRouter API for AI features. Make sure your `.env` file contains:
```
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
```

### Model Settings

- **Whisper Model**: Uses "tiny" model for fast transcription (configurable in `speech_to_text.py`)
- **AI Model**: Mistral-7B Instruct via OpenRouter

## 📁 Project Structure

```
voice_to_text/
├── app.py                 # Main Streamlit application
├── speech_to_text.py      # Audio transcription module
├── text_analyzer.py       # Text cleaning and analysis
├── summarizer.py          # AI summarization
├── quiz_generator.py      # Quiz and flashcard generation
├── openrouter_utils.py    # OpenRouter API utilities
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
└── README.md             # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check the license file for details.

## 🆘 Troubleshooting

### Common Issues

**"OpenRouter API key not configured"**
- Ensure your `.env` file exists and contains the correct API key
- Restart the Streamlit app after adding the key

**"Import errors"**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Ensure you're using the correct Python version

**"Audio transcription fails"**
- Check that your audio file is in a supported format
- Ensure the file is not corrupted

**"App shows blank page"**
- Clear browser cache
- Try incognito/private mode
- Check console for JavaScript errors

### Performance Tips

- Use shorter audio files for faster processing
- The "tiny" Whisper model is fast but less accurate; consider "base" or "small" for better quality
- Close other applications to free up RAM for transcription

## 🔗 Links

- [OpenRouter API](https://openrouter.ai/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper)

---

Made with ❤️ for students and educators</content>
<parameter name="filePath">c:\Users\RAKSHITHA\voice_to_text\README.md