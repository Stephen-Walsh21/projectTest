from datetime import datetime, time as dtime
from schedule import normalized_intervals

def analyze_schedule(events, day_start="06:00", day_end="22:00"): #arbitrary day start/end time
    # events: list of dictionaries with ISO (standard date/time format) start/end
    # Normalize the raw schedule into sorted, merged busy intervals
    busy = normalized_intervals(events)

    # Convert the day start/end strings into datetime objects for today
    ds = datetime.combine(datetime.today(), datetime.strptime(day_start, "%H:%M").time())
    de = datetime.combine(datetime.today(), datetime.strptime(day_end, "%H:%M").time())

    free = [] #list to hold free time slots
    cur = ds #pointer to track current time as we scan through busy intervals

    # Find gaps between busy intervals and collect them as free slots
    for s, en in busy: #s = start time, en = end time of a busy interval
        if en <= cur:
            # This busy interval ends before or exactly at current pointer (so ignore it)
            continue
        if s <= cur < en:
            # Current pointer is inside a busy interval, so skip ahead to its end.
            cur = max(cur, en)
            continue
        if s > cur:
            # Then there is a free gap before the next busy interval
            free.append((cur, s))
            cur = max(cur, en)
    if cur < de:
        # Add any remaining free time between the last event and the end of day
        free.append((cur, de))

    # Convert free slots into suggested workout activities
    plan = []
    for (s, en) in free:
        minutes = int((en - s).total_seconds() // 60)
        if minutes < 15:
            # This skips very short gaps that are too small for a workout
            continue
        if minutes < 30:
            #This is enough time for a quick workout
            act = "Quick stretch / core (15 minutes)"
            duration = 15
        elif minutes < 45:
            #More time means longer workout
            act = "HIIT or brisk walk (30 minutes)"#HIIT = High-Intensity Interval Training (workout that alternates between intense activity and periods of less-intense activity/complete rest)
            duration = 30
        else:
            #Lots of free time so you've enough time for a full workout
            act = "Full workout: cardio + strength (45 minutes)"
            duration = 45

        start_str = s.strftime("%H:%M") #formats the start time of the free slot into a string like "14:30"
        end_str = en.strftime("%H:%M") #formats the end time of the free slot into a string like "15:15"
        plan.append({
            "time_range": f"{start_str}-{end_str}",
            "activity": act,
            "suggested_minutes": duration,
        }) #makes a list of the activities to do, the time to do it and the suggested duration of the activity
    return plan
