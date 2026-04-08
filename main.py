from speech import listen_command
from tts import speak
import reminders
import fitness
import schedule as schedule_mod
import time
import re #regular expression to check for specific words in the command in a flexible way (e.g. "set an alarm" vs "set alarm for 7am")

def _ask_with_voice_fallback(speech_prompt: str, text_prompt: str):
    speak(speech_prompt) #says prompt out loud
    try:
        heard = listen_command(timeout=5, phrase_time_limit=5)
    except Exception:
        heard = "" #if nothing gets said
    if heard and heard.strip():
        return heard.strip()
    return input(text_prompt).strip()

def handle_command(cmd: str): #takes the command as a string and processes (text/voice) to determine what action to take
    cmd = cmd.lower().strip() #cmd is a string that represents the user's command. The code converts it to lowercase and removes leading/trailing whitespace to standardize it for easier processing
    if not cmd:
        return
    def has_word(word: str):
        return re.search(rf"\b{re.escape(word)}\b", cmd) is not None

    # Identify user intent and topic from the command text.
    wants_list = any(has_word(word) for word in ("list", "show", "display", "what"))
    wants_set = any(has_word(word) for word in ("set", "add", "create", "new"))
    has_alarm = has_word("alarm") or has_word("alarms")
    has_reminder = has_word("remind") or has_word("reminder") or has_word("reminders")
    has_schedule = has_word("schedule") or has_word("schedules")
    has_event = has_word("event") or has_word("events")

    # Clear flows: schedule, reminders, or alarms.
    if has_word("clear") and (has_reminder or has_alarm or has_schedule):
        if has_schedule:
            choice = _ask_with_voice_fallback(
                "Do you want to clear all schedule events or just one?",
                "Clear 'all' or 'one': ",
            ).lower()
            if choice == "all":
                existing_events = schedule_mod.load_schedule("schedule.json")
                removed = schedule_mod.clear_schedule("schedule.json")
                if removed:
                    names = ", ".join(e.get("title", "Untitled") for e in existing_events)
                    speak(f"Cleared all schedule events: {names}")
                else:
                    speak("No schedule events to clear.")
            elif choice == "one":
                title = _ask_with_voice_fallback(
                    "Say or type the schedule event title to clear.",
                    "Event title to clear: ",
                )
                if schedule_mod.delete_schedule_event_by_title("schedule.json", title):
                    speak(f"Cleared schedule event: {title}")
                else:
                    speak("No schedule event found with that title.")
            else:
                speak("Please choose all or one.")
            return

        kind = "alarm" if has_alarm else "reminder"
        scope = "alarms" if kind == "alarm" else "reminders"
        choice = _ask_with_voice_fallback(
            f"Do you want to clear all {scope} or just one?",
            "Clear 'all' or 'one': ",
        ).lower()
        if choice == "all":
            existing_items = reminders.list_entries(kind=kind)
            removed = reminders.clear_entries(kind=kind)
            if removed:
                names = ", ".join(item.get("text", "Untitled") for item in existing_items)
                speak(f"Cleared all {scope}: {names}")
            else:
                speak(f"No {scope} to clear.")
        elif choice == "one":
            label = _ask_with_voice_fallback(
                f"Say or type the {kind} label to clear.",
                f"Type the {kind} label to clear: ",
            )
            if reminders.delete_by_label(label, kind=kind):
                speak(f"Cleared {kind}: {label}")
            else:
                speak(f"No {kind} found with that label.")
        else:
            speak("Please choose all or one.")
        return

    # Explicit list queries first to avoid matching generic set branches.
    elif wants_list and has_event:
        events = schedule_mod.load_schedule("schedule.json")
        if not events:
            speak("No schedule events found.")
        for event in events:
            out = f"Event: {event.get('title', 'Untitled')} from {event.get('start', '?')} to {event.get('end', '?')}"
            print(out)
            speak(out)
    elif wants_list and has_alarm:
        alarms = reminders.list_entries(kind="alarm")
        if not alarms:
            speak("No alarms scheduled.")
        for r in alarms:
            out = f"Alarm: {r.get('text', 'Untitled')} at {r.get('time', '?')}"
            print(out)
            speak(out)
    elif wants_list and has_reminder:
        reminder_items = reminders.list_entries(kind="reminder")
        if not reminder_items:
            speak("No reminders scheduled.")
        for r in reminder_items:
            out = f"Reminder: {r.get('text', 'Untitled')} at {r.get('time', '?')}"
            print(out)
            speak(out)

    # Create new reminders, alarms, or events.
    elif wants_set and has_reminder:
        speak("Please type the reminder time in ISO format, e.g. 2026-01-06 14:30")
        t = input("Reminder time (YYYY-MM-DD HH:MM): ")
        text = input("Reminder text: ")
        reminders.add_reminder(t, text, kind="reminder")
        speak("Reminder set.")
    elif wants_set and has_alarm:
        speak("Please type alarm time in ISO format, e.g. 2026-01-06 07:00")
        t = input("Alarm time (YYYY-MM-DD HH:MM): ")
        text = input("Alarm label: ")
        reminders.add_reminder(t, text, kind="alarm")
        speak("Alarm scheduled.")
    elif wants_set and has_event:
        title = _ask_with_voice_fallback(
            "What is the event title?",
            "Event title: ",
        )
        start = _ask_with_voice_fallback(
            "What is the event start time? Use ISO format like 2026-01-06 09:00",
            "Event start (YYYY-MM-DD HH:MM): ",
        )
        end = _ask_with_voice_fallback(
            "What is the event end time? Use ISO format like 2026-01-06 10:00",
            "Event end (YYYY-MM-DD HH:MM): ",
        )
        try:
            event = schedule_mod.add_schedule_event("schedule.json", start, end, title)
            speak(f"Added to schedule: {event['title']} from {event['start']} to {event['end']}")
        except Exception:
            speak("Couldn't add that event. Please use valid times and make sure end is after start.")

    # Analyze current schedule and suggest workout slots.
    elif "analyze" in cmd or "fitness" in cmd:
        speak("Loading schedule.json and analyzing free time.")
        sched = schedule_mod.load_schedule("schedule.json")
        plan = fitness.analyze_schedule(sched)
        for item in plan: #item is the individual workout suggestion
            out = f"{item['time_range']}: {item['activity']}"
            print(out)
            speak(out)

    # Exit command.
    elif cmd in ("exit","quit","stop"):
        speak("Goodbye")
        raise SystemExit
    else:
        speak("Command not recognized. Try: set reminder, set alarm, add event, analyze schedule, list events, list reminders, list alarms, clear schedule, clear reminders, clear alarms, or exit.")

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
