Dieses Projekt erstellt einen iCal-Dienstplan aus einer Streamlit-Oberfläche.

Vorgehen:

1. Virtuelle Umgebung aktivieren (falls vorhanden):

   source .venv/bin/activate

2. Abhängigkeiten installieren:

   pip install -r requirements.txt

3. App starten:

   streamlit run main.py

4. Tests ausführen:

   python -m tests.run_tests

Hinweis: Die iCal-Erzeugung verwendet `ZoneInfo("Europe/Berlin")` für lokale Zeiten.
