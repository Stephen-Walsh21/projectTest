# Voice-driven Personal Assistant (basic scaffold)

This repository contains a minimal voice-driven assistant scaffold with features:

- Set reminders / alarms (persistent in `reminders.json`)
- Text-to-speech via `pyttsx3`
- Respond to voice commands (uses `SpeechRecognition` with Google recognizer)
- Analyze a schedule (`schedule.json`) and propose a simple fitness plan

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. On Linux, install PortAudio for `pyaudio` (Debian/Ubuntu):

```bash
sudo apt-get update && sudo apt-get install -y portaudio19-dev python3-pyaudio
```

3. Run the assistant:

```bash
python main.py
```

Notes

- `schedule.json` is a small example file. The analyzer expects ISO timestamps.
- Voice input may require a working microphone and drivers; if voice fails, the CLI falls back to typed commands.
