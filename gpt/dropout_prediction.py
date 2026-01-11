import json
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    f1_score,
    balanced_accuracy_score,
    accuracy_score,
    confusion_matrix,
    classification_report,
)

# Paths (relative to project root)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "shared-data" / "data.csv"
RESULT_PATH = Path(__file__).resolve().parent / "result.json"

# Load dataset
df = pd.read_csv(DATA_PATH)

# Assume the target column is named 'target' or the last column if not specified
if "target" in df.columns:
    y = df["target"]
    X = df.drop(columns=["target"])
else:
    y = df.iloc[:, -1]
    X = df.iloc[:, :-1]

# Train‑test split (80/20, stratified, seed 42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Identify categorical and numeric columns
categorical_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()
numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

# Pre‑processing pipelines
preprocess = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
    ]
)

# Model – Random Forest (default hyper‑parameters, can be tuned later)
model = RandomForestClassifier(random_state=42)

# Full pipeline
pipeline = Pipeline(steps=[("preprocess", preprocess), ("model", model)])

# Train
pipeline.fit(X_train, y_train)

# Predict
y_pred = pipeline.predict(X_test)

# Evaluation metrics
macro_f1 = f1_score(y_test, y_pred, average="macro")
weighted_f1 = f1_score(y_test, y_pred, average="weighted")
bal_acc = balanced_accuracy_score(y_test, y_pred)
acc = accuracy_score(y_test, y_pred)

# Confusion matrix (as list of lists for JSON serialisation)
conf_mat = confusion_matrix(y_test, y_pred).tolist()

# Per‑class metrics (precision, recall, f1, support)
report = classification_report(y_test, y_pred, output_dict=True)
per_class_metrics = {
    cls: {
        "precision": vals["precision"],
        "recall": vals["recall"],
        "f1_score": vals["f1-score"],
        "support": int(vals["support"]),
    }
    for cls, vals in report.items()
    if cls not in ["accuracy", "macro avg", "weighted avg"]
}

# Pipeline documentation (place‑holders – can be filled manually later)
pipeline_documentation = {
    "initial_assumptions": "[Welche Annahmen hattest du zu Beginn?]",
    "preprocessing": "[Beschreibe deine Encoding‑Strategie]",
    "feature_engineering": "[Welche Features hast du erstellt?]",
    "model": "RandomForestClassifier (default parameters)",
    "hyperparameters": "[Wichtigste Parameter]",
    "rejected_alternatives": "[Welche Ansätze hast du bewusst nicht gewählt?]",
    "training_time_seconds": "[XX.X]",
}

# Assemble final result
result = {
    "macro_f1": macro_f1,
    "weighted_f1": weighted_f1,
    "balanced_accuracy": bal_acc,
    "accuracy": acc,
    "confusion_matrix": conf_mat,
    "per_class_metrics": per_class_metrics,
    "pipeline_documentation": pipeline_documentation,
}

# Write JSON output
with open(RESULT_PATH, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

print(f"Result written to {RESULT_PATH}")
