# Startanleitung für das Dropout Prediction Dashboard

Dieses Dashboard ermöglicht eine interaktive Visualisierung der Machine-Learning-Ergebnisse.

## Voraussetzungen
- Ein moderner Webbrowser (Chrome, Firefox, Edge, Safari).
- Die Datei `result.json` muss im gleichen Verzeichnis wie `index.html` vorhanden sein (wurde durch den ML-Lauf generiert).

## Startoptionen

### Option 1: Direktes Öffnen (Empfohlen für schnellen Check)
1. Navigieren Sie in Ihrem Dateimanager zum Ordner `gemini/`.
2. Doppelklicken Sie auf die Datei `index.html`.
3. Da Browser das automatische Laden lokaler Dateien aus Sicherheitsgründen oft blockieren (CORS), klicken Sie oben rechts auf den Button **"Upload result.json"**.
4. Wählen Sie die Datei `result.json` aus dem gleichen Ordner aus.

### Option 2: Über einen lokalen Server (Volle Funktionalität)
Wenn Sie einen lokalen Server starten, wird die Datei automatisch geladen:

**Mit Python:**
```bash
# Im Projekt-Root oder /gemini Ordner:
python -m http.server 8000
```
Öffnen Sie dann `http://localhost:8000/gemini/index.html` (oder direkt, falls im Ordner gestartet).

**Mit Node.js / npm:**
```bash
npx serve gemini
```

## Übersicht der Visualisierungen
- **Global Metrics**: Zeigt Accuracy, F1-Scores und Balanced Accuracy auf einen Blick.
- **Per-Class Performance**: Ein Balkendiagramm vergleicht Precision, Recall und F1-Score für die drei Klassen (Dropout, Enrolled, Graduate). So lässt sich schnell erkennen, welche Klasse das Modell am besten erkennt.
- **Confusion Matrix**: Eine tabellarische Darstellung der Fehlklassifikationen, um zu sehen, welche Klassen am häufigsten verwechselt wurden.
- **Pipeline Summary**: Zusammenfassung der Trainingszeit und der optimierten Hyperparameter.
