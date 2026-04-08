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
