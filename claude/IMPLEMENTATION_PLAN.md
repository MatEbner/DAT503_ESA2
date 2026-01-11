# Implementation Plan - Student Dropout Prediction

## Ziel

Entwicklung eines Machine Learning Klassifikations-Modells zur Vorhersage von Student Dropout basierend auf dem UCI ML Repository Dataset "Predict Students' Dropout and Academic Success".

---

## Vorgaben (strikt eingehalten)

| Vorgabe | Umsetzung |
|---------|-----------|
| Train/Test Split | 80/20 |
| Random Seed | 42 |
| Stratified Split | ✓ `stratify=y` |
| Primary Metric | Macro F1-Score |
| Secondary Metrics | Weighted F1, Balanced Accuracy, Accuracy |

---

## Proposed Changes

### Datenanalyse

- **Dataset**: 4,424 Studenten, 36 Features
- **Zielklassen**: Dropout (32.1%), Enrolled (17.9%), Graduate (49.9%)
- **Missing Values**: Keine
- **Feature-Typen**: Numerisch (Integer, Float)

### Preprocessing-Strategie

1. **Encoding**: Target-Variable mit LabelEncoder (Dropout=0, Enrolled=1, Graduate=2)
2. **Scaling**: StandardScaler für alle Features
3. **Missing Values**: Keine Behandlung nötig

### Feature Engineering

| Feature | Beschreibung | Rationale |
|---------|--------------|-----------|
| `sem1_approval_rate` | Approved/Enrolled Ratio Sem 1 | Früherkennung akademischer Probleme |
| `sem2_approval_rate` | Approved/Enrolled Ratio Sem 2 | Akademische Entwicklung |
| `total_approval_rate` | Gesamte Approval Rate | Gesamtperformance |
| `avg_grade` | Durchschnittsnote beider Semester | Akademische Leistung |
| `grade_improvement` | Notenverbesserung Sem 2 vs Sem 1 | Entwicklungstrend |
| `total_credited` | Summe angerechneter Kurse | Vorleistungen |
| `evaluation_efficiency` | Approved/Evaluations Ratio | Prüfungseffizienz |
| `financial_stress` | Debtor + Tuition Status | Finanzielle Belastung |
| `age_deviation` | Alter relativ zu 19 Jahren | Non-traditional Students |

### Modell-Wahl

**Voting Ensemble (RandomForest + GradientBoosting)**

**Begründung:**
- RandomForest: Robust gegenüber Ausreißern, gut mit gemischten Features
- GradientBoosting: Starke Performance auf tabellarischen Daten
- Ensemble: Kombiniert Stärken beider Modelle

### Hyperparameter

```python
RandomForest:
  n_estimators: 200
  max_depth: 15
  min_samples_split: 5
  min_samples_leaf: 2
  class_weight: 'balanced'

GradientBoosting:
  n_estimators: 150
  max_depth: 6
  learning_rate: 0.1
  min_samples_split: 5
  min_samples_leaf: 2

Voting: 'soft' (Probability Averaging)
```

### Imbalance-Handling

**Methode**: `class_weight='balanced'` in RandomForest

**Begründung**: 
- Keine externe Dependency nötig
- Gewichtet Minority-Klassen proportional höher
- Vermeidet Overfitting durch synthetische Samples

### Rejected Alternatives

| Alternative | Grund für Ablehnung |
|-------------|---------------------|
| Logistic Regression | Zu simpel für komplexe Feature-Interaktionen |
| Single Random Forest | Ensemble performt besser |
| SMOTE | Benötigt externe Dependency (imbalanced-learn) |
| Undersampling | Verlust wertvoller Trainingsdaten |

---

## Verification Plan

### Automatisierte Tests

```bash
# Script ausführen
python dropout_prediction.py

# Überprüfen der Ausgabe
# - result.json wird generiert
# - Alle 4 Metriken werden berechnet
# - Confusion Matrix wird ausgegeben
```

### Erwartete Ergebnisse

- Macro F1-Score > 0.65 (erreicht: 0.7059)
- Alle Klassen werden erkannt
- Training Time < 60 Sekunden
