"""
Student Dropout Prediction - Machine Learning Pipeline
=======================================================
Author: Claude AI
Date: 2026-01-11

This script implements a comprehensive ML pipeline for predicting student dropout.
Dataset: Predict Students' Dropout and Academic Success (UCI ML Repository)
"""

import pandas as pd
import numpy as np
import json
import time
from pathlib import Path

# Scikit-learn imports
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    f1_score, balanced_accuracy_score, accuracy_score,
    confusion_matrix, classification_report, precision_recall_fscore_support
)
from sklearn.pipeline import Pipeline

# Note: Using class_weight='balanced' instead of SMOTE for simplicity
# This avoids external dependency on imbalanced-learn

import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# Get the script directory and set paths relative to it
SCRIPT_DIR = Path(__file__).parent
DATA_PATH = SCRIPT_DIR.parent / "shared-data" / "data.csv"
OUTPUT_PATH = SCRIPT_DIR / "result.json"

# Random seed for reproducibility (as per requirements)
SPLIT_RANDOM_STATE = 42


def load_and_explore_data():
    """Load dataset and perform initial exploration."""
    print("=" * 60)
    print("LOADING AND EXPLORING DATA")
    print("=" * 60)
    
    # Load data - CSV uses semicolon separator
    df = pd.read_csv(DATA_PATH, sep=';')
    
    print(f"\nDataset Shape: {df.shape}")
    print(f"Total samples: {df.shape[0]}")
    print(f"Total features: {df.shape[1] - 1}")  # -1 for target
    
    # Check target distribution
    print("\n--- Target Distribution ---")
    target_counts = df['Target'].value_counts()
    print(target_counts)
    print(f"\nClass proportions:")
    print(target_counts / len(df) * 100)
    
    # Check for missing values
    print(f"\n--- Missing Values ---")
    missing = df.isnull().sum().sum()
    print(f"Total missing values: {missing}")
    
    return df


def preprocess_data(df):
    """
    Preprocess the dataset with encoding and feature engineering.
    
    Preprocessing Strategy:
    1. Encode target variable (Dropout, Enrolled, Graduate)
    2. All features are already numeric in this dataset
    3. Apply StandardScaler for numerical stability
    4. Create derived features based on domain knowledge
    """
    print("\n" + "=" * 60)
    print("PREPROCESSING DATA")
    print("=" * 60)
    
    # Separate features and target
    X = df.drop('Target', axis=1)
    y = df['Target']
    
    # Encode target variable
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    class_names = label_encoder.classes_
    print(f"\nTarget classes: {list(class_names)}")
    print(f"Encoded as: {list(range(len(class_names)))}")
    
    # ═══════════════════════════════════════════════════════════════
    # FEATURE ENGINEERING
    # ═══════════════════════════════════════════════════════════════
    print("\n--- Feature Engineering ---")
    
    # Create derived features based on domain knowledge
    X_engineered = X.copy()
    
    # 1. Academic performance features (1st semester)
    # Ratio of approved to enrolled units in 1st semester
    X_engineered['sem1_approval_rate'] = np.where(
        X['Curricular units 1st sem (enrolled)'] > 0,
        X['Curricular units 1st sem (approved)'] / X['Curricular units 1st sem (enrolled)'],
        0
    )
    
    # 2. Academic performance features (2nd semester)
    X_engineered['sem2_approval_rate'] = np.where(
        X['Curricular units 2nd sem (enrolled)'] > 0,
        X['Curricular units 2nd sem (approved)'] / X['Curricular units 2nd sem (enrolled)'],
        0
    )
    
    # 3. Combined academic performance
    total_enrolled = (X['Curricular units 1st sem (enrolled)'] + 
                      X['Curricular units 2nd sem (enrolled)'])
    total_approved = (X['Curricular units 1st sem (approved)'] + 
                      X['Curricular units 2nd sem (approved)'])
    X_engineered['total_approval_rate'] = np.where(
        total_enrolled > 0,
        total_approved / total_enrolled,
        0
    )
    
    # 4. Average grade across both semesters
    X_engineered['avg_grade'] = (
        X['Curricular units 1st sem (grade)'] + X['Curricular units 2nd sem (grade)']
    ) / 2
    
    # 5. Grade improvement (2nd sem vs 1st sem)
    X_engineered['grade_improvement'] = (
        X['Curricular units 2nd sem (grade)'] - X['Curricular units 1st sem (grade)']
    )
    
    # 6. Total credited units
    X_engineered['total_credited'] = (
        X['Curricular units 1st sem (credited)'] + X['Curricular units 2nd sem (credited)']
    )
    
    # 7. Evaluation efficiency (approved vs evaluations)
    total_evaluations = (X['Curricular units 1st sem (evaluations)'] + 
                         X['Curricular units 2nd sem (evaluations)'])
    X_engineered['evaluation_efficiency'] = np.where(
        total_evaluations > 0,
        total_approved / total_evaluations,
        0
    )
    
    # 8. Financial stress indicator (debtor and tuition status combined)
    X_engineered['financial_stress'] = X['Debtor'] + (1 - X['Tuition fees up to date'])
    
    # 9. Age when enrolled relative to typical (18-20)
    X_engineered['age_deviation'] = X['Age at enrollment'] - 19
    
    print(f"Original features: {X.shape[1]}")
    print(f"Engineered features added: {X_engineered.shape[1] - X.shape[1]}")
    print(f"Total features: {X_engineered.shape[1]}")
    
    return X_engineered, y_encoded, class_names, label_encoder


