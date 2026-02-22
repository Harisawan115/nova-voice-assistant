# NOVA – AI Voice Assistant

NOVA is a desktop-based AI voice assistant built with Python.
It supports speech recognition, text-to-speech, web automation, and
information retrieval through a modern GUI interface.

---

## Overview

NOVA allows users to interact with their system using voice or text commands. It integrates speech recognition, natural language processing, and online services such as YouTube, Google Search, and Wikipedia.
The application is designed with multi-threading to ensure smooth UI performance during voice processing

---

## Features

### Voice Interaction

* Speech-to-Text using Google Speech Recognition
* Text-to-Speech using gTTS (online) and pyttsx3 (offline fallback)
* Ambient noise adjustment for improved accuracy

### Assistant Capabilities

* Open YouTube and perform searches
* Google search via voice command
* Fetch Wikipedia summaries
* Play songs from YouTube
* Provide current time and date

### GUI

* Built with Tkinter
* Dark-themed interface
* Status indicators
* Thread-safe UI updates

---

## Tech Stack

* Python 3.8+
* Tkinter
* SpeechRecognition
* gTTS
* pyttsx3
* PyWhatKit
* Wikipedia API
* Pygame
* Threading

---

## Installation

Clone the repository:

```bash
git clone https://github.com/harisawan115/nova-voice-assistant.git
cd nova-voice-assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python nova_assistant.py
```

---

## Example Commands

Voice mode supports commands such as:

* “What time is it?”
* “Play Believer”
* “Search Wikipedia for Artificial Intelligence”
* “Open YouTube”
* “Google search latest AI news”

---

## Author

Haris Awan
Portfolio: [https://haris-awan.vercel.app](https://haris-awan.vercel.app)

---
