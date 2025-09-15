from scheduler import dienstzeiten_mit_wegezeit, erstelle_kalender
from datetime import datetime

# Teste Februar Schaltjahr und Nicht-Schaltjahr
cases = [
    (2, 2024),  # Schaltjahr, 29 Tage
    (2, 2025),  # Nicht-Schaltjahr, 28 Tage
    (4, 2025),  # April 30 Tage
    (1, 2025),  # Januar 31 Tage
]

for monat, jahr in cases:
    print(f"Testing {monat}/{jahr}")
    _, num_days = __import__('calendar').monthrange(jahr, monat)
    dienstformen = {d: 'Frei' for d in range(1, num_days+1)}
    # setze ein paar Dienste
    if num_days >= 1:
        dienstformen[1] = 'Frühdienst'
    if num_days >= 2:
        dienstformen[2] = 'Nachtdienst'
    cal = erstelle_kalender(monat, jahr, dienstformen, wegezeit=30)
    print(f"Events: {len(cal.events)}")
    assert isinstance(cal.events, set)

print("Basic tests passed")
