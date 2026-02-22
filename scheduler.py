from datetime import datetime, timedelta, time
import calendar
from ics import Calendar, Event
from zoneinfo import ZoneInfo

ZEITEN = {
    "Frühdienst": ("06:30", "15:00"),
    "Zwischendienst": ("10:00", "19:00"),
    "Spätdienst": ("14:30", "23:00"),
    "Nachtdienst": ("22:30", "08:00"),
}


def parse_time(t_str):
    h, m = map(int, t_str.split(':'))
    return h, m


def dienstzeiten_mit_wegezeit(dienstform, datum, wegezeit_minuten, schicht_zeiten, tz_name="Europe/Berlin"):
    """Gibt (start_dt, end_dt) mit Wegezeit vor/nach zurück oder (None, None) für Frei."""
    if dienstform == "Frei":
        return None, None
    tz = ZoneInfo(tz_name)
    start_str, end_str = schicht_zeiten[dienstform]
    # start_str und end_str können entweder "HH:MM" Strings oder datetime.time Objekte sein
    if isinstance(start_str, str):
        sh, sm = parse_time(start_str)
        start_time = time(sh, sm)
    else:
        start_time = start_str
        
    if isinstance(end_str, str):
        eh, em = parse_time(end_str)
        end_time = time(eh, em)
    else:
        end_time = end_str

    start_dt = datetime.combine(datum, start_time, tzinfo=tz) - timedelta(minutes=wegezeit_minuten)
    
    # Nachtdienst oder Schichten über Mitternacht hinaus: Ende am Folgetag
    # Wir prüfen, ob die Endzeit vor der Startzeit liegt
    if end_time < start_time:
        end_dt = datetime.combine(datum + timedelta(days=1), end_time, tzinfo=tz) + timedelta(minutes=wegezeit_minuten)
    else:
        end_dt = datetime.combine(datum, end_time, tzinfo=tz) + timedelta(minutes=wegezeit_minuten)
    return start_dt, end_dt


def erstelle_kalender(monat, jahr, dienstformen, wegezeit, schicht_zeiten=None, tz_name="Europe/Berlin"):
    if schicht_zeiten is None:
        schicht_zeiten = ZEITEN
    cal = Calendar()
    _, num_days = calendar.monthrange(jahr, monat)
    for tag in range(1, num_days + 1):
        datum = datetime(jahr, monat, tag).date()
        dienstform = dienstformen.get(tag, "Frei")
        if dienstform not in schicht_zeiten and dienstform != "Frei":
            continue
        start, end = dienstzeiten_mit_wegezeit(dienstform, datum, wegezeit, schicht_zeiten, tz_name=tz_name)
        if start and end:
            e = Event()
            e.name = f"{dienstform} Dienst"
            e.begin = start
            e.end = end
            e.description = f"{dienstform} am {datum.strftime('%d.%m.%Y')}"
            cal.events.add(e)
    return cal
