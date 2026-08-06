import pandas as pd
import joblib
import json

from pathlib import Path


# ==========================================================
# CyberGuard AI
# Step 7 - Save Final Model
# Dataset: UNSW-NB15
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


print("=" * 70)
print("CYBERGUARD AI - SAVE FINAL MODEL")
print("=" * 70)


# ==========================================================
# 2. Load the best trained model
# ==========================================================

print("\nLoading Random Forest model...")


MODEL_PATH = (
    MODELS_DIR /
    "random_forest_engineered.joblib"
)


if not MODEL_PATH.exists():

    raise FileNotFoundError(
        f"Model not found:\n{MODEL_PATH}"
    )


random_forest = joblib.load(
    MODEL_PATH
)


print(
    "Random Forest model loaded successfully."
)


# ==========================================================
# 3. Load feature selection object
# ==========================================================

print("\nLoading feature selection objects...")


SELECTOR_PATH = (
    MODELS_DIR /
    "select_k_best.joblib"
)


VARIANCE_PATH = (
    MODELS_DIR /
    "variance_selector.joblib"
)


if not SELECTOR_PATH.exists():

    raise FileNotFoundError(
        f"SelectKBest file not found:\n"
        f"{SELECTOR_PATH}"
    )


if not VARIANCE_PATH.exists():

    raise FileNotFoundError(
        f"Variance selector not found:\n"
        f"{VARIANCE_PATH}"
    )


select_k_best = joblib.load(
    SELECTOR_PATH
)

variance_selector = joblib.load(
    VARIANCE_PATH
)


print(
    "Feature selection objects loaded successfully."
)


# ==========================================================
# 4. Load selected feature names
# ==========================================================

FEATURES_PATH = (
    MODELS_DIR /
    "selected_features.txt"
)


if not FEATURES_PATH.exists():

    raise FileNotFoundError(
        f"Selected feature file not found:\n"
        f"{FEATURES_PATH}"
    )


with open(
    FEATURES_PATH,
    "r",
    encoding="utf-8"
) as file:

    selected_features = [
        line.strip()
        for line in file
        if line.strip()
    ]


print(
    f"\nNumber of selected features: "
    f"{len(selected_features)}"
)


# ==========================================================
# 5. Save final model
# ==========================================================

FINAL_MODEL_PATH = (
    MODELS_DIR /
    "cyberguard_final_random_forest.joblib"
)


joblib.dump(
    random_forest,
    FINAL_MODEL_PATH
)


print(
    "\nFinal Random Forest model saved to:"
)

print(
    FINAL_MODEL_PATH
)


# ==========================================================
# 6. Save complete feature pipeline
# ==========================================================

feature_pipeline = {

    "variance_selector":
        variance_selector,

    "select_k_best":
        select_k_best,

    "selected_features":
        selected_features
}


PIPELINE_PATH = (
    MODELS_DIR /
    "cyberguard_feature_pipeline.joblib"
)


joblib.dump(
    feature_pipeline,
    PIPELINE_PATH
)


print(
    "\nFeature engineering pipeline saved to:"
)

print(
    PIPELINE_PATH
)


# ==========================================================
# 7. Save model metadata
# ==========================================================

metadata = {

    "project":
        "CyberGuard AI",

    "dataset":
        "UNSW-NB15",

    "task":
        "Binary Network Attack Detection",

    "model":
        "Random Forest",

    "model_file":
        "cyberguard_final_random_forest.joblib",

    "feature_pipeline":
        "cyberguard_feature_pipeline.joblib",

    "number_of_features":
        len(selected_features),

    "classes": {

        "0":
            "Normal",

        "1":
            "Attack"
    },

    "training_results": {

        "accuracy":
            0.875370,

        "precision":
            0.823993,

        "recall":
            0.983786,

        "f1_score":
            0.896828,

        "roc_auc":
            0.979243
    }

}


METADATA_PATH = (
    MODELS_DIR /
    "model_metadata.json"
)


with open(
    METADATA_PATH,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        metadata,
        file,
        indent=4
    )


print(
    "\nModel metadata saved to:"
)

print(
    METADATA_PATH
)


# ==========================================================
# 8. Verify saved files
# ==========================================================

print("\n" + "=" * 70)

print(
    "SAVED MODEL FILES"
)

print("=" * 70)


saved_files = [

    FINAL_MODEL_PATH,

    PIPELINE_PATH,

    METADATA_PATH,

    FEATURES_PATH
]


for file_path in saved_files:

    if file_path.exists():

        size_mb = (
            file_path.stat().st_size
            / (1024 * 1024)
        )

        print(
            f"✓ {file_path.name}"
            f" ({size_mb:.2f} MB)"
        )

    else:

        print(
            f"✗ Missing: "
            f"{file_path.name}"
        )


# ==========================================================
# 9. Final message
# ==========================================================

print("\n" + "=" * 70)

print(
    "MODEL SAVING COMPLETED SUCCESSFULLY"
)

print("=" * 70)


print("\nCyberGuard AI final model:")

print(
    "Random Forest"
)

print(
    "Accuracy : 87.54%"
)

print(
    "Precision: 82.40%"
)

print(
    "Recall   : 98.38%"
)

print(
    "F1-Score : 89.68%"
)

print(
    "ROC-AUC  : 97.92%"
)