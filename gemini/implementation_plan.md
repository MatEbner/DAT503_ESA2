# Student Dropout Prediction Implementation Plan

This plan outlines the steps to develop a classification model for student dropout prediction, adhering to the strict requirements provided in `prompts/ML_prompt.ini`.

## Proposed Changes

### Gemini Component

#### [NEW] [dropout_prediction.py](file:///c:/Users/mathias/Desktop/OneDrive%20-%20Ferdinand%20Porsche%20FERNFH/DAT503%20AI%20assisted%20Engineering/ESA2/DAT503_ESA2/gemini/dropout_prediction.py)
This script will:
- Load `shared-data/data.csv`.
- Preprocess data:
    - Encode the target variable (`Dropout`, `Enrolled`, `Graduate`).
    - Standardize/Scale numerical features.
- Split data into 80% training and 20% testing using `random_state=42` and `stratify=y`.
- Train a `RandomForestClassifier` (or similar high-performance model).
- Perform hyperparameter tuning using `GridSearchCV`.
- Evaluate the model using Macro F1, Weighted F1, Balanced Accuracy, and Accuracy.
- Print results in the specified format.
- Save results to `gemini/result.json`.
- Include full pipeline documentation.

## Verification Plan

### Automated Tests
- Run `python gemini/dropout_prediction.py` and verify:
    - Success execution without errors.
    - Generation of `gemini/result.json`.
    - Output matches the required format.

### Manual Verification
- Check the `result.json` content for correctness and consistency with the printed output.
