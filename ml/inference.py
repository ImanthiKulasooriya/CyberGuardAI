import pandas as pd
import joblib

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT /
    "models" /
    "cyberguard_final_random_forest.joblib"
)


model = joblib.load(
    MODEL_PATH
)


def predict_dataframe(df):

    predictions = model.predict(df)

    probabilities = model.predict_proba(df)

    results = []

    for prediction, probability in zip(
        predictions,
        probabilities
    ):

        attack_probability = float(
            probability[1]
        )

        if prediction == 1:

            label = "Attack"

        else:

            label = "Normal"


        if attack_probability >= 0.80:

            risk = "HIGH"

        elif attack_probability >= 0.50:

            risk = "MEDIUM"

        else:

            risk = "LOW"


        results.append({

            "prediction": label,

            "confidence":
                attack_probability,

            "risk_level": risk
        })


    return results