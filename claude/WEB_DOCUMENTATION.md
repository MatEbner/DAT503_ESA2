# Web-Frontend Dokumentation

## Aufbau der Seite

Das Dashboard ist als **Single Page Application (SPA)** aufgebaut mit folgenden Sektionen:

```
┌─────────────────────────────────────────────────────────────┐
│                         HEADER                               │
│        🎓 Student Dropout Prediction Dashboard              │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Macro F1 │ │Weighted  │ │ Balanced │ │ Accuracy │       │
│  │  70.6%   │ │   F1     │ │ Accuracy │ │  76.9%   │       │
│  │          │ │  76.5%   │ │  70.0%   │ │          │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
├───────────────────────┬─────────────────────────────────────┤
│   Confusion Matrix    │      Predictions Distribution       │
│   (Tabelle)           │      (Stacked Bar Chart)            │
├───────────────────────┴─────────────────────────────────────┤
│            Per-Class Performance Metrics                     │
│   Class      Precision    Recall    F1-Score    Support     │
│   Dropout    ████ 81.9%   ███ 75%   ████ 78.3%    284       │
│   Enrolled   ██ 50.7%     ██ 45.3%  ██ 47.8%      159       │
│   Graduate   ████ 82.0%   ████ 90%  ████ 85.6%    442       │
├───────────────────────┬─────────────────────────────────────┤
│   F1-Score by Class   │     Precision vs Recall             │
│   (Doughnut Chart)    │     (Radar Chart)                   │
├───────────────────────┴─────────────────────────────────────┤
│                    INTERPRETATION                            │
│   💡 Erklärungen für Nicht-ML-Experten                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Verwendete Visualisierungen

### 1. Metric Cards (Globale Metriken)

**Typ**: Große Karten mit animierten Werten

**Warum**: 
- Sofortiger Überblick über die wichtigsten Kennzahlen
- Visuelles Farbschema zeigt Performance-Level
- Gradient-Effekte für modernes Erscheinungsbild

### 2. Confusion Matrix (Tabelle)

**Typ**: HTML-Tabelle mit farblicher Hervorhebung

**Warum**:
- Klassische ML-Darstellung, die Experten kennen
- Diagonale grün hervorgehoben = korrekte Vorhersagen
- Einfach zu lesen und zu interpretieren

### 3. Predictions Distribution (Stacked Bar Chart)

**Typ**: Gestapeltes Balkendiagramm (Chart.js)

**Warum**:
- Zeigt Verhältnis von korrekten zu falschen Vorhersagen
- Intuitive visuelle Darstellung der Confusion Matrix
- Grün = richtig, Rot = falsch

### 4. Per-Class Metrics (Tabelle mit Progress Bars)

**Typ**: Tabelle mit visuellen Fortschrittsbalken

**Warum**:
- Schneller visueller Vergleich zwischen Klassen
- Farbcodierung: Grün (>70%), Gelb (50-70%), Rot (<50%)
- Support-Spalte zeigt Klassengrößen

### 5. F1-Score by Class (Doughnut Chart)

**Typ**: Ringdiagramm

**Warum**:
- Zeigt F1-Score-Verteilung auf einen Blick
- Farben korrespondieren mit Klassentypen
- Gut für Vergleich der relativen Performance

### 6. Precision vs Recall (Radar Chart)

**Typ**: Radar/Spider-Diagramm

**Warum**:
- Multidimensionale Metrik-Darstellung
- Zeigt Trade-offs zwischen Precision und Recall
- Überlappende Klassen gut sichtbar

---

## Interpretation für Nutzer

### Was bedeuten die Metriken?

| Metrik | Bedeutung | Guter Wert |
|--------|-----------|------------|
| **Macro F1-Score** | Durchschnittliche Balance zwischen Precision & Recall | > 0.70 |
| **Weighted F1** | Gewichteter Durchschnitt nach Klassengröße | > 0.75 |
| **Balanced Accuracy** | Accuracy korrigiert für Klassenungleichgewicht | > 0.65 |
| **Accuracy** | Anteil korrekter Vorhersagen insgesamt | > 0.75 |

### Was sagt die Confusion Matrix?

```
              Predicted
              Dropout  Enrolled  Graduate
Actual
Dropout         213       37        34      ← 75% richtig erkannt
Enrolled         34       72        53      ← 45% richtig erkannt  
Graduate         13       33       396      ← 90% richtig erkannt
```

**Interpretation**:
- Hohe Werte auf der Diagonale = gute Vorhersagen
- Werte außerhalb der Diagonale = Fehler
- Beispiel: 37 Dropout-Studenten wurden fälschlich als "Enrolled" vorhergesagt

### Warum ist "Enrolled" schwächer?

1. **Kleinste Klasse** (nur 17.9% der Daten)
2. **Übergangsphase** - Studenten können noch in beide Richtungen gehen
3. **Inhärent schwer vorherzusagen** ohne zeitliche Daten

---

## Technische Details

### Verwendete Bibliotheken

| Bibliothek | Version | Zweck |
|------------|---------|-------|
| Chart.js | 4.4.1 | Interaktive Charts |
| Google Fonts (Inter) | - | Moderne Typografie |

### Keine Build-Tools nötig

- Reines HTML/CSS/JavaScript
- CDN-basierte Bibliotheken
- Kein npm, webpack, oder ähnliches

### Datenfluss

```
result.json → fetch() → JavaScript → DOM Rendering + Chart.js
```

---

## Lokale Startanleitung

### Empfohlene Methode: Python HTTP Server

```bash
# Terminal öffnen
cd claude

# Server starten
python -m http.server 8000

# Browser öffnen
# http://localhost:8000
```

### Alternative: Node.js

```bash
npx serve .
```

---

## Responsive Design

Das Dashboard ist für folgende Bildschirmgrößen optimiert:

| Breakpoint | Layout |
|------------|--------|
| > 1400px | 4 Metric Cards nebeneinander |
| 768px - 1400px | 2x2 Grid für Cards |
| < 768px | Mobile-optimiert, Cards untereinander |
