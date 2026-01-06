import tts
import speech

# Disable real audio and microphone for headless run
tts.speak = lambda x: print('SPEAK:', x)
speech.listen_command = lambda timeout=5, phrase_time_limit=8: ""

if __name__ == '__main__':
    import main
    try:
        main.main()
    except SystemExit:
        print('main exited')
