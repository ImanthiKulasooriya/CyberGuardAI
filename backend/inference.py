import pandas as pd
import numpy as np
import joblib

from pathlib import Path


# ==========================================================
# CyberGuard AI - Inference Pipeline
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODELS_DIR = PROJECT_ROOT / "models"


# ==========================================================
# Load saved ML components
# ==========================================================

print("Loading CyberGuard AI inference components...")

preprocessor = joblib.load(
    MODELS_DIR / "preprocessor.joblib"
)

training_medians = joblib.load(
    MODELS_DIR / "training_medians.joblib"
)

variance_selector = joblib.load(
    MODELS_DIR / "variance_selector.joblib"
)

select_k_best = joblib.load(
    MODELS_DIR / "select_k_best.joblib"
)

model = joblib.load(
    MODELS_DIR / "random_forest_engineered.joblib"
)

print("Inference components loaded successfully.")


# ==========================================================
# Feature Engineering
# ==========================================================

def create_engineered_features(df):

    df = df.copy()

    # Remove target-related columns
    for column in ["label", "attack_cat", "id"]:

        if column in df.columns:
            df = df.drop(
                columns=[column]
            )

    # Total packets
    if (
        "spkts" in df.columns
        and "dpkts" in df.columns
    ):

        df["total_packets"] = (
            df["spkts"] + df["dpkts"]
        )

    # Total bytes
    if (
        "sbytes" in df.columns
        and "dbytes" in df.columns
    ):

        df["total_bytes"] = (
            df["sbytes"] + df["dbytes"]
        )

    # Bytes per packet
    if (
        "total_bytes" in df.columns
        and "total_packets" in df.columns
    ):

        df["bytes_per_packet"] = (
            df["total_bytes"]
            /
            df["total_packets"].replace(
                0,
                np.nan
            )
        )

    # Packets per second
    if (
        "total_packets" in df.columns
        and "dur" in df.columns
    ):

        df["packets_per_second"] = (
            df["total_packets"]
            /
            df["dur"].replace(
                0,
                np.nan
            )
        )

    # Bytes per second
    if (
        "total_bytes" in df.columns
        and "dur" in df.columns
    ):

        df["bytes_per_second"] = (
            df["total_bytes"]
            /
            df["dur"].replace(
                0,
                np.nan
            )
        )

    # Source / destination byte ratio
    if (
        "sbytes" in df.columns
        and "dbytes" in df.columns
    ):

        df["source_destination_byte_ratio"] = (
            df["sbytes"]
            /
            df["dbytes"].replace(
                0,
                np.nan
            )
        )

    # Replace infinity
    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    return df


# ==========================================================
# Prepare Input
# ==========================================================

def prepare_input(df):

    df = df.copy()

    # ------------------------------------------------------
    # Feature engineering
    # ------------------------------------------------------

    df = create_engineered_features(
        df
    )

    # ------------------------------------------------------
    # Required training columns
    # ------------------------------------------------------

    required_columns = (
        preprocessor.feature_names_in_
    )

    # ------------------------------------------------------
    # Check missing columns
    # ------------------------------------------------------

    missing_columns = (
        set(required_columns)
        -
        set(df.columns)
    )

    if missing_columns:

        raise ValueError(
            "Input CSV is missing required "
            f"columns: {sorted(missing_columns)}"
        )

    # ------------------------------------------------------
    # Keep EXACT same columns and order
    # ------------------------------------------------------

    df = df[
        required_columns
    ].copy()

    # ------------------------------------------------------
    # Replace infinity
    # ------------------------------------------------------

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    # ------------------------------------------------------
    # Fill missing values
    # using training medians
    # ------------------------------------------------------

    for column in df.columns:

        if column in training_medians:

            df[column] = (
                df[column]
                .fillna(
                    training_medians[column]
                )
            )

    # ------------------------------------------------------
    # Categorical missing values
    # ------------------------------------------------------

    categorical_columns = (
        df.select_dtypes(
            include=["object"]
        ).columns
    )

    for column in categorical_columns:

        df[column] = (
            df[column]
            .fillna("unknown")
        )

    # ------------------------------------------------------
    # Final numerical safety check
    # ------------------------------------------------------

    numerical_columns = (
        df.select_dtypes(
            include=[np.number]
        ).columns
    )

    df[numerical_columns] = (
        df[numerical_columns]
        .replace(
            [np.inf, -np.inf],
            np.nan
        )
    )

    # If anything is still missing,
    # use training median or 0.

    for column in numerical_columns:

        if df[column].isna().any():

            if column in training_medians:

                df[column] = (
                    df[column]
                    .fillna(
                        training_medians[column]
                    )
                )

            else:

                df[column] = (
                    df[column]
                    .fillna(0)
                )

    # ------------------------------------------------------
    # Verify no NaN remains
    # ------------------------------------------------------

    if df.isna().any().any():

        remaining = (
            df.columns[
                df.isna().any()
            ].tolist()
        )

        raise ValueError(
            "NaN values remain after "
            f"preprocessing: {remaining}"
        )

    return df


# ==========================================================
# Prediction
# ==========================================================

def predict_dataframe(df):

    # ------------------------------------------------------
    # 1. Prepare input
    # ------------------------------------------------------

    prepared_df = prepare_input(
        df
    )

    # ------------------------------------------------------
    # 2. Preprocessing
    # ------------------------------------------------------

    processed = (
        preprocessor.transform(
            prepared_df
        )
    )

    # ------------------------------------------------------
    # Extra safety check
    # ------------------------------------------------------

    if np.isnan(processed).any():

        raise ValueError(
            "NaN values detected after "
            "preprocessor.transform()."
        )

    # ------------------------------------------------------
    # 3. Variance selection
    # ------------------------------------------------------

    variance_data = (
        variance_selector.transform(
            processed
        )
    )

    # ------------------------------------------------------
    # 4. SelectKBest
    # ------------------------------------------------------

    selected_data = (
        select_k_best.transform(
            variance_data
        )
    )

    # ------------------------------------------------------
    # Extra safety check
    # ------------------------------------------------------

    if np.isnan(selected_data).any():

        raise ValueError(
            "NaN values detected before "
            "model prediction."
        )

    # ------------------------------------------------------
    # 5. Model prediction
    # ------------------------------------------------------

    predictions = (
        model.predict(
            selected_data
        )
    )

    probabilities = (
        model.predict_proba(
            selected_data
        )
    )

    results = []

    # ------------------------------------------------------
    # 6. Generate results
    # ------------------------------------------------------

    for index, prediction in enumerate(
        predictions
    ):

        attack_probability = float(
            probabilities[index][1]
        )

        normal_probability = float(
            probabilities[index][0]
        )

        # Prediction label
        if prediction == 1:

            label = "Attack"

            confidence = (
                attack_probability
            )

        else:

            label = "Normal"

            confidence = (
                normal_probability
            )

        # Risk level
        if attack_probability >= 0.80:

            risk = "HIGH"

        elif attack_probability >= 0.50:

            risk = "MEDIUM"

        else:

            risk = "LOW"

        results.append({

            "prediction": label,

            "confidence": round(
                confidence * 100,
                2
            ),

            "attack_probability": round(
                attack_probability * 100,
                2
            ),

            "normal_probability": round(
                normal_probability * 100,
                2
            ),

            "risk_level": risk
        })

    return results