def train_model(X, y, class_names):
    """
    Train and optimize the ML model.
    
    Model Choice: Ensemble of RandomForest and GradientBoosting
    Rationale:
    - RandomForest: Good with mixed feature types, handles imbalance well
    - GradientBoosting: Strong performance on tabular data
    - Voting Ensemble: Combines strengths of both for better generalization
    
    Imbalance Handling: class_weight='balanced'
    Rationale: Dataset has imbalanced classes, class_weight adjusts weights
    inversely proportional to class frequencies.
    """
    print("\n" + "=" * 60)
    print("TRAINING MODEL")
    print("=" * 60)
    
    start_time = time.time()
    
    # ═══════════════════════════════════════════════════════════════
    # TRAIN/TEST SPLIT (AS PER REQUIREMENTS)
    # ═══════════════════════════════════════════════════════════════
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SPLIT_RANDOM_STATE, stratify=y
    )
    
    print(f"\nTrain set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    print(f"Train/Test split: 80/20")
    print(f"Random state: {SPLIT_RANDOM_STATE}")
    print(f"Stratified: Yes")
    
    # ═══════════════════════════════════════════════════════════════
    # CLASS IMBALANCE HANDLING
    # ═══════════════════════════════════════════════════════════════
    print("\n--- Handling Class Imbalance with class_weight='balanced' ---")
    print(f"Training set class distribution:")
    for i, name in enumerate(class_names):
        print(f"  {name}: {sum(y_train == i)}")
    print("\nUsing class_weight='balanced' in RandomForest to handle imbalance")
    
    # ═══════════════════════════════════════════════════════════════
    # SCALE FEATURES
    # ═══════════════════════════════════════════════════════════════
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # ═══════════════════════════════════════════════════════════════
    # MODEL DEFINITION
    # ═══════════════════════════════════════════════════════════════
    print("\n--- Model Selection ---")
    print("Using Voting Ensemble (RandomForest + GradientBoosting)")
    
    # Base classifiers with tuned hyperparameters
    rf_clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight='balanced',
        random_state=SPLIT_RANDOM_STATE,
        n_jobs=-1
    )
    
    gb_clf = GradientBoostingClassifier(
        n_estimators=150,
        max_depth=6,
        learning_rate=0.1,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=SPLIT_RANDOM_STATE
    )
    
    # Voting Ensemble
    ensemble = VotingClassifier(
        estimators=[
            ('rf', rf_clf),
            ('gb', gb_clf)
        ],
        voting='soft',  # Use probability averaging
        n_jobs=-1
    )
    
    print("\nTraining ensemble model...")
    ensemble.fit(X_train_scaled, y_train)
    
    training_time = time.time() - start_time
    print(f"Training completed in {training_time:.2f} seconds")
    
    return ensemble, scaler, X_test_scaled, y_test, training_time


