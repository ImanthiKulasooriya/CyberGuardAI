import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ==========================================================
# CyberGuard AI
# Step 2: Exploratory Data Analysis
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

REPORTS_DIR = PROJECT_ROOT / "reports"

REPORTS_DIR.mkdir(exist_ok=True)


# ----------------------------------------------------------
# 2. Load dataset
# ----------------------------------------------------------

print("=" * 60)
print("CYBERGUARD AI - EXPLORATORY DATA ANALYSIS")
print("=" * 60)

print("\nLoading training dataset...")

df = pd.read_csv(TRAIN_PATH)

print(f"Dataset loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")


# ==========================================================
# 3. Class Distribution
# ==========================================================

print("\n" + "=" * 60)
print("1. NORMAL VS ATTACK TRAFFIC")
print("=" * 60)

label_counts = df["label"].value_counts()

print(label_counts)

plt.figure(figsize=(8, 6))

labels = ["Attack", "Normal"]
values = [
    label_counts.get(1, 0),
    label_counts.get(0, 0)
]

plt.bar(labels, values)

plt.title("Normal vs Attack Network Traffic")
plt.xlabel("Traffic Type")
plt.ylabel("Number of Records")

plt.tight_layout()

plt.savefig(
    REPORTS_DIR / "01_normal_vs_attack.png",
    dpi=300
)

plt.show()


# ==========================================================
# 4. Attack Category Distribution
# ==========================================================

print("\n" + "=" * 60)
print("2. ATTACK CATEGORY DISTRIBUTION")
print("=" * 60)

attack_counts = df["attack_cat"].value_counts()

print(attack_counts)

plt.figure(figsize=(10, 6))

attack_counts.plot(kind="bar")

plt.title("Distribution of Network Traffic by Attack Category")
plt.xlabel("Attack Category")
plt.ylabel("Number of Records")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    REPORTS_DIR / "02_attack_categories.png",
    dpi=300
)

plt.show()


# ==========================================================
# 5. Protocol Distribution
# ==========================================================

print("\n" + "=" * 60)
print("3. TOP NETWORK PROTOCOLS")
print("=" * 60)

protocol_counts = df["proto"].value_counts().head(15)

print(protocol_counts)

plt.figure(figsize=(10, 6))

protocol_counts.plot(kind="bar")

plt.title("Top 15 Network Protocols")
plt.xlabel("Protocol")
plt.ylabel("Number of Records")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    REPORTS_DIR / "03_top_protocols.png",
    dpi=300
)

plt.show()


# ==========================================================
# 6. Service Distribution
# ==========================================================

print("\n" + "=" * 60)
print("4. TOP NETWORK SERVICES")
print("=" * 60)

service_counts = df["service"].value_counts().head(15)

print(service_counts)

plt.figure(figsize=(10, 6))

service_counts.plot(kind="bar")

plt.title("Top 15 Network Services")
plt.xlabel("Service")
plt.ylabel("Number of Records")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    REPORTS_DIR / "04_top_services.png",
    dpi=300
)

plt.show()


# ==========================================================
# 7. Traffic State Distribution
# ==========================================================

print("\n" + "=" * 60)
print("5. CONNECTION STATE DISTRIBUTION")
print("=" * 60)

state_counts = df["state"].value_counts()

print(state_counts)

plt.figure(figsize=(10, 6))

state_counts.plot(kind="bar")

plt.title("Network Connection State Distribution")
plt.xlabel("Connection State")
plt.ylabel("Number of Records")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    REPORTS_DIR / "05_connection_states.png",
    dpi=300
)

plt.show()


# ==========================================================
# 8. Attack Categories Excluding Normal
# ==========================================================

print("\n" + "=" * 60)
print("6. ATTACK TYPES ONLY")
print("=" * 60)

attack_only = df[df["label"] == 1]

attack_only_counts = attack_only["attack_cat"].value_counts()

print(attack_only_counts)

plt.figure(figsize=(10, 6))

attack_only_counts.plot(kind="bar")

plt.title("Distribution of Attack Types")
plt.xlabel("Attack Type")
plt.ylabel("Number of Attack Records")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    REPORTS_DIR / "06_attack_types_only.png",
    dpi=300
)

plt.show()


# ==========================================================
# 9. Numerical Feature Distributions
# ==========================================================

print("\n" + "=" * 60)
print("7. NUMERICAL FEATURE DISTRIBUTIONS")
print("=" * 60)

features = [
    "dur",
    "spkts",
    "dpkts",
    "sbytes",
    "dbytes",
    "rate"
]

for feature in features:

    if feature not in df.columns:
        continue

    plt.figure(figsize=(8, 5))

    plt.hist(
        df[feature],
        bins=50
    )

    plt.title(f"Distribution of {feature}")

    plt.xlabel(feature)
    plt.ylabel("Frequency")

    plt.tight_layout()

    filename = f"07_distribution_{feature}.png"

    plt.savefig(
        REPORTS_DIR / filename,
        dpi=300
    )

    plt.show()


# ==========================================================
# 10. Correlation Matrix
# ==========================================================

print("\n" + "=" * 60)
print("8. CORRELATION ANALYSIS")
print("=" * 60)

numeric_df = df.select_dtypes(include=["int64", "float64"])

correlation = numeric_df.corr()

plt.figure(figsize=(14, 10))

plt.imshow(
    correlation,
    aspect="auto"
)

plt.colorbar()

plt.title("Correlation Matrix of Numerical Features")

plt.tight_layout()

plt.savefig(
    REPORTS_DIR / "08_correlation_matrix.png",
    dpi=300
)

plt.show()


# ==========================================================
# 11. Correlation with Target
# ==========================================================

print("\n" + "=" * 60)
print("9. FEATURE CORRELATION WITH LABEL")
print("=" * 60)

target_correlation = (
    numeric_df
    .corr()["label"]
    .sort_values(ascending=False)
)

print(target_correlation)


# ==========================================================
# 12. Save correlation results
# ==========================================================

target_correlation.to_csv(
    REPORTS_DIR / "feature_label_correlations.csv"
)


# ==========================================================
# Finished
# ==========================================================

print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nGraphs saved to:")

print(REPORTS_DIR)