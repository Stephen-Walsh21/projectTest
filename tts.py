import pyttsx3

engine = pyttsx3.init()

def speak(text: str):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception:
        print("TTS failed:", text)
