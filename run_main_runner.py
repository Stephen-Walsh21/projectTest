import tts
import speech

# Disable real audio and microphone if no microphone or speaker is available
tts.speak = lambda x: print('SPEAK:', x) #lambda used for simple function that prints the text instead of speaking it out loud
speech.listen_command = lambda timeout=5, phrase_time_limit=8: ""

if __name__ == '__main__':
    import main
    try:
        main.main()
    except SystemExit:
        print('main exited')
