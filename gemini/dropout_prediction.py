import pandas as pd
import numpy as np
import json
import time
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    confusion_matrix,
    classification_report
)

def run_pipeline():
    start_time = time.time()
    
    # 1. Load Dataset
    data_path = 'shared-data/data.csv'
    # The file uses semicolons as separators based on the preview
    df = pd.read_csv(data_path, sep=';')
    
    # 2. Preprocessing
    # Target Encoding
    le = LabelEncoder()
    df['Target'] = le.fit_transform(df['Target'])
    # Mapping for later: Dropout: 0, Enrolled: 1, Graduate: 2 (usually alphabetical)
    # Let's verify classes
    target_names = le.classes_
    
    X = df.drop('Target', axis=1)
    y = df['Target']
    
    # 3. Dataset Split (Strictly 80/20, Seed 42, Stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scaling numerical features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 4. Model Training & Tuning
    # Using Random Forest as it handles mixed feature types well and provides feature importance.
    rf = RandomForestClassifier(random_state=42)
    
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5]
    }
    
    grid_search = GridSearchCV(rf, param_grid, cv=3, scoring='f1_macro', n_jobs=-1)
    grid_search.fit(X_train_scaled, y_train)
    
    best_model = grid_search.best_estimator_
    
    # 5. Prediction & Evaluation
    y_pred = best_model.predict(X_test_scaled)
    
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    weighted_f1 = f1_score(y_test, y_pred, average='weighted')
    balanced_acc = balanced_accuracy_score(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=target_names, output_dict=True)
    
    end_time = time.time()
    training_time = end_time - start_time
    
    # Format results for terminal and JSON
    res_text = f"""===== EVALUATION RESULTS =====
Macro F1-Score:      {macro_f1:.4f}
Weighted F1-Score:   {weighted_f1:.4f}
Balanced Accuracy:   {balanced_acc:.4f}
Accuracy:            {acc:.4f}

Confusion Matrix:
             Dropout  Enrolled  Graduate
Dropout         {cm[0,0]:>3}      {cm[0,1]:>3}       {cm[0,2]:>3}
Enrolled        {cm[1,0]:>3}      {cm[1,1]:>3}       {cm[1,2]:>3}
Graduate        {cm[2,0]:>3}      {cm[2,1]:>3}       {cm[2,2]:>3}

Per-Class Metrics:
             Precision  Recall  F1-Score  Support
Dropout         {report['Dropout']['precision']:.3f}   {report['Dropout']['recall']:.3f}     {report['Dropout']['f1-score']:.3f}      {int(report['Dropout']['support'])}
Enrolled        {report['Enrolled']['precision']:.3f}   {report['Enrolled']['recall']:.3f}     {report['Enrolled']['f1-score']:.3f}      {int(report['Enrolled']['support'])}
Graduate        {report['Graduate']['precision']:.3f}   {report['Graduate']['recall']:.3f}     {report['Graduate']['f1-score']:.3f}      {int(report['Graduate']['support'])}
==============================

PIPELINE DOCUMENTATION:
- Initial Assumptions: The dataset is relatively clean but contains class imbalance (likely Graduate > Dropout > Enrolled). Feature scaling is necessary for some models, though RF is robust.
- Preprocessing: Standard numerical scaling, LabelEncoding for the target. Semicolon separator used for CSV reading.
- Feature Engineering: None in this initial version; relying on raw features and RF's inherent selection.
- Model: RandomForestClassifier. Chosen for its robustness to non-linear relationships and feature scaling, and ease of interpretability (importance).
- Hyperparameters: {grid_search.best_params_}
- Rejected Alternatives: Logistic Regression (might be too simple), SVM (scaling sensitive and slower to tune).
- Training Time: {training_time:.1f} seconds
"""
    print(res_text)
    
    # Save to result.json (per requirements)
    results_json = {
        "metrics": {
            "macro_f1": macro_f1,
            "weighted_f1": weighted_f1,
            "balanced_accuracy": balanced_acc,
            "accuracy": acc
        },
        "confusion_matrix": cm.tolist(),
        "classification_report": report,
        "training_time": training_time,
        "best_params": grid_search.best_params_
    }
    
    with open('gemini/result.json', 'w') as f:
        json.dump(results_json, f, indent=4)

if __name__ == "__main__":
    run_pipeline()
