import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ==========================================================
# CyberGuard AI
# Step 10: Preprocessing + Feature Engineering
# Dataset: UNSW-NB15
# ==========================================================


# ----------------------------------------------------------
# 1. Project paths
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TRAIN_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "UNSW_NB15_training-set.csv"
)

TEST_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "UNSW_NB15_testing-set.csv"
)

PROCESSED_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

MODELS_DIR = (
    PROJECT_ROOT
    / "models"
)

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ----------------------------------------------------------
# 2. Load datasets
# ----------------------------------------------------------

print("=" * 70)
print("CYBERGUARD AI - PREPROCESSING + FEATURE ENGINEERING")
print("=" * 70)

print("\nLoading datasets...")

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

print(f"Training shape: {train_df.shape}")
print(f"Testing shape : {test_df.shape}")


# ----------------------------------------------------------
# 3. Separate target
# ----------------------------------------------------------

TARGET = "label"

y_train = train_df[TARGET].copy()
y_test = test_df[TARGET].copy()

X_train = train_df.drop(
    columns=[TARGET]
).copy()

X_test = test_df.drop(
    columns=[TARGET]
).copy()


# ----------------------------------------------------------
# 4. Remove target-related information
# ----------------------------------------------------------

if "attack_cat" in X_train.columns:

    X_train = X_train.drop(
        columns=["attack_cat"]
    )

    X_test = X_test.drop(
        columns=["attack_cat"]
    )

    print("\nRemoved: attack_cat")


# ----------------------------------------------------------
# 5. Remove identifier
# ----------------------------------------------------------

if "id" in X_train.columns:

    X_train = X_train.drop(
        columns=["id"]
    )

    X_test = X_test.drop(
        columns=["id"]
    )

    print("Removed: id")


# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

print("\n" + "=" * 70)
print("FEATURE ENGINEERING")
print("=" * 70)


def create_engineered_features(df):
    """
    Create additional network traffic features.

    The function does not use:
    - label
    - attack_cat
    - id

    This prevents target leakage.
    """

    df = df.copy()

    # ------------------------------------------------------
    # Total packets
    # ------------------------------------------------------

    if "spkts" in df.columns and "dpkts" in df.columns:

        df["total_packets"] = (
            df["spkts"] + df["dpkts"]
        )

    # ------------------------------------------------------
    # Total bytes
    # ------------------------------------------------------

    if "sbytes" in df.columns and "dbytes" in df.columns:

        df["total_bytes"] = (
            df["sbytes"] + df["dbytes"]
        )

    # ------------------------------------------------------
    # Bytes per packet
    # ------------------------------------------------------

    if (
        "total_bytes" in df.columns
        and "total_packets" in df.columns
    ):

        df["bytes_per_packet"] = (
            df["total_bytes"]
            / df["total_packets"].replace(0, np.nan)
        )

    # ------------------------------------------------------
    # Packets per second
    # ------------------------------------------------------

    if (
        "total_packets" in df.columns
        and "dur" in df.columns
    ):

        df["packets_per_second"] = (
            df["total_packets"]
            / df["dur"].replace(0, np.nan)
        )

    # ------------------------------------------------------
    # Bytes per second
    # ------------------------------------------------------

    if (
        "total_bytes" in df.columns
        and "dur" in df.columns
    ):

        df["bytes_per_second"] = (
            df["total_bytes"]
            / df["dur"].replace(0, np.nan)
        )

    # ------------------------------------------------------
    # Source-to-destination byte ratio
    # ------------------------------------------------------

    if (
        "sbytes" in df.columns
        and "dbytes" in df.columns
    ):

        df["source_destination_byte_ratio"] = (
            df["sbytes"]
            / df["dbytes"].replace(0, np.nan)
        )

    # ------------------------------------------------------
    # Replace infinite values
    # ------------------------------------------------------

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    return df


# Apply the EXACT SAME feature engineering to both sets

X_train = create_engineered_features(X_train)

X_test = create_engineered_features(X_test)


# ----------------------------------------------------------
# Display engineered features
# ----------------------------------------------------------

engineered_features = [
    "total_packets",
    "total_bytes",
    "bytes_per_packet",
    "packets_per_second",
    "bytes_per_second",
    "source_destination_byte_ratio"
]

print("\nEngineered features created:")

for feature in engineered_features:

    if feature in X_train.columns:
        print(f"  + {feature}")


# ----------------------------------------------------------
# Handle NaN values created by division
# ----------------------------------------------------------

