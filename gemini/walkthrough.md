# Student Dropout Prediction Walkthrough

I have successfully developed and verified the student dropout prediction machine learning pipeline, strictly adhering to the requirements in `prompts/ML_prompt.ini`.

## Changes Made

### Gemini Component
- [dropout_prediction.py](file:///c:/Users/mathias/Desktop/OneDrive%20-%20Ferdinand%20Porsche%20FERNFH/DAT503%20AI%20assisted%20Engineering/ESA2/DAT503_ESA2/gemini/dropout_prediction.py): A comprehensive Python script that:
    - Loads the dataset from `shared-data/data.csv`.
    - Handles preprocessing (Target encoding, Numerical scaling).
    - Splits data (80/20, Seed 42, Stratified).
    - Optimizes a `RandomForestClassifier` using `GridSearchCV`.
    - Produces the required terminal output and saves comprehensive results to [result.json](file:///c:/Users/mathias/Desktop/OneDrive%20-%20Ferdinand%20Porsche%20FERNFH/DAT503%20AI%20assisted%20Engineering/ESA2/DAT503_ESA2/gemini/result.json).

## Verification Results

### Execution Output
The script was executed and produced the following metrics:

```text
===== EVALUATION RESULTS =====
Macro F1-Score:      0.6975
Weighted F1-Score:   0.7600
Balanced Accuracy:   0.6856
Accuracy:            0.7740

Confusion Matrix:
             Dropout  Enrolled  Graduate
Dropout         214       24        46
Enrolled         36       59        64
Graduate         12       18       412
...
```

### JSON Export
The results were correctly serialized to `gemini/result.json` with high precision.

### Pipeline Documentation Summary
- **Model**: RandomForestClassifier (Best Params: `n_estimators=200`, `min_samples_split=5`).
- **Training Time**: ~12 seconds.
- **Preprocessing**: Used Standard Scaling and Label Encoding for the target variable.
