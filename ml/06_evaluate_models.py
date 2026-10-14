import pandas as pd
import joblib

from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
    roc_curve,
    precision_recall_curve,
    average_precision_score
)

import matplotlib.pyplot as plt


# ==========================================================
# CyberGuard AI
# Step 12: Model Evaluation
# ==========================================================


# ----------------------------------------------------------
# 1. Project paths
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "processed"

MODELS_DIR = PROJECT_ROOT / "models"

REPORTS_DIR = PROJECT_ROOT / "reports"

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ----------------------------------------------------------
# 2. Load processed test data
# ----------------------------------------------------------

print("=" * 70)
print("CYBERGUARD AI - MODEL EVALUATION")
print("=" * 70)

print("\nLoading test data...")

X_test = pd.read_csv(
    DATA_DIR / "X_test.csv"
)

y_test = pd.read_csv(
    DATA_DIR / "y_test.csv"
).squeeze()

print("Test data loaded successfully.")

print(f"X_test shape: {X_test.shape}")
print(f"y_test shape: {y_test.shape}")


# ----------------------------------------------------------
# 3. Load trained model
# ----------------------------------------------------------

MODEL_PATH = (
    MODELS_DIR
    / "baseline_logistic_regression.joblib"
)

print("\nLoading trained model...")

model = joblib.load(
    MODEL_PATH
)

print("Model loaded successfully.")

print(f"Model: {model}")


# ----------------------------------------------------------
# 4. Generate predictions
# ----------------------------------------------------------

print("\nGenerating predictions...")

y_pred = model.predict(
    X_test
)

y_probability = model.predict_proba(
    X_test
)[:, 1]

print("Predictions generated successfully.")


# ==========================================================
# 5. BASIC CLASSIFICATION METRICS
# ==========================================================

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

roc_auc = roc_auc_score(
    y_test,
    y_probability
)

average_precision = average_precision_score(
    y_test,
    y_probability
)


# ==========================================================
# 6. CONFUSION MATRIX
# ==========================================================

cm = confusion_matrix(
    y_test,
    y_pred
)

tn, fp, fn, tp = cm.ravel()


# ----------------------------------------------------------
# Additional cybersecurity metrics
# ----------------------------------------------------------

false_positive_rate = (
    fp / (fp + tn)
    if (fp + tn) > 0
    else 0
)

false_negative_rate = (
    fn / (fn + tp)
    if (fn + tp) > 0
    else 0
)


# ==========================================================
# 7. PRINT RESULTS
# ==========================================================

print("\n" + "=" * 70)
print("MODEL PERFORMANCE")
print("=" * 70)

print(f"\nAccuracy              : {accuracy:.4f}")
print(f"Precision             : {precision:.4f}")
print(f"Attack Recall        : {recall:.4f}")
print(f"F1-Score              : {f1:.4f}")
print(f"ROC-AUC               : {roc_auc:.4f}")
print(f"Average Precision     : {average_precision:.4f}")

print("\n" + "-" * 70)

print(f"True Negatives        : {tn}")
print(f"False Positives       : {fp}")
print(f"False Negatives       : {fn}")
print(f"True Positives        : {tp}")

print("\n" + "-" * 70)

print(
    f"False Positive Rate   : "
    f"{false_positive_rate:.4f}"
)

print(
    f"False Negative Rate   : "
    f"{false_negative_rate:.4f}"
)


# ==========================================================
# 8. CLASSIFICATION REPORT
# ==========================================================

print("\n" + "=" * 70)
print("CLASSIFICATION REPORT")
print("=" * 70)

report = classification_report(
    y_test,
    y_pred,
    target_names=[
        "Normal",
        "Attack"
    ],
    zero_division=0
)

print(report)


# Save classification report

report_path = (
    REPORTS_DIR
    / "classification_report.txt"
)

with open(
    report_path,
    "w",
    encoding="utf-8"
) as file:

    file.write(report)


# ==========================================================
# 9. SAVE METRICS
# ==========================================================

