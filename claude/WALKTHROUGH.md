# Walkthrough - Student Dropout Prediction ML Pipeline

## Überblick

Dieses Dokument beschreibt die entwickelte Machine Learning Pipeline zur Vorhersage von Studienabbrüchen (Student Dropout Prediction).

---

## Dateien

| Datei | Beschreibung |
|-------|--------------|
| `dropout_prediction.py` | Haupt-Python-Script mit ML-Pipeline |
| `result.json` | Evaluierungsergebnisse im JSON-Format |
| `README.md` | Anleitung zur Ausführung |
| `IMPLEMENTATION_PLAN.md` | Technischer Implementierungsplan |

---

## Dataset

- **Quelle**: UCI ML Repository - "Predict Students' Dropout and Academic Success"
- **Dokumentation**: https://archive.ics.uci.edu/dataset/697
- **Samples**: 4,424 Studenten
- **Features**: 36 Original-Features (Demografisch, Akademisch, Sozioökonomisch)
- **Zielklassen**: 
  - Dropout (Studienabbruch): 32.1%
  - Enrolled (Noch eingeschrieben): 17.9%
  - Graduate (Abgeschlossen): 49.9%

---

## Pipeline-Schritte

### 1. Daten laden und explorieren

```python
df = pd.read_csv(DATA_PATH, sep=';')
```

- Überprüfung der Datenstruktur
- Analyse der Klassenverteilung
- Check auf fehlende Werte (keine vorhanden)

### 2. Feature Engineering

**9 neue Features** wurden basierend auf Domänenwissen erstellt:

| Feature | Formel | Zweck |
|---------|--------|-------|
| `sem1_approval_rate` | approved / enrolled (Sem 1) | Frühe akademische Performance |
| `sem2_approval_rate` | approved / enrolled (Sem 2) | Akademische Entwicklung |
| `total_approval_rate` | gesamt approved / gesamt enrolled | Gesamtperformance |
| `avg_grade` | (grade Sem1 + grade Sem2) / 2 | Durchschnittliche Leistung |
| `grade_improvement` | grade Sem2 - grade Sem1 | Leistungstrend |
| `total_credited` | credited Sem1 + credited Sem2 | Vorleistungen |
| `evaluation_efficiency` | approved / evaluations | Prüfungseffizienz |
| `financial_stress` | debtor + (1 - tuition_up_to_date) | Finanzielle Belastung |
| `age_deviation` | age - 19 | Abweichung vom typischen Alter |

**Ergebnis**: 45 Features (36 original + 9 engineered)

### 3. Train/Test Split

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

- **Training**: 3,539 Samples (80%)
- **Test**: 885 Samples (20%)
- **Stratified**: Ja (gleiche Klassenverteilung)

### 4. Modell-Training

**Voting Ensemble** mit zwei Base Classifiern:

```
┌─────────────────────────────────────────┐
│           Voting Classifier             │
│            (Soft Voting)                │
├────────────────────┬────────────────────┤
│   RandomForest     │  GradientBoosting  │
│   n_estimators=200 │  n_estimators=150  │
│   max_depth=15     │  max_depth=6       │
│   class_weight=    │  learning_rate=0.1 │
│     'balanced'     │                    │
└────────────────────┴────────────────────┘
```

**Training Time**: 9.62 Sekunden

### 5. Evaluation

---

## Ergebnisse

### Hauptmetriken

| Metrik | Score |
|--------|-------|
| **Macro F1-Score** (Primary) | **0.7059** |
| Weighted F1-Score | 0.7649 |
| Balanced Accuracy | 0.6996 |
| Accuracy | 0.7695 |

### Confusion Matrix

```
             Dropout  Enrolled  Graduate
Dropout         213        37        34
Enrolled         34        72        53
Graduate         13        33       396
```

**Interpretation**:
- **Dropout**: 75% korrekt erkannt (213/284)
- **Enrolled**: 45% korrekt erkannt (72/159) - schwächste Klasse
- **Graduate**: 90% korrekt erkannt (396/442) - stärkste Klasse

### Per-Class Metrics

| Klasse | Precision | Recall | F1-Score | Support |
|--------|-----------|--------|----------|---------|
| Dropout | 0.819 | 0.750 | 0.783 | 284 |
| Enrolled | 0.507 | 0.453 | 0.478 | 159 |
| Graduate | 0.820 | 0.896 | 0.856 | 442 |

---

## Key Insights

### Warum ist "Enrolled" schwächer?

1. **Kleinste Klasse** (nur 17.9% der Daten)
2. **Übergangsklasse** zwischen Dropout und Graduate
3. Studenten können noch in beide Richtungen wechseln

### Wichtigste Einflussfaktoren

Basierend auf der Feature-Importance (implizit durch das Modell):

1. **Akademische Performance** (Approval Rates, Grades)
2. **Finanzielle Situation** (Debtor, Tuition Status)
3. **Alter bei Einschreibung** (Non-traditional Students)

---

## Mögliche Verbesserungen

1. **SMOTE** für bessere Minority-Class-Repräsentation (benötigt `imbalanced-learn`)
2. **Hyperparameter-Tuning** mit GridSearchCV oder RandomizedSearchCV
3. **Feature Selection** zur Reduktion von Noise
4. **XGBoost/LightGBM** als Alternative zu GradientBoosting
