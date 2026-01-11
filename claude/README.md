# Student Dropout Prediction - README

## Beschreibung

Machine Learning Pipeline zur Vorhersage von Studienabbrüchen basierend auf dem UCI ML Repository Dataset "Predict Students' Dropout and Academic Success". Inklusive Web-Dashboard zur Visualisierung der Ergebnisse.

---

## Projektstruktur

```
claude/
├── dropout_prediction.py    # ML-Pipeline Script
├── result.json              # Evaluierungsergebnisse
├── index.html               # Web-Dashboard (Single Page)
├── README.md                # Diese Datei
├── IMPLEMENTATION_PLAN.md   # Technischer Plan (ML)
├── WALKTHROUGH.md           # Detaillierte ML-Erklärung
└── WEB_DOCUMENTATION.md     # Web-Frontend Dokumentation

shared-data/
└── data.csv                 # Dataset
```

---

## 🚀 Schnellstart

### Option 1: ML-Script ausführen

```bash
cd claude
python dropout_prediction.py
```

### Option 2: Web-Dashboard starten

**Methode A: Mit Python Server (empfohlen)**
```bash
cd claude
python -m http.server 8000
```
Dann im Browser öffnen: **http://localhost:8000**

**Methode B: Mit Node.js Server**
```bash
cd claude
npx serve .
```

**Methode C: VS Code Live Server**
1. VS Code Extension "Live Server" installieren
2. Rechtsklick auf `index.html` → "Open with Live Server"

> ⚠️ **Wichtig**: Das direkte Öffnen der HTML-Datei im Browser funktioniert aufgrund von CORS-Einschränkungen beim Laden von `result.json` nicht. Ein lokaler Server ist erforderlich.

---

## Voraussetzungen

### Für ML-Script
- Python 3.8+
- pandas, numpy, scikit-learn

```bash
pip install pandas numpy scikit-learn
```

### Für Web-Dashboard
- Nur ein moderner Webbrowser
- Lokaler HTTP-Server (Python, Node.js, oder VS Code)

---

## ML-Pipeline Details

### Ausführung

```bash
python dropout_prediction.py
```

### Erwartete Ausgabe

```
============================================================
STUDENT DROPOUT PREDICTION - ML PIPELINE
============================================================
...
===== EVALUATION RESULTS =====
Macro F1-Score:      0.7059
Weighted F1-Score:   0.7649
Balanced Accuracy:   0.6996
Accuracy:            0.7695
...
PIPELINE COMPLETED SUCCESSFULLY
============================================================
```

### Generierte Datei

`result.json` enthält:
- Evaluation Metrics (Macro F1, Weighted F1, Balanced Accuracy, Accuracy)
- Confusion Matrix (3x3 für Dropout, Enrolled, Graduate)
- Per-Class Metrics (Precision, Recall, F1-Score, Support)
- Pipeline Documentation (Feature Engineering, Model, Hyperparameters)

---

## Web-Dashboard Details

### Features

| Feature | Beschreibung |
|---------|--------------|
| 📊 Metric Cards | Globale Metriken mit animierten Werten |
| 📈 Confusion Matrix | Tabellarische + grafische Darstellung |
| 🎯 Per-Class Metrics | Tabelle mit Progress-Bars |
| 📉 Charts | Doughnut (F1), Radar (PR), Stacked Bar |
| 📖 Interpretation | Erklärungen für Nicht-ML-Experten |

### Technologien

- **HTML5 + CSS3**: Modernes Dark-Theme Layout
- **JavaScript (Vanilla)**: Keine Frameworks, keine Build-Tools
- **Chart.js**: Interaktive Visualisierungen
- **Google Fonts (Inter)**: Moderne Typografie

### Screenshots

Das Dashboard zeigt:

1. **Header**: Titel und Beschreibung
2. **Metric Cards**: Die 4 Hauptmetriken als große Karten
3. **Confusion Matrix**: Links Tabelle, rechts Stacked Bar Chart
4. **Per-Class Table**: Precision, Recall, F1 mit farbigen Progress-Bars
5. **Charts**: F1 Doughnut + Precision/Recall Radar
6. **Interpretation**: Hilfe für Nicht-Experten

---

## Fehlerbehebung

### "Failed to load result.json"

**Problem**: Browser blockiert lokale Dateizugriffe (CORS)

**Lösung**: Lokalen Server starten:
```bash
python -m http.server 8000
```

### ModuleNotFoundError (Python)

```bash
pip install pandas numpy scikit-learn
```

### result.json nicht gefunden

Stelle sicher, dass `result.json` im selben Ordner wie `index.html` liegt.

---

## Autor

**Claude AI** - Generiert am 2026-01-11

## Lizenz

Dieses Projekt wurde für Bildungszwecke erstellt.
