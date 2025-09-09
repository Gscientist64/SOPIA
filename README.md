# SOPIA - Your SOP Assistant

This project allows employees to query Standard Operating Procedures (SOPs) and receive answers in a chat-like format.

## Features:
- AI-powered query system that searches within SOP documents (.docx and .pdf).
- Web search integration (via SerpApi) with user consent when SOPs don't have the answer.
- WhatsApp integration using Twilio (sandbox mode for demo).
- Simple frontend interface for user interaction.

## Getting Started:
1. Install dependencies: `pip install -r requirements.txt`
2. Place your SOP documents in the `documents/` folder.
3. Run the app: `python app.py`
4. For WhatsApp, sign up for Twilio and use the sandbox.

## OCR Setup:
If your SOPs contain images with text (e.g., scanned documents), you can enable OCR text extraction:

1. Install **Tesseract**:
   - Windows: [Download Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - macOS: `brew install tesseract`
   - Linux: `sudo apt install tesseract-ocr`

2. Install the required Python libraries:
   ```bash
   pip install pytesseract Pillow

For a more detailed setup, check out the Twilio and SerpApi documentation.