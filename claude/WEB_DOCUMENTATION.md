# Web-Frontend Dokumentation (React Version)

## Aufbau der Seite

Das Dashboard ist als **React Single Page Application** mit Vite aufgebaut:

```
┌─────────────────────────────────────────────────────────────┐
│                         HEADER                               │
│        🎓 Student Dropout Prediction Dashboard              │
│            "Powered by ML Analytics" Badge                  │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ 🎯       │ │ ⚖️       │ │ 📈       │ │ ✅       │       │
│  │ Macro F1 │ │Weighted  │ │ Balanced │ │ Accuracy │       │
│  │  70.6%   │ │   F1     │ │ Accuracy │ │  77.0%   │       │
│  │          │ │  76.5%   │ │  70.0%   │ │          │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
├───────────────────────┬─────────────────────────────────────┤
│   📊 Confusion Matrix │      📈 Predictions Distribution    │
│   (Tabelle)           │      (Stacked Bar Chart)            │
├───────────────────────┴─────────────────────────────────────┤
│            🎯 Per-Class Performance Metrics                  │
│   Mit Progress-Bars und Farbcodierung                       │
├───────────────────────┬─────────────────────────────────────┤
│   📉 F1-Score         │     ⚖️ Precision vs Recall          │
│   (Doughnut Chart)    │     (Radar Chart)                   │
├───────────────────────┴─────────────────────────────────────┤
│                    📖 INTERPRETATION                         │
│   Erklärungen mit Icons für Nicht-ML-Experten              │
└─────────────────────────────────────────────────────────────┘
```

---

## Technologie-Stack

| Technologie | Version | Zweck |
|-------------|---------|-------|
| React | 19 | UI-Komponenten |
| Vite | 5.4.0 | Build Tool & Dev Server |
| Chart.js | 4.x | Visualisierungen |
| react-chartjs-2 | 5.x | React-Wrapper für Chart.js |
| Vanilla CSS | - | Premium Dark Theme |

---

## Komponenten-Struktur

```jsx
App
├── Header              // Titel + Badge
├── MetricsSection      // 4 MetricCards
│   └── MetricCard      // Einzelne Metrik-Karte
├── Dashboard Grid
│   ├── ConfusionMatrix // Tabelle
│   └── PredictionsChart // Stacked Bar
├── PerClassMetrics     // Tabelle mit Progress-Bars
├── Charts Grid
│   ├── F1DoughnutChart // Doughnut
│   └── RadarChart      // Radar
├── InterpretationCard  // Erklärungen
└── Footer
```

---

## Lokale Startanleitung

### Voraussetzungen

- Node.js (v18+)
- npm

### Installation & Start

```bash
# In den richtigen Ordner wechseln
cd claude/web

# Dependencies installieren (einmalig)
npm install

# Development Server starten
npm run dev
```

**URL**: http://localhost:5173

### Build für Produktion

```bash
npm run build
npm run preview
```

---

## Design-Entscheidungen

### Dark Theme mit Glassmorphism

- Moderne, professionelle Ästhetik
- Reduzierte Augenbelastung
- Gradient-Akzente für visuelles Interesse
- Backdrop-Filter für Tiefe

### Farbcodierung

| Farbe | Klasse | Bedeutung |
|-------|--------|-----------|
| 🔴 Rot | Dropout | Gefährdete Studenten |
| 🟡 Gelb | Enrolled | Noch eingeschrieben |
| 🟢 Grün | Graduate | Erfolgreich abgeschlossen |

### Animationen

- `fadeInUp` für gestaffeltes Laden der Karten
- Hover-Effekte mit Transform und Glow
- Smooth Transitions (250ms ease)

---

## Datenfluss

```
result.json (public/)
       ↓
   fetch() in useEffect
       ↓
   useState(data)
       ↓
   Props an Komponenten
       ↓
   Chart.js Rendering
```

---

## Responsive Design

| Breakpoint | Layout |
|------------|--------|
| > 1200px | 4 Metriken nebeneinander, 2-Spalten Grid |
| 768-1200px | 2x2 Metriken, 2-Spalten Grid |
| < 768px | Alle Karten untereinander |

---

## Vergleich: Alte vs. Neue Version

| Feature | HTML (first_version) | React (web) |
|---------|---------------------|-------------|
| Framework | Vanilla JS | React 19 |
| Build Tool | Keines | Vite |
| Modularität | Single File | Komponenten |
| Styling | Inline CSS | Separate CSS |
| Animationen | Basis | Erweitert |
| Wartbarkeit | Mittel | Hoch |
| Performance | Gut | Sehr gut (HMR) |
