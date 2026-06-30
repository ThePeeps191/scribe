# Scribe

Dictate with your voice. Currently only supports Windows.

## Widget Controls

**Left-click and drag**: move the widget around

**Right-click**: close the widget

**Ctrl + Shift + Alt + M**: start or stop the microphone

## Features

- Global hotkey (`Ctrl + Shift + Alt + M`) to start/stop recording from anywhere
- Local speech-to-text via OpenAI Whisper (no internet needed for transcription)
- Optional Groq-powered AI cleanup — fixes misheard words, adds punctuation, removes filler
- Types transcribed text automatically at your cursor
- Compact always-on-top overlay widget with microphone icon and mute indicator

## Setup

1. Copy `.env.example` to `.env` and replace `your-key-here` with your [Groq](https://groq.com) API key (only needed if using Groq cleanup - you can edit the `ASK_GROQ` constant in `main.py`).

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python main.py
   ```

## How It Works

Mic audio → WAV file → Whisper (local) → [Groq AI cleanup] → typed at cursor

- Audio is captured at 44.1kHz mono via `sounddevice`
- Saved as WAV to `audio/` with a Unix timestamp filename
- Transcribed locally with Whisper (`base` model, falls back to `tiny` on low memory)
- Optionally polished via Groq API using a custom prompt (`prompt.txt`)
- Typed at the active cursor position via `pyautogui`

## Tech Stack

- **Python / Tkinter** — overlay window
- **Whisper** — local speech-to-text
- **sounddevice** — audio capture
- **Groq API** — optional AI transcription cleanup
- **PyAutoGUI** — simulate typing
- **keyboard** — global hotkeys

## Using the Executable

1. First download `executable.zip` from [Google Drive](https://drive.google.com/file/d/10M1y_tfQeg-De2dCpXSu9d4NdVE4u329/view?usp=sharing).
2. Unzip `executable.zip`.
3. Run `scribe.exe` as an administrator (needed because the `keyboard` library requires this).

## License

MIT