def evaluate_model(model, X_test, y_test, class_names, training_time):
    """
    Evaluate the model and generate required outputs.
    
    Metrics (as per requirements):
    - Primary: Macro F1-Score
    - Secondary: Weighted F1, Balanced Accuracy, Accuracy
    """
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)
    
    # Get predictions
    y_pred = model.predict(X_test)
    
    # ═══════════════════════════════════════════════════════════════
    # COMPUTE REQUIRED METRICS
    # ═══════════════════════════════════════════════════════════════
    
    # Primary metric
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    
    # Secondary metrics
    weighted_f1 = f1_score(y_test, y_pred, average='weighted')
    balanced_acc = balanced_accuracy_score(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n===== EVALUATION RESULTS =====")
    print(f"Macro F1-Score:      {macro_f1:.4f}")
    print(f"Weighted F1-Score:   {weighted_f1:.4f}")
    print(f"Balanced Accuracy:   {balanced_acc:.4f}")
    print(f"Accuracy:            {accuracy:.4f}")
    
    # ═══════════════════════════════════════════════════════════════
    # CONFUSION MATRIX
    # ═══════════════════════════════════════════════════════════════
    cm = confusion_matrix(y_test, y_pred)
    
    print("\nConfusion Matrix:")
    # Header
    header = "             " + "  ".join([f"{name:>8}" for name in class_names])
    print(header)
    
    # Matrix rows
    for i, name in enumerate(class_names):
        row = f"{name:>12} " + "  ".join([f"{cm[i,j]:>8}" for j in range(len(class_names))])
        print(row)
    
    # ═══════════════════════════════════════════════════════════════
    # PER-CLASS METRICS
    # ═══════════════════════════════════════════════════════════════
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, y_pred, average=None
    )
    
    print("\nPer-Class Metrics:")
    print("             Precision  Recall  F1-Score  Support")
    for i, name in enumerate(class_names):
        print(f"{name:>12}     {precision[i]:.3f}   {recall[i]:.3f}     {f1[i]:.3f}      {support[i]}")
    
    print("=" * 30)
    
    # ═══════════════════════════════════════════════════════════════
    # PREPARE RESULTS FOR JSON
    # ═══════════════════════════════════════════════════════════════
    results = {
        "evaluation_metrics": {
            "macro_f1_score": round(macro_f1, 4),
            "weighted_f1_score": round(weighted_f1, 4),
            "balanced_accuracy": round(balanced_acc, 4),
            "accuracy": round(accuracy, 4)
        },
        "confusion_matrix": {
            "matrix": cm.tolist(),
            "labels": list(class_names)
        },
        "per_class_metrics": {
            name: {
                "precision": round(precision[i], 4),
                "recall": round(recall[i], 4),
                "f1_score": round(f1[i], 4),
                "support": int(support[i])
            }
            for i, name in enumerate(class_names)
        },
        "training_time_seconds": round(training_time, 2),
        "pipeline_documentation": {
            "initial_assumptions": [
                "Students with poor academic performance in early semesters are more likely to dropout",
                "Financial stress (debtor status, tuition fees) affects retention",
                "Age at enrollment may indicate non-traditional students with different risks",
                "Dataset has class imbalance that needs to be addressed"
            ],
            "preprocessing": {
                "encoding": "All features already numeric; Target encoded with LabelEncoder",
                "scaling": "StandardScaler applied for feature normalization",
                "missing_values": "No missing values in dataset"
            },
            "feature_engineering": {
                "created_features": [
                    "sem1_approval_rate - Ratio of approved/enrolled units in semester 1",
                    "sem2_approval_rate - Ratio of approved/enrolled units in semester 2", 
                    "total_approval_rate - Overall approval rate across both semesters",
                    "avg_grade - Average grade across both semesters",
                    "grade_improvement - Difference in grades between semesters",
                    "total_credited - Sum of credited units",
                    "evaluation_efficiency - Ratio of approved to evaluations",
                    "financial_stress - Combined debtor and tuition status indicator",
                    "age_deviation - Age at enrollment relative to typical age (19)"
                ],
                "rationale": "Academic performance features capture student engagement; financial features capture economic barriers"
            },
            "model": {
                "type": "Voting Ensemble (RandomForest + GradientBoosting)",
                "rationale": [
                    "RandomForest: Robust to outliers, handles mixed feature types well",
                    "GradientBoosting: Strong predictive performance on tabular data",
                    "Ensemble: Combines model strengths for better generalization"
                ]
            },
            "hyperparameters": {
                "RandomForest": {
                    "n_estimators": 200,
                    "max_depth": 15,
                    "min_samples_split": 5,
                    "min_samples_leaf": 2,
                    "class_weight": "balanced"
                },
                "GradientBoosting": {
                    "n_estimators": 150,
                    "max_depth": 6,
                    "learning_rate": 0.1,
                    "min_samples_split": 5,
                    "min_samples_leaf": 2
                },
                "Voting": "soft (probability averaging)"
            },
            "imbalance_handling": {
                "method": "class_weight='balanced' in RandomForest",
                "rationale": "Adjusts weights inversely proportional to class frequencies, penalizing misclassification of minority classes more heavily"
            },
            "rejected_alternatives": [
                "Logistic Regression - too simple for complex feature interactions",
                "Single Random Forest - ensemble performs better",
                "SMOTE - requires additional dependency (imbalanced-learn)",
                "Undersampling - would lose valuable training data"
            ]
        }
    }
    
    return results


def save_results(results):
    """Save results to JSON file."""
    print(f"\n--- Saving Results to {OUTPUT_PATH} ---")
    
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Results saved successfully!")


def main():
    """Main pipeline execution."""
    print("\n" + "=" * 60)
    print("STUDENT DROPOUT PREDICTION - ML PIPELINE")
    print("=" * 60)
    print("Author: Claude AI")
    print("Dataset: Predict Students' Dropout and Academic Success")
    print("=" * 60)
    
    # Step 1: Load and explore data
    df = load_and_explore_data()
    
    # Step 2: Preprocess data
    X, y, class_names, label_encoder = preprocess_data(df)
    
    # Step 3: Train model
    model, scaler, X_test, y_test, training_time = train_model(X, y, class_names)
    
    # Step 4: Evaluate model
    results = evaluate_model(model, X_test, y_test, class_names, training_time)
    
    # Step 5: Save results
    save_results(results)
    
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    main()
