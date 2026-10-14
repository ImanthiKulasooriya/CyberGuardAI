import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from sklearn.feature_selection import (
    VarianceThreshold,
    SelectKBest,
    mutual_info_classif
)

import matplotlib.pyplot as plt


# ==========================================================
# CyberGuard AI
# Step 11: Feature Engineering
#
# Dataset: UNSW-NB15
# Task: Binary Network Attack Detection
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
print("CYBERGUARD AI - FEATURE ENGINEERING")
print("=" * 70)


# ----------------------------------------------------------
# 2. Load processed data
# ----------------------------------------------------------

print("\nLoading processed datasets...")

X_train = pd.read_csv(
    DATA_DIR / "X_train.csv"
)

X_test = pd.read_csv(
    DATA_DIR / "X_test.csv"
)

y_train = pd.read_csv(
    DATA_DIR / "y_train.csv"
).squeeze()

y_test = pd.read_csv(
    DATA_DIR / "y_test.csv"
).squeeze()


print("\nData loaded successfully.")

print(f"X_train shape: {X_train.shape}")
print(f"X_test shape : {X_test.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"y_test shape : {y_test.shape}")


# ----------------------------------------------------------
# 3. Make sure train and test columns match
# ----------------------------------------------------------

if list(X_train.columns) != list(X_test.columns):

    raise ValueError(
        "Training and testing feature columns do not match."
    )

print("\nTraining and testing features match.")


# ==========================================================
# PART A — REMOVE CONSTANT / LOW-VARIANCE FEATURES
# ==========================================================

print("\n" + "=" * 70)
print("PART A - VARIANCE THRESHOLD")
print("=" * 70)


# ----------------------------------------------------------
# 4. Find zero-variance features
# ----------------------------------------------------------

variance_selector = VarianceThreshold(
    threshold=0.0
)

variance_selector.fit(X_train)


variance_mask = variance_selector.get_support()


removed_variance_features = (
    X_train.columns[~variance_mask]
    .tolist()
)

remaining_variance_features = (
    X_train.columns[variance_mask]
    .tolist()
)


print(
    f"\nOriginal number of features: "
    f"{X_train.shape[1]}"
)

print(
    f"Zero-variance features removed: "
    f"{len(removed_variance_features)}"
)

print(
    f"Features remaining: "
    f"{len(remaining_variance_features)}"
)


# Apply variance selection

X_train_variance = pd.DataFrame(
    variance_selector.transform(X_train),
    columns=remaining_variance_features
)

X_test_variance = pd.DataFrame(
    variance_selector.transform(X_test),
    columns=remaining_variance_features
)


# ----------------------------------------------------------
# 5. Save variance selector
# ----------------------------------------------------------

joblib.dump(
    variance_selector,
    MODELS_DIR / "variance_selector.joblib"
)


# ==========================================================
# PART B — MUTUAL INFORMATION FEATURE SELECTION
# ==========================================================

print("\n" + "=" * 70)
print("PART B - MUTUAL INFORMATION")
print("=" * 70)


print(
    "\nCalculating feature relevance..."
)

print(
    "This may take some time because the dataset "
    "contains many samples."
)


# ----------------------------------------------------------
# 6. Calculate mutual information
# ----------------------------------------------------------

mi_scores = mutual_info_classif(
    X_train_variance,
    y_train,
    random_state=42
)


mi_scores_df = pd.DataFrame({
    "feature": X_train_variance.columns,
    "mutual_information": mi_scores
})


mi_scores_df = mi_scores_df.sort_values(
    by="mutual_information",
    ascending=False
)


# ----------------------------------------------------------
# 7. Save all feature scores
# ----------------------------------------------------------

mi_scores_df.to_csv(
    REPORTS_DIR / "mutual_information_scores.csv",
    index=False
)


print("\nTop 20 features based on mutual information:")

print(
    mi_scores_df.head(20).to_string(
        index=False
    )
)


# ==========================================================
# PART C — SELECT TOP FEATURES
# ==========================================================

print("\n" + "=" * 70)
print("PART C - SELECT TOP FEATURES")
print("=" * 70)


# ----------------------------------------------------------
# 8. Select top K features
# ----------------------------------------------------------

# We currently have 200 processed features.
# We will keep the top 100 informative features.

K_FEATURES = min(
    100,
    X_train_variance.shape[1]
)


print(
    f"\nSelecting top {K_FEATURES} features..."
)


select_k_best = SelectKBest(
    score_func=mutual_info_classif,
    k=K_FEATURES
)


X_train_selected_array = (
    select_k_best.fit_transform(
        X_train_variance,
        y_train
    )
)


X_test_selected_array = (
    select_k_best.transform(
        X_test_variance
    )
)


# ----------------------------------------------------------
# 9. Get selected feature names
# ----------------------------------------------------------

selected_mask = (
    select_k_best.get_support()
)

selected_features = (
    X_train_variance.columns[selected_mask]
    .tolist()
)


print(
    f"\nSelected features: "
    f"{len(selected_features)}"
)


print("\nSelected feature names:")

for number, feature in enumerate(
    selected_features,
    start=1
):

    print(
        f"{number:3d}. {feature}"
    )


# ----------------------------------------------------------
# 10. Convert arrays to DataFrames
# ----------------------------------------------------------

X_train_selected = pd.DataFrame(
    X_train_selected_array,
    columns=selected_features
)

X_test_selected = pd.DataFrame(
    X_test_selected_array,
    columns=selected_features
)


# ==========================================================
# PART D — SAVE FEATURE-ENGINEERED DATA
# ==========================================================

print("\n" + "=" * 70)
print("PART D - SAVE FEATURE-ENGINEERED DATA")
print("=" * 70)


# ----------------------------------------------------------
# 11. Save selected training data
# ----------------------------------------------------------

X_train_selected.to_csv(
    DATA_DIR / "X_train_engineered.csv",
    index=False
)


# ----------------------------------------------------------
# 12. Save selected testing data
# ----------------------------------------------------------

X_test_selected.to_csv(
    DATA_DIR / "X_test_engineered.csv",
    index=False
)


# ----------------------------------------------------------
# 13. Save labels
# ----------------------------------------------------------

y_train.to_csv(
    DATA_DIR / "y_train_engineered.csv",
    index=False
)

y_test.to_csv(
    DATA_DIR / "y_test_engineered.csv",
    index=False
)


# ----------------------------------------------------------
# 14. Save selected feature names
# ----------------------------------------------------------

with open(
    MODELS_DIR / "selected_features.txt",
    "w",
    encoding="utf-8"
) as file:

    for feature in selected_features:

        file.write(
            feature + "\n"
        )


# ----------------------------------------------------------
# 15. Save SelectKBest object
# ----------------------------------------------------------

joblib.dump(
    select_k_best,
    MODELS_DIR / "select_k_best.joblib"
)


# ==========================================================
# PART E — FEATURE IMPORTANCE VISUALIZATION
# ==========================================================

print("\n" + "=" * 70)
print("PART E - FEATURE IMPORTANCE VISUALIZATION")
print("=" * 70)


selected_scores = mi_scores_df[
    mi_scores_df["feature"].isin(
        selected_features
    )
].copy()


selected_scores = selected_scores.sort_values(
    by="mutual_information",
    ascending=True
)


# ----------------------------------------------------------
# 16. Plot top 20 features
# ----------------------------------------------------------

top_20 = (
    selected_scores
    .sort_values(
        by="mutual_information",
        ascending=False
    )
    .head(20)
    .sort_values(
        by="mutual_information",
        ascending=True
    )
)


plt.figure(
    figsize=(10, 8)
)

plt.barh(
    top_20["feature"],
    top_20["mutual_information"]
)

plt.xlabel(
    "Mutual Information Score"
)

plt.ylabel(
    "Feature"
)

plt.title(
    "Top 20 Features - CyberGuard AI"
)

plt.tight_layout()


feature_plot_path = (
    REPORTS_DIR
    / "13_top_20_features.png"
)


plt.savefig(
    feature_plot_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ==========================================================
# PART F — SUMMARY
# ==========================================================

print("\n" + "=" * 70)
print("FEATURE ENGINEERING SUMMARY")
print("=" * 70)


print(
    f"\nOriginal features:"
    f" {X_train.shape[1]}"
)

print(
    f"After variance filtering:"
    f" {X_train_variance.shape[1]}"
)

print(
    f"Final selected features:"
    f" {X_train_selected.shape[1]}"
)

print(
    f"\nEngineered training shape:"
    f" {X_train_selected.shape}"
)

print(
    f"Engineered testing shape:"
    f" {X_test_selected.shape}"
)


print("\nGenerated files:")

print(
    DATA_DIR / "X_train_engineered.csv"
)

print(
    DATA_DIR / "X_test_engineered.csv"
)

print(
    DATA_DIR / "y_train_engineered.csv"
)

print(
    DATA_DIR / "y_test_engineered.csv"
)

print(
    MODELS_DIR / "selected_features.txt"
)

print(
    REPORTS_DIR / "mutual_information_scores.csv"
)

print(
    REPORTS_DIR / "13_top_20_features.png"
)


print("\n" + "=" * 70)
print("FEATURE ENGINEERING COMPLETED")
print("=" * 70)

import pandas as pd

importance = pd.DataFrame({

    "feature": X_train.columns,

    "importance":
        model.feature_importances_

})


importance = importance.sort_values(
    "importance",
    ascending=False
)


print(
    importance.head(20)
)
