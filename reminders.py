import json
import os
import threading
from datetime import datetime
from tts import speak

STORE = "reminders.json"

def _ensure_store():
    if not os.path.exists(STORE):
        with open(STORE, 'w') as f:
            json.dump([], f)

def _parse_time(timestr: str):
    # accept 'YYYY-MM-DD HH:MM' or ISO
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(timestr, fmt)
        except Exception:
            continue
    # last resort
    return datetime.fromisoformat(timestr)

def add_reminder(timestr: str, text: str):
    _ensure_store()
    t = _parse_time(timestr)
    entry = {"time": t.isoformat(), "text": text}
    with open(STORE, 'r+') as f:
        data = json.load(f)
        data.append(entry)
        f.seek(0)
        json.dump(data, f, indent=2)
    schedule_entry(entry)

def list_reminders():
    _ensure_store()
    with open(STORE, 'r') as f:
        return json.load(f)

def _trigger(entry):
    speak(f"Reminder: {entry['text']}")

def schedule_entry(entry):
    t = datetime.fromisoformat(entry['time'])
    now = datetime.now()
    delta = (t - now).total_seconds()
    if delta <= 0:
        # past; trigger immediately
        threading.Thread(target=_trigger, args=(entry,)).start()
    else:
        timer = threading.Timer(delta, _trigger, args=(entry,))
        timer.daemon = True
        timer.start()

def schedule_existing_reminders():
    _ensure_store()
    with open(STORE, 'r') as f:
        data = json.load(f)
    for e in data:
        schedule_entry(e)
