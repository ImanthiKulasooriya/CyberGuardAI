import pandas as pd
import joblib

from pathlib import Path
import matplotlib.pyplot as plt


# ==========================================================
# CyberGuard AI
# Step 8 - Feature Importance
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


print("=" * 70)
print("CYBERGUARD AI - FEATURE IMPORTANCE")
print("=" * 70)


# ----------------------------------------------------------
# 1. Load trained Random Forest
# ----------------------------------------------------------

MODEL_PATH = (
    MODELS_DIR /
    "random_forest_engineered.joblib"
)


print("\nLoading Random Forest model...")


if not MODEL_PATH.exists():

    raise FileNotFoundError(
        f"Model not found:\n{MODEL_PATH}"
    )


model = joblib.load(
    MODEL_PATH
)


print("Model loaded successfully.")


# ----------------------------------------------------------
# 2. Load engineered training data
# ----------------------------------------------------------

TRAIN_PATH = (
    DATA_DIR /
    "X_train_engineered.csv"
)


print("\nLoading engineered training data...")


if not TRAIN_PATH.exists():

    raise FileNotFoundError(
        f"Training data not found:\n{TRAIN_PATH}"
    )


X_train = pd.read_csv(
    TRAIN_PATH
)


print(
    f"Training data shape: {X_train.shape}"
)


# ----------------------------------------------------------
# 3. Check feature count
# ----------------------------------------------------------

print("\nChecking feature count...")


print(
    f"Model expects: "
    f"{model.n_features_in_} features"
)

print(
    f"Dataset contains: "
    f"{X_train.shape[1]} features"
)


if model.n_features_in_ != X_train.shape[1]:

    raise ValueError(
        "Feature count mismatch between "
        "model and dataset."
    )


# ----------------------------------------------------------
# 4. Extract feature importance
# ----------------------------------------------------------

importance = pd.DataFrame({

    "Feature":
        X_train.columns,

    "Importance":
        model.feature_importances_

})


# ----------------------------------------------------------
# 5. Sort by importance
# ----------------------------------------------------------

importance = importance.sort_values(
    by="Importance",
    ascending=False
)


importance = importance.reset_index(
    drop=True
)


# ----------------------------------------------------------
# 6. Save complete feature importance
# ----------------------------------------------------------

CSV_PATH = (
    REPORTS_DIR /
    "feature_importance.csv"
)


importance.to_csv(
    CSV_PATH,
    index=False
)


print(
    "\nFeature importance saved to:"
)

print(
    CSV_PATH
)


# ----------------------------------------------------------
# 7. Display top 20
# ----------------------------------------------------------

print("\n" + "=" * 70)

print(
    "TOP 20 MOST IMPORTANT FEATURES"
)

print("=" * 70)


print(
    importance.head(20).to_string(
        index=False
    )
)


# ----------------------------------------------------------
# 8. Create top 20 chart
# ----------------------------------------------------------

top_features = (
    importance
    .head(20)
    .sort_values(
        by="Importance",
        ascending=True
    )
)


plt.figure(
    figsize=(10, 8)
)


plt.barh(
    top_features["Feature"],
    top_features["Importance"]
)


plt.xlabel(
    "Feature Importance"
)

plt.ylabel(
    "Feature"
)

plt.title(
    "Top 20 Features - Random Forest"
)

plt.tight_layout()


CHART_PATH = (
    REPORTS_DIR /
    "feature_importance_top20.png"
)


plt.savefig(
    CHART_PATH,
    dpi=300,
    bbox_inches="tight"
)


plt.close()


print(
    "\nFeature importance chart saved to:"
)

print(
    CHART_PATH
)


print("\n" + "=" * 70)

print(
    "FEATURE IMPORTANCE COMPLETED"
)

print("=" * 70)