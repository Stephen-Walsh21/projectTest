from speech import listen_command
from tts import speak
import reminders
import fitness
import schedule as schedule_mod
import time

def handle_command(cmd: str): #takes the command as a string and processes (text/voice) to determine what action to take
    cmd = cmd.lower().strip() #cmd is a string that represents the user's command. The code converts it to lowercase and removes leading/trailing whitespace to standardize it for easier processing
    if not cmd:
        return
    #explicit list query first to avoid matching the generic 'remind' keyword
    if "list" in cmd and "remind" in cmd:
        for r in reminders.list_reminders():
            print(r)
            speak(str(r))
    elif "remind" in cmd or "reminder" in cmd:
        speak("Please type the reminder time in ISO format, e.g. 2026-01-06 14:30")
        t = input("Reminder time (YYYY-MM-DD HH:MM): ")
        text = input("Reminder text: ")
        reminders.add_reminder(t, text)
        speak("Reminder set.")
    elif "alarm" in cmd:
        speak("Please type alarm time in ISO format, e.g. 2026-01-06 07:00")
        t = input("Alarm time (YYYY-MM-DD HH:MM): ")
        text = input("Alarm label: ")
        reminders.add_reminder(t, text)
        speak("Alarm scheduled.")
    elif "analyze" in cmd or "fitness" in cmd:
        speak("Loading schedule.json and analyzing free time.")
        sched = schedule_mod.load_schedule("schedule.json")
        plan = fitness.analyze_schedule(sched)
        for item in plan: #item is the individual workout suggestion
            out = f"{item['time_range']}: {item['activity']}"
            print(out)
            speak(out)
    elif cmd in ("exit","quit","stop"):
        speak("Goodbye")
        raise SystemExit
    else:
        speak("Command not recognized. Try: set reminder, set alarm, analyze schedule, list reminders, or exit.")

def main():
    reminders.schedule_existing_reminders() #schedules any reminders that were added in previous runs of the program (stored in reminders.json)
    speak("Assistant ready. Say a command or type it.")
    while True:
        try:
            cmd = listen_command()
        except Exception:
            cmd = ""
        if not cmd: #waits for a voice command, if it doesnt hear one then it waits for a text command instead
            cmd = input(">> ")
        handle_command(cmd)
        time.sleep(0.2) #pauses the loop for a short time before the next cycle so that the CPU isnt overworked

if __name__ == '__main__': 
    main() #only runs the main function if this script is executed directly (not imported as a module)