metrics = {
    "model": "Logistic Regression",
    "accuracy": accuracy,
    "precision": precision,
    "attack_recall": recall,
    "f1_score": f1,
    "roc_auc": roc_auc,
    "average_precision": average_precision,
    "true_negatives": tn,
    "false_positives": fp,
    "false_negatives": fn,
    "true_positives": tp,
    "false_positive_rate": false_positive_rate,
    "false_negative_rate": false_negative_rate
}

metrics_df = pd.DataFrame(
    [metrics]
)

metrics_path = (
    REPORTS_DIR
    / "model_evaluation_metrics.csv"
)

metrics_df.to_csv(
    metrics_path,
    index=False
)

print(
    f"\nMetrics saved to:"
    f"\n{metrics_path}"
)


# ==========================================================
# 10. SAVE PREDICTIONS
# ==========================================================

predictions_df = pd.DataFrame({
    "actual": y_test,
    "predicted": y_pred,
    "attack_probability": y_probability
})

predictions_path = (
    REPORTS_DIR
    / "baseline_predictions.csv"
)

predictions_df.to_csv(
    predictions_path,
    index=False
)

print(
    f"Predictions saved to:"
    f"\n{predictions_path}"
)


# ==========================================================
# 11. CONFUSION MATRIX PLOT
# ==========================================================

plt.figure(
    figsize=(7, 6)
)

plt.imshow(
    cm
)

plt.title(
    "CyberGuard AI - Confusion Matrix"
)

plt.xlabel(
    "Predicted Label"
)

plt.ylabel(
    "Actual Label"
)

plt.xticks(
    [0, 1],
    ["Normal", "Attack"]
)

plt.yticks(
    [0, 1],
    ["Normal", "Attack"]
)


for i in range(2):

    for j in range(2):

        plt.text(
            j,
            i,
            cm[i, j],
            ha="center",
            va="center"
        )


plt.tight_layout()

confusion_path = (
    REPORTS_DIR
    / "10_confusion_matrix.png"
)

plt.savefig(
    confusion_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    f"\nConfusion matrix saved to:"
    f"\n{confusion_path}"
)


# ==========================================================
# 12. ROC CURVE
# ==========================================================

fpr, tpr, thresholds = roc_curve(
    y_test,
    y_probability
)

plt.figure(
    figsize=(8, 6)
)

plt.plot(
    fpr,
    tpr,
    label=f"ROC-AUC = {roc_auc:.4f}"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    label="Random Classifier"
)

plt.xlabel(
    "False Positive Rate"
)

plt.ylabel(
    "True Positive Rate"
)

plt.title(
    "ROC Curve - Logistic Regression"
)

plt.legend()

plt.tight_layout()

roc_path = (
    REPORTS_DIR
    / "11_roc_curve.png"
)

plt.savefig(
    roc_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    f"ROC curve saved to:"
    f"\n{roc_path}"
)


# ==========================================================
# 13. PRECISION-RECALL CURVE
# ==========================================================

precision_values, recall_values, pr_thresholds = (
    precision_recall_curve(
        y_test,
        y_probability
    )
)

plt.figure(
    figsize=(8, 6)
)

plt.plot(
    recall_values,
    precision_values,
    label=f"AP = {average_precision:.4f}"
)

plt.xlabel(
    "Recall"
)

plt.ylabel(
    "Precision"
)

plt.title(
    "Precision-Recall Curve - Logistic Regression"
)

plt.legend()

plt.tight_layout()

pr_path = (
    REPORTS_DIR
    / "12_precision_recall_curve.png"
)

plt.savefig(
    pr_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    f"Precision-Recall curve saved to:"
    f"\n{pr_path}"
)


# ==========================================================
# 14. FINAL SUMMARY
# ==========================================================

print("\n" + "=" * 70)
print("EVALUATION COMPLETED")
print("=" * 70)

print("\nKey cybersecurity result:")

print(
    f"Attack Detection Recall: "
    f"{recall * 100:.2f}%"
)

print(
    f"False Negative Rate: "
    f"{false_negative_rate * 100:.2f}%"
)

print(
    f"False Positive Rate: "
    f"{false_positive_rate * 100:.2f}%"
)

print("\nAll evaluation results saved in:")
print(REPORTS_DIR)
