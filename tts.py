import os
import subprocess

import pyttsx3

engine = None #engine is the TTS object, named as it does all the heavy lifting of converting text to speech

def _init_engine():
    if os.name == "nt":
        # Use the native Windows SAPI driver for better reliability.
        return pyttsx3.init(driverName="sapi5")
    return pyttsx3.init()

def _speak_windows_fallback(text: str):
    # Fallback for Windows when pyttsx3 is unavailable or fails.
    ps_script = (
        "$t = [Console]::In.ReadToEnd(); "
        "Add-Type -AssemblyName System.Speech; "
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "$s.Speak($t)"
    )

    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            input=text,
            text=True,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        print("TTS fallback failed:", text)

def speak(text: str):
    global engine #allows engine to be modified within the function
    try:
        if engine is None:
            engine = _init_engine() #initializes the TTS engine if it hasn't been initialized yet
            engine.setProperty("volume", 1.0)
        engine.say(text) #queues the text to be spoken by the TTS engine
        engine.runAndWait() #plays and runs the queued speech commands, blocking until all speech has been spoken
    except Exception:
        if os.name == "nt":
            _speak_windows_fallback(text)
        else:
            print("TTS failed:", text)
