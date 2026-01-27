import calendar
import streamlit as st
from datetime import datetime, timedelta, time
from ics import Calendar, Event
from zoneinfo import ZoneInfo  # Python 3.9+
from scheduler import erstelle_kalender, dienstzeiten_mit_wegezeit

aktueller_monat = datetime.now().month
aktuelles_jahr = datetime.now().year

monat = aktueller_monat + 1 if aktueller_monat < 12 else 1
jahr = aktuelles_jahr if monat != 1 else aktuelles_jahr + 1


# Hinweis: Anzahl der Tage wird nach der Eingabe von Monat/Jahr berechnet (siehe weiter unten)

zeiten = {
    "Frühdienst": ("07:00", "15:30"),
    "Zwischendienst": ("10:00", "19:00"),
    "Spätdienst": ("15:00", "23:30"),
    "Nachtdienst": ("23:00", "07:30"),
}


wegezeit = 30

st.title("Schichtplan zu iCal")
col1, col2 = st.columns(2)
with col1:
    monat = st.number_input(label="Monat", min_value=1, max_value=12, value=monat, step=1)
with col2:
    jahr = st.number_input(label="Jahr", min_value=aktuelles_jahr - 3, max_value=aktuelles_jahr + 5, value=jahr, step=1)

# Jetzt die Anzahl Tage basierend auf der aktuellen Auswahl berechnen
_, anzahl_tage = calendar.monthrange(jahr, monat)
# Session State für tage initialisieren oder aktualisieren (immer exakt gültige Tage)
tage_dict = st.session_state.get('tage', {})
tage = {tag: tage_dict.get(tag, "Frei") for tag in range(1, anzahl_tage+1)}
st.session_state['tage'] = tage

with st.expander("Schichtzeiten konfigurieren"):
    for schicht, (start, ende) in zeiten.items():
        s_col1, s_col2, s_col3 = st.columns([1.5, 2, 2])
        start_h, start_m = map(int, start.split(":"))
        ende_h, ende_m = map(int, ende.split(":"))
        with s_col1:
            st.markdown(f"<p style='text-align:center; margin-top: 2em;'>{schicht}</p>", unsafe_allow_html=True)
        with s_col2:
            st.time_input(label="Startzeit", value=time(start_h, start_m), key=f"{schicht}_start")
        with s_col3:
            st.time_input(label="Endzeit", value=time(ende_h, ende_m), key=f"{schicht}_ende")
        st.markdown("<hr style='margin: 0.05em 0; border: 1px solid gray;'>", unsafe_allow_html=True)
        
    w_col1, w_col2, w_col3 = st.columns([1.5, 2, 2])
    with w_col1:
            st.markdown(f"<p style='text-align:center; margin-top: 2em;'>Wegezeit</p>", unsafe_allow_html=True)
    with w_col2:
        wegezeit = st.number_input(label="", min_value=0, max_value=300, value=wegezeit, step=5)


# --- Schichtauswahl pro Tag ---
st.markdown("## Schichtauswahl pro Tag")
schicht_optionen = list(zeiten.keys()) + ["Frei"]
wochentage = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
for tag in range(1, anzahl_tage + 1):
    col1, col2 = st.columns([1, 6])
    # Wochentag berechnen
    wochentag_idx = datetime(jahr, monat, tag).weekday()  # 0=Mo, 6=So
    wochentag_abk = wochentage[wochentag_idx]
    with col1:
        st.markdown(f"<p style='text-align:center; margin-top: 2.3em;'>{tag:02d} - {wochentag_abk}</p>", unsafe_allow_html=True)
    with col2:
        tage[tag] = st.radio(
            label="",
            options=schicht_optionen,
            index=schicht_optionen.index(tage.get(tag, "Frei")),
            horizontal=True,
            key=f"schicht_{tag}"
        )

# Änderungen an 'tage' zurück in den Session State schreiben
st.session_state['tage'] = tage

# --- iCal-Export mit Wegezeit und Download ---
# kalender-funktionen sind jetzt in scheduler.py

if st.button("iCal-Datei erstellen und herunterladen"):
    cal = erstelle_kalender(monat, jahr, tage, wegezeit)
    ics_content = str(cal)
    st.download_button(
        label="Dienstplan als .ics herunterladen",
        data=ics_content,
        file_name="dienstplan.ics",
        mime="text/calendar"
    )
    
