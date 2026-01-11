# Student Dropout Prediction Project

Dieses Projekt bietet eine Machine-Learning-Pipeline zur Vorhersage von Studienabbrüchen sowie zwei verschiedene Web-Dashboards zur Visualisierung der Ergebnisse.

## 1. Machine Learning Pipeline (Python)
Die Pipeline führt die Datenvorverarbeitung, das Modelltraining (Random Forest) und die umfassende Evaluation durch.

### Ausführung
Wechseln Sie in den Ordner `/gemini` und führen Sie das Skript aus:
```bash
python dropout_prediction.py
```
*Das Skript generiert die Datei `public/result.json` für die React-App und spiegelt diese nach `first_version/result.json`.*

## 2. Start React Dashboard (Hauptversion)
Eine moderne, interaktive Single Page Application mit Framer Motion, Lucide-Icons und Chart.js.

### Installation
Stellen Sie sicher, dass Sie im Ordner `/gemini` sind:
```bash
npm install
```

### Starten
```bash
npm run dev
```
Öffnen Sie anschließend [http://localhost:5173](http://localhost:5173). Die Daten werden automatisch geladen.

## 3. Start first_version
Die ursprüngliche, statische HTML-Version. Ideal für einen schnellen Überblick ohne Node.js-Abhängigkeiten.

### Ausführung
Navigieren Sie in den Ordner `/gemini/first_version`.

**Option A: Direktes Öffnen**
1. Doppelklicken Sie auf die Datei `index.html` in Ihrem Browser.
2. Da Browser das automatische Laden lokaler Dateien oft blockieren (CORS), klicken Sie oben rechts auf den Button **"Upload result.json"**.
3. Wählen Sie die Datei `result.json` aus demselben Ordner aus.

**Option B: Lokaler Server (Python)**
```bash
# Im Ordner /gemini/first_version ausführen:
python -m http.server 8000
```
Öffnen Sie anschließend [http://localhost:8000](http://localhost:8000). Die Daten werden hier automatisch geladen.

## Technische Details
- **Modell**: RandomForestClassifier (optimiert via GridSearchCV)
- **Frontend**: React 19, Vite 5, Chart.js, Framer Motion
- **Struktur**: 
    - `/src`: React Quellcode
    - `/public`: Statische Assets & ML-Ergebnisse
    - `/first_version`: Statische Fallback-Version
    - `dropout_prediction.py`: ML-Pipeline
