import json
from datetime import datetime

def load_schedule(path: str):
    try:
        with open(path, 'r') as f: #r is read
            data = json.load(f)
            # expect list of {"start":"ISO","end":"ISO","title":"..."}
            return data
    except FileNotFoundError:
        return []

def normalized_intervals(events):
    res = [] #makes empty list (res stands for result)
    for e in events: #loop through events
        try:
            s = datetime.fromisoformat(e['start'])
            en = datetime.fromisoformat(e['end']) #parses the start and end times of the event from ISO format into datetime objects
            res.append((s,en)) #add to the list as a tuple of (start, end)
        except Exception: #skip anything that fails to parse (e.g. missing fields, invalid format)
            continue
    res.sort() #sorts the intervals by start time
    return res

def add_schedule_event(path: str, start: str, end: str, title: str):
    s = datetime.fromisoformat(start)
    en = datetime.fromisoformat(end)
    if en <= s:
        raise ValueError("End time must be after start time")

    events = load_schedule(path)
    events.append({"start": s.isoformat(timespec="minutes"), "end": en.isoformat(timespec="minutes"), "title": title})

    with open(path, 'w') as f:
        json.dump(events, f, indent=2)

    return events[-1]

def clear_schedule(path: str):
    events = load_schedule(path)
    removed = len(events)
    with open(path, 'w') as f:
        json.dump([], f, indent=2)
    return removed

def delete_schedule_event_by_title(path: str, title: str):
    events = load_schedule(path)
    needle = title.strip().lower()
    idx = -1
    for i, event in enumerate(events):
        if event.get("title", "").strip().lower() == needle:
            idx = i
            break

    if idx == -1:
        return False

    events.pop(idx)
    with open(path, 'w') as f:
        json.dump(events, f, indent=2)
    return True
