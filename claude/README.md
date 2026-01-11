# Student Dropout Prediction

Machine Learning Pipeline und Web-Dashboard zur Vorhersage von Studienabbrüchen.

---

## 📁 Projektstruktur

```
claude/
├── web/                      # 🌐 React Web App (NEU)
│   ├── src/
│   │   ├── App.jsx          # Hauptkomponente
│   │   ├── index.css        # Premium Dark Theme
│   │   └── main.jsx         # Entry Point
│   ├── public/
│   │   └── result.json      # ML-Ergebnisse
│   └── package.json
│
├── first_version/            # 📦 Backup der alten Version
│   ├── index.html           # Standalone HTML
│   ├── result.json
│   └── WEB_DOCUMENTATION.md
│
├── dropout_prediction.py     # 🐍 ML-Pipeline
├── result.json              # ML-Ergebnisse
├── README.md                # Diese Datei
├── IMPLEMENTATION_PLAN.md   # ML-Technische Planung
├── WALKTHROUGH.md           # ML-Dokumentation
└── WEB_DOCUMENTATION.md     # Web-Dokumentation
```

---

## 🌐 Web-Dashboard (React)

### Starten

```bash
cd claude/web
npm install     # Einmalig: Dependencies installieren
npm run dev     # Development Server starten
```

**URL**: http://localhost:5173

### Features

| Feature | Beschreibung |
|---------|--------------|
| 📊 Metric Cards | Animierte Hauptmetriken mit Glow-Effekten |
| 📈 Confusion Matrix | Tabellarische + Chart Darstellung |
| 🎯 Per-Class Metrics | Progress-Bars mit Farbcodierung |
| 📉 Charts | Doughnut, Radar, Stacked Bar |
| 📖 Interpretation | Erklärungen für Nicht-ML-Experten |
| 🌙 Dark Theme | Premium Glassmorphism Design |

### Technologie-Stack

- **React 19** + Vite
- **Chart.js** + react-chartjs-2
- **Vanilla CSS** (kein Tailwind)

---

## 📦 Backup: Erste Version

Die ursprüngliche Standalone-HTML-Version ist im Ordner `first_version/` gespeichert.

### Ausführen der alten Version

```bash
cd claude/first_version
python -m http.server 8000
# Browser: http://localhost:8000
```

---

## 🐍 ML-Pipeline

### Ausführen

```bash
cd claude
python dropout_prediction.py
```

### Ergebnisse

`result.json` enthält:
- Macro F1: **0.7059**
- Weighted F1: **0.7649**
- Balanced Accuracy: **0.6996**
- Accuracy: **0.7695**

### Voraussetzungen

```bash
pip install pandas numpy scikit-learn
```

---

## 📊 Modell-Performance

| Klasse | Precision | Recall | F1-Score |
|--------|-----------|--------|----------|
| Dropout | 81.9% | 75.0% | 78.3% |
| Enrolled | 50.7% | 45.3% | 47.8% |
| Graduate | 82.0% | 89.6% | 85.6% |

---

## 🔧 Troubleshooting

### "Module not found" bei npm run dev

```bash
cd claude/web
npm install
```

### Port 5173 belegt

Vite wählt automatisch einen anderen Port (z.B. 5174).

### result.json nicht gefunden

Stelle sicher, dass `result.json` im `/web/public/` Ordner liegt.

---

## 👤 Autor

**Claude AI** - Erstellt am 2026-01-11
