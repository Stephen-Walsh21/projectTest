import pyttsx3

engine = None #engine is the TTS object, named as it does all the heavy lifting of converting text to speech

def speak(text: str):
    global engine #allows engine to be modified within the function
    try:
        if engine is None:
            engine = pyttsx3.init() #initializes the TTS engine if it hasn't been initialized yet
        engine.say(text) #queues the text to be spoken by the TTS engine
        engine.runAndWait() #plays and runs the queued speech commands, blocking until all speech has been spoken
    except Exception:
        print("TTS failed:", text)
