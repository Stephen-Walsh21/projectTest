from datetime import datetime, time as dtime
from schedule import normalized_intervals

def analyze_schedule(events, day_start="06:00", day_end="22:00"):
    # events: list of dicts with ISO start/end
    busy = normalized_intervals(events)
    ds = datetime.combine(datetime.today(), datetime.strptime(day_start, "%H:%M").time())
    de = datetime.combine(datetime.today(), datetime.strptime(day_end, "%H:%M").time())
    free = []
    cur = ds
    for s,en in busy:
        if en <= cur:
            continue
        if s <= cur < en:
            cur = max(cur, en)
            continue
        if s > cur:
            free.append((cur,s))
            cur = max(cur, en)
    if cur < de:
        free.append((cur,de))

    # turn free slots into simple exercises
    plan = []
    for (s,en) in free:
        minutes = int((en - s).total_seconds() // 60)
        if minutes < 15:
            continue
        if minutes < 30:
            act = "Quick stretch / core (15 minutes)"
            duration = 15
        elif minutes < 45:
            act = "HIIT or brisk walk (30 minutes)"
            duration = 30
        else:
            act = "Full workout: cardio + strength (45 minutes)"
            duration = 45
        start_str = s.strftime("%H:%M")
        end_time = (s + (en - s))
        end_str = (s + (en - s)).strftime("%H:%M")
        plan.append({"time_range": f"{start_str}-{end_str}", "activity": act, "suggested_minutes": duration})
    return plan
