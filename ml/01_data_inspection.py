import pandas as pd
from pathlib import Path


# ==========================================
# CyberGuard AI
# Step 1: Dataset Inspection
# Dataset: UNSW-NB15
# ==========================================


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Dataset paths
TRAIN_PATH = PROJECT_ROOT / "data" / "raw" / "UNSW_NB15_training-set.csv"
TEST_PATH = PROJECT_ROOT / "data" / "raw" / "UNSW_NB15_testing-set.csv"


# ==========================================
# 1. Check whether files exist
# ==========================================

print("=" * 60)
print("CYBERGUARD AI - DATASET INSPECTION")
print("=" * 60)

print("\nChecking dataset files...")

if not TRAIN_PATH.exists():
    print(f"ERROR: Training file not found:")
    print(TRAIN_PATH)
    raise FileNotFoundError(TRAIN_PATH)

if not TEST_PATH.exists():
    print(f"ERROR: Testing file not found:")
    print(TEST_PATH)
    raise FileNotFoundError(TEST_PATH)

print("Training file found.")
print("Testing file found.")


# ==========================================
# 2. Load datasets
# ==========================================

print("\nLoading datasets...")

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

print("Datasets loaded successfully.")


# ==========================================
# 3. Dataset dimensions
# ==========================================

print("\n" + "=" * 60)
print("DATASET DIMENSIONS")
print("=" * 60)

print(f"Training rows    : {train_df.shape[0]:,}")
print(f"Training columns : {train_df.shape[1]:,}")

print(f"Testing rows     : {test_df.shape[0]:,}")
print(f"Testing columns  : {test_df.shape[1]:,}")


# ==========================================
# 4. Column names
# ==========================================

print("\n" + "=" * 60)
print("COLUMN NAMES")
print("=" * 60)

for number, column in enumerate(train_df.columns, start=1):
    print(f"{number:2}. {column}")


# ==========================================
# 5. First 5 rows
# ==========================================

print("\n" + "=" * 60)
print("FIRST 5 TRAINING RECORDS")
print("=" * 60)

print(train_df.head())


# ==========================================
# 6. Dataset information
# ==========================================

print("\n" + "=" * 60)
print("DATA TYPES AND INFORMATION")
print("=" * 60)

train_df.info()


# ==========================================
# 7. Missing values
# ==========================================

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing_values = train_df.isnull().sum()

print(missing_values[missing_values > 0])

if missing_values.sum() == 0:
    print("No missing values found.")


# ==========================================
# 8. Duplicate records
# ==========================================

print("\n" + "=" * 60)
print("DUPLICATE RECORDS")
print("=" * 60)

duplicate_count = train_df.duplicated().sum()

print(f"Duplicate rows: {duplicate_count:,}")


# ==========================================
# 9. Target columns
# ==========================================

print("\n" + "=" * 60)
print("TARGET COLUMNS")
print("=" * 60)

if "label" in train_df.columns:
    print("\nLabel distribution:")
    print(train_df["label"].value_counts())

    print("\nLabel percentages:")
    print(
        train_df["label"]
        .value_counts(normalize=True)
        .mul(100)
        .round(2)
    )

if "attack_cat" in train_df.columns:
    print("\nAttack category distribution:")
    print(train_df["attack_cat"].value_counts(dropna=False))


# ==========================================
# 10. Data types summary
# ==========================================

print("\n" + "=" * 60)
print("DATA TYPE SUMMARY")
print("=" * 60)

print(train_df.dtypes.value_counts())


# ==========================================
# 11. Numerical statistics
# ==========================================

print("\n" + "=" * 60)
print("NUMERICAL FEATURE SUMMARY")
print("=" * 60)

print(train_df.describe().T)


# ==========================================
# Finished
# ==========================================

print("\n" + "=" * 60)
print("DATASET INSPECTION COMPLETED")
print("=" * 60)