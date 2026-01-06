import json
from datetime import datetime

def load_schedule(path: str):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            # expect list of {"start":"ISO","end":"ISO","title":"..."}
            return data
    except FileNotFoundError:
        return []

def normalized_intervals(events):
    res = []
    for e in events:
        try:
            s = datetime.fromisoformat(e['start'])
            en = datetime.fromisoformat(e['end'])
            res.append((s,en))
        except Exception:
            continue
    res.sort()
    return res
