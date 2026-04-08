import speech_recognition as sr

def listen_command(timeout=5, phrase_time_limit=8) -> str:
    r = sr.Recognizer() #r (recogniser) gets ready to listen to audio and then convert to text
    try:
        with sr.Microphone() as source: #uses the default microphone as the audio source
            r.adjust_for_ambient_noise(source, duration=0.5) #listens to the ambient noise for 0.5 seconds to calibrate the recognizer to ignore background noise
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit) #listens for a single phrase from the microphone with the specified timeout and phrase time limit
        try:
            text = r.recognize_google(audio) #uses Google's speech recognition API (Application programming interface) to convert the captured audio into text
            print("Heard:", text) #prints the recognised text
            return text
        except sr.UnknownValueError: #if the recognizer could not understand the audio, it raises an UnknownValueError exception, which is caught here and results in an empty string being returned
            return ""
        except sr.RequestError: #If there was an issue with the API request (e.g. network error, invalid API key), it raises a RequestError exception, which is also caught here and results in an empty string being returned
            return ""
    except Exception:
        # Microphone not available or other issue
        return ""
