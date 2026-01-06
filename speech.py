import speech_recognition as sr

def listen_command(timeout=5, phrase_time_limit=8) -> str:
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        try:
            text = r.recognize_google(audio)
            print("Heard:", text)
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""
    except Exception:
        # Microphone not available or other issue
        return ""