# We use training-set medians to fill numerical missing values.
# The medians are learned ONLY from the training data.

numeric_for_median = X_train.select_dtypes(
    include=[np.number]
).columns

train_medians = X_train[
    numeric_for_median
].median()

X_train[numeric_for_median] = (
    X_train[numeric_for_median]
    .fillna(train_medians)
)

X_test[numeric_for_median] = (
    X_test[numeric_for_median]
    .fillna(train_medians)
)


# ==========================================================
# IDENTIFY FEATURE TYPES
# ==========================================================

categorical_columns = X_train.select_dtypes(
    include=["object"]
).columns.tolist()

numerical_columns = X_train.select_dtypes(
    include=[np.number]
).columns.tolist()


print("\n" + "=" * 70)
print("FEATURE INFORMATION")
print("=" * 70)

print(
    f"\nNumerical features   : "
    f"{len(numerical_columns)}"
)

print(
    f"Categorical features : "
    f"{len(categorical_columns)}"
)

print("\nCategorical columns:")

for column in categorical_columns:
    print(f"  - {column}")


# ==========================================================
# PREPROCESSING PIPELINE
# ==========================================================

print("\n" + "=" * 70)
print("CREATING PREPROCESSING PIPELINE")
print("=" * 70)


preprocessor = ColumnTransformer(
    transformers=[
        (
            "numerical",
            StandardScaler(),
            numerical_columns
        ),
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_columns
        )
    ]
)


# ==========================================================
# FIT ONLY ON TRAINING DATA
# ==========================================================

print("\nFitting preprocessor on TRAINING data...")

X_train_processed = preprocessor.fit_transform(
    X_train
)


# ==========================================================
# TRANSFORM TEST DATA
# ==========================================================

print("Transforming TEST data...")

X_test_processed = preprocessor.transform(
    X_test
)


# ==========================================================
# FEATURE NAMES
# ==========================================================

feature_names = (
    preprocessor
    .get_feature_names_out()
)

print(
    f"\nTotal processed features: "
    f"{len(feature_names)}"
)


# ==========================================================
# CONVERT TO DATAFRAMES
# ==========================================================

X_train_processed = pd.DataFrame(
    X_train_processed,
    columns=feature_names
)

X_test_processed = pd.DataFrame(
    X_test_processed,
    columns=feature_names
)


# ==========================================================
# SAVE PROCESSED DATA
# ==========================================================

print("\nSaving processed datasets...")

X_train_processed.to_csv(
    PROCESSED_DIR / "X_train.csv",
    index=False
)

X_test_processed.to_csv(
    PROCESSED_DIR / "X_test.csv",
    index=False
)

y_train.to_csv(
    PROCESSED_DIR / "y_train.csv",
    index=False
)

y_test.to_csv(
    PROCESSED_DIR / "y_test.csv",
    index=False
)


# ==========================================================
# SAVE PREPROCESSOR
# ==========================================================

preprocessor_path = (
    MODELS_DIR
    / "preprocessor.joblib"
)

joblib.dump(
    preprocessor,
    preprocessor_path
)

# Save training medians for inference

medians_path = (
    MODELS_DIR / "training_medians.joblib"
)

joblib.dump(
    train_medians.to_dict(),
    medians_path
)

print(
    f"Training medians saved to:"
    f"\n{medians_path}"
)

print(
    f"\nPreprocessor saved to:"
    f"\n{preprocessor_path}"
)


# ==========================================================
# SAVE FEATURE NAMES
# ==========================================================

feature_names_path = (
    MODELS_DIR
    / "feature_names.txt"
)

with open(
    feature_names_path,
    "w",
    encoding="utf-8"
) as file:

    for feature in feature_names:
        file.write(
            f"{feature}\n"
        )

print(
    f"Feature names saved to:"
    f"\n{feature_names_path}"
)


# ==========================================================
# FINAL INFORMATION
# ==========================================================

print("\n" + "=" * 70)
print("FINAL PROCESSED DATA")
print("=" * 70)

print(
    f"\nX_train: "
    f"{X_train_processed.shape}"
)

print(
    f"X_test : "
    f"{X_test_processed.shape}"
)

print(
    f"y_train: "
    f"{y_train.shape}"
)

print(
    f"y_test : "
    f"{y_test.shape}"
)


print("\n" + "=" * 70)
print("STEP 10 COMPLETED SUCCESSFULLY")
print("=" * 70)