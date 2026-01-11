from datetime import datetime, timedelta
from django.utils import timezone

DOW = {"MON":0,"TUE":1,"WED":2,"THU":3,"FRI":4,"SAT":5,"SUN":6}

def _next_weekday(d: datetime, weekday: int) -> datetime:
    days_ahead = weekday - d.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return d + timedelta(days=days_ahead)

def generate_sessions(start_date, time_start, minutes, days_pair, total_sessions=22):
    tz = timezone.get_current_timezone()
    base = timezone.make_aware(datetime.combine(start_date, time_start), timezone=tz)

    candidates = [_next_weekday(base, wd) for wd in days_pair]
    current = min(candidates)

    sessions = []
    while len(sessions) < total_sessions:
        week_start = current - timedelta(days=current.weekday())
        for wd in sorted(days_pair):
            dt = week_start + timedelta(days=wd)
            dt = dt.replace(hour=base.hour, minute=base.minute, second=0, microsecond=0)
            if dt < base:
                continue
            sessions.append((dt, dt + timedelta(minutes=minutes)))
            if len(sessions) >= total_sessions:
                break
        current = current + timedelta(days=7)
    return sessions
