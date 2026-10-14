import pandas as pd
import joblib

from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

import time


# ==========================================================
# CyberGuard AI
# Step 13: Train ML Models
# Dataset: UNSW-NB15
# Task: Binary Attack Detection
# ==========================================================


# ----------------------------------------------------------
# 1. Project paths
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "processed"

MODELS_DIR = PROJECT_ROOT / "models"

REPORTS_DIR = PROJECT_ROOT / "reports"

MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ----------------------------------------------------------
# 2. Load engineered data
# ----------------------------------------------------------

print("=" * 70)
print("CYBERGUARD AI - MODEL TRAINING")
print("=" * 70)

print("\nLoading engineered datasets...")

X_train = pd.read_csv(
    DATA_DIR / "X_train_engineered.csv"
)

X_test = pd.read_csv(
    DATA_DIR / "X_test_engineered.csv"
)

y_train = pd.read_csv(
    DATA_DIR / "y_train_engineered.csv"
).squeeze()

y_test = pd.read_csv(
    DATA_DIR / "y_test_engineered.csv"
).squeeze()


print("\nData loaded successfully.")

print(
    f"X_train shape: {X_train.shape}"
)

print(
    f"X_test shape : {X_test.shape}"
)

print(
    f"y_train shape: {y_train.shape}"
)

print(
    f"y_test shape : {y_test.shape}"
)


# ==========================================================
# 3. Define models
# ==========================================================

models = {

    "Logistic Regression":
        LogisticRegression(
            max_iter=1000,
            random_state=42
        ),

    "Decision Tree":
        DecisionTreeClassifier(
            random_state=42
        ),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
}


# ==========================================================
# 4. Train models
# ==========================================================

results = []

trained_models = {}


for name, model in models.items():

    print("\n" + "=" * 70)

    print(
        f"TRAINING: {name}"
    )

    print("=" * 70)

    start_time = time.time()

    # Train
    model.fit(
        X_train,
        y_train
    )

    training_time = (
        time.time() - start_time
    )

    print(
        f"Training completed in "
        f"{training_time:.2f} seconds."
    )


    # ------------------------------------------------------
    # Predictions
    # ------------------------------------------------------

    y_pred = model.predict(
        X_test
    )


    # ------------------------------------------------------
    # Probability predictions
    # ------------------------------------------------------

    if hasattr(
        model,
        "predict_proba"
    ):

        y_probability = (
            model.predict_proba(
                X_test
            )[:, 1]
        )

        roc_auc = roc_auc_score(
            y_test,
            y_probability
        )

    else:

        roc_auc = None


    # ------------------------------------------------------
    # Metrics
    # ------------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )


    # ------------------------------------------------------
    # Store results
    # ------------------------------------------------------

    results.append({

        "Model": name,

        "Accuracy": accuracy,

        "Precision": precision,

        "Recall": recall,

        "F1_Score": f1,

        "ROC_AUC": roc_auc,

        "Training_Time_Seconds":
            training_time
    })


    trained_models[name] = model


    # ------------------------------------------------------
    # Print results
    # ------------------------------------------------------

    print(
        f"\nAccuracy : {accuracy:.4f}"
    )

    print(
        f"Precision: {precision:.4f}"
    )

    print(
        f"Recall   : {recall:.4f}"
    )

    print(
        f"F1-Score : {f1:.4f}"
    )

    if roc_auc is not None:

        print(
            f"ROC-AUC  : {roc_auc:.4f}"
        )


# ==========================================================
# 5. Create comparison table
# ==========================================================

results_df = pd.DataFrame(
    results
)


results_df = results_df.sort_values(
    by="F1_Score",
    ascending=False
)


print("\n" + "=" * 70)

print(
    "MODEL COMPARISON"
)

print("=" * 70)

print(
    results_df.to_string(
        index=False
    )
)


# ==========================================================
# 6. Save comparison results
# ==========================================================

comparison_path = (
    REPORTS_DIR
    / "model_comparison_engineered.csv"
)

results_df.to_csv(
    comparison_path,
    index=False
)


print(
    f"\nComparison saved to:"
    f"\n{comparison_path}"
)


# ==========================================================
# 7. Save trained models
# ==========================================================

for name, model in trained_models.items():

    filename = (
        name
        .lower()
        .replace(" ", "_")
        + "_engineered.joblib"
    )

    model_path = (
        MODELS_DIR
        / filename
    )

    joblib.dump(
        model,
        model_path
    )

    print(
        f"\nSaved {name} to:"
        f"\n{model_path}"
    )


# ==========================================================
# 8. Final summary
# ==========================================================

print("\n" + "=" * 70)

print(
    "MODEL TRAINING COMPLETED"
)

print("=" * 70)

print(
    "\nBest model based on F1-score:"
)

best_model = results_df.iloc[0]

print(
    f"Model    : {best_model['Model']}"
)

print(
    f"Accuracy : "
    f"{best_model['Accuracy']:.4f}"
)

print(
    f"Precision: "
    f"{best_model['Precision']:.4f}"
)

print(
    f"Recall   : "
    f"{best_model['Recall']:.4f}"
)

print(
    f"F1-Score : "
    f"{best_model['F1_Score']:.4f}"
)

print(
    f"ROC-AUC  : "
    f"{best_model['ROC_AUC']}"
)