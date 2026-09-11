import pandas as pd
import glob
import os

# Original dataset
dataset_path = "dataset"

# Sample dataset folder
sample_path = "sample_dataset"
os.makedirs(sample_path, exist_ok=True)

# Output file
output_file = os.path.join(
    sample_path,
    "network_traffic_sample.csv"
)

# Purani sample file remove karo
if os.path.exists(output_file):
    os.remove(output_file)

# Har label se maximum rows
SAMPLE_PER_LABEL = 1000

# Temporary storage
samples = {}

# CSV files
files = glob.glob(
    os.path.join(dataset_path, "*.csv")
)

print("Total CSV files:", len(files))
print("\nCreating balanced sample...")

# ------------------------------------------------
# CSV files ko ek-ek karke chunks mein read karo
# ------------------------------------------------

for file in files:

    print("\nReading:", os.path.basename(file))

    for chunk in pd.read_csv(
        file,
        chunksize=100000
    ):

        # Column names clean
        chunk.columns = chunk.columns.str.strip()

        # Invalid labels remove
        chunk = chunk[
            chunk["Label"].notna()
        ]

        chunk = chunk[
            chunk["Label"].astype(str).str.strip().str.lower()
            != "label"
        ]

        # Har label ka data
        for label in chunk["Label"].unique():

            label_data = chunk[
                chunk["Label"] == label
            ]

            # Agar already 1000 rows hain
            current_count = len(
                samples.get(label, [])
            )

            if current_count >= SAMPLE_PER_LABEL:
                continue

            remaining = (
                SAMPLE_PER_LABEL - current_count
            )

            selected = label_data.sample(
                n=min(remaining, len(label_data)),
                random_state=42
            )

            if label not in samples:
                samples[label] = []

            samples[label].append(selected)

# ------------------------------------------------
# Samples combine karo
# ------------------------------------------------

all_samples = []

for label, data_parts in samples.items():

    label_sample = pd.concat(
        data_parts,
        ignore_index=True
    )

    # Maximum 1000 rows
    label_sample = label_sample.head(
        SAMPLE_PER_LABEL
    )

    all_samples.append(label_sample)

# Final dataset
sample_data = pd.concat(
    all_samples,
    ignore_index=True
)

# Random shuffle
sample_data = sample_data.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# Save
sample_data.to_csv(
    output_file,
    index=False
)

# ------------------------------------------------
# Result
# ------------------------------------------------

print("\n================================")
print("SAMPLE DATASET CREATED")
print("================================")

print("Total rows:", len(sample_data))
print("Total columns:", len(sample_data.columns))

print("\nLabel distribution:")
print(
    sample_data["Label"].value_counts()
)

print("\nSaved at:")
print(output_file)