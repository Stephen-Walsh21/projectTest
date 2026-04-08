import json
import os
import threading
from datetime import datetime
from tts import speak

STORE = "reminders.json" #where all reminders are stored (in JSON format - human and machine readable)
ACTIVE_TIMERS = []

def _ensure_store():
    if not os.path.exists(STORE):
        with open(STORE, 'w') as f:
            json.dump([], f) #checks if the reminders file exists and if it doesnt then it creates it

def _parse_time(timestr: str):
    # accept 'YYYY-MM-DD HH:MM' or ISO
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S"): #tries to parse the time string in different formats (with or without seconds, with space or T separator)
        try: #fmt is a loop variable holding data/time formats
            return datetime.strptime(timestr, fmt)
        except Exception:
            continue
    # if all else fails, try ISO format which is more flexible and can handle timezone info
    return datetime.fromisoformat(timestr)

def _same_entry(a, b):
    return (
        a.get("time") == b.get("time")
        and a.get("text") == b.get("text")
        and a.get("kind", "reminder") == b.get("kind", "reminder")
    )

def _cancel_timers_for(predicate): #used for cancelling reminders
    remaining = []
    for item in ACTIVE_TIMERS:
        if predicate(item["entry"]):
            try:
                item["timer"].cancel()
            except Exception:
                pass
        else:
            remaining.append(item)
    ACTIVE_TIMERS.clear()
    ACTIVE_TIMERS.extend(remaining)

def add_reminder(timestr: str, text: str, kind: str = "reminder"):
    _ensure_store() #makes sure reminders file exists
    t = _parse_time(timestr) #converts input string into a datetime object
    entry = {
        "time": t.isoformat(),
        "text": text,
        "kind": kind,
    } #creates a dictionary with the reminder time (in ISO format) and the reminder text
    with open(STORE, 'r+') as f:
        data = json.load(f) #loads the store list
        data.append(entry) #adds to store list
        f.seek(0) #retruns to start of file
        json.dump(data, f, indent=2) #overwrites the file with the updated list of reminders (including the new one just added)
    schedule_entry(entry) #schedules the new reminder to be triggered at the specified time

def list_reminders():
    _ensure_store()
    with open(STORE, 'r') as f: #opens file for reading
        return json.load(f) #reads and returns the list

def list_entries(kind: str | None = None):
    entries = list_reminders()
    if kind is None:
        return entries
    return [e for e in entries if e.get("kind", "reminder") == kind]

def clear_reminders():
    return clear_entries(kind="reminder")

def clear_entries(kind: str | None = None): #used to clear reminders
    _ensure_store()
    with open(STORE, 'r') as f:
        data = json.load(f)

    if kind is None:
        removed = list(data)
        kept = []
    else:
        removed = [e for e in data if e.get("kind", "reminder") == kind]
        kept = [e for e in data if e.get("kind", "reminder") != kind]

    _cancel_timers_for(lambda entry: any(_same_entry(entry, r) for r in removed))

    with open(STORE, 'w') as f: #overwrites with only what we want to keep
        json.dump(kept, f, indent=2)

    return len(removed)

def delete_by_label(label: str, kind: str):
    _ensure_store()
    with open(STORE, 'r') as f:
        data = json.load(f)

    needle = label.strip().lower()
    idx = -1
    for i, entry in enumerate(data):
        if entry.get("kind", "reminder") != kind:
            continue
        if entry.get("text", "").strip().lower() == needle:
            idx = i
            break

    if idx == -1:
        return False

    removed = data.pop(idx)
    _cancel_timers_for(lambda entry: _same_entry(entry, removed))

    with open(STORE, 'w') as f:
        json.dump(data, f, indent=2)

    return True

def _trigger(entry): #reads the reminder out loud
    speak(f"Reminder: {entry['text']}")

def schedule_entry(entry):
    t = datetime.fromisoformat(entry['time'])
    now = datetime.now()
    delta = (t - now).total_seconds()
    if delta <= 0:
        # if the time has passed; trigger immediately
        threading.Thread(target=_trigger, args=(entry,)).start()
    else: #start when time hits
        timer = threading.Timer(delta, _trigger, args=(entry,))
        timer.daemon = True
        ACTIVE_TIMERS.append({"entry": entry, "timer": timer})
        timer.start()

def schedule_existing_reminders():
    _ensure_store()
    with open(STORE, 'r') as f:
        data = json.load(f)
    for e in data:
        schedule_entry(e) #loop through all reminders in the store and schedule them to be triggered at their specified times (if they havent already passed)
