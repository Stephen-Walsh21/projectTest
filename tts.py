import pyttsx3

engine = None

def speak(text: str):
    global engine
    try:
        if engine is None:
            engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        print("TTS failed:", text)
