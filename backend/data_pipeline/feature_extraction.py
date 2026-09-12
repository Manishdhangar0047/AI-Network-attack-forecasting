import pandas as pd
import glob
import os

# Dataset folder
dataset_path = "dataset"

# Processed data folder
processed_path = "processed_data"
os.makedirs(processed_path, exist_ok=True)

# Saari CSV files
files = glob.glob(os.path.join(dataset_path, "*.csv"))

print("Total CSV files:", len(files))

# Final output file
output_file = os.path.join(
    processed_path,
    "network_traffic_processed.csv"
)

# Agar purani incomplete file hai to remove karo
if os.path.exists(output_file):
    os.remove(output_file)

first_file = True
total_rows = 0

# Har CSV ko ek-ek karke process karo
for file in files:

    print("\n================================")
    print("Processing:", os.path.basename(file))
    print("================================")

    # CSV ko chunks mein read karo
    for chunk in pd.read_csv(file, chunksize=100000):

        # Extra columns remove karo
        extra_columns = [
            "Flow ID",
            "Src IP",
            "Src Port",
            "Dst IP"
        ]

        chunk = chunk.drop(
            columns=extra_columns,
            errors="ignore"
        )

        # Column names clean karo
        chunk.columns = chunk.columns.str.strip()

        # Infinity ko NaN mein convert karo
        chunk = chunk.replace(
            [float("inf"), float("-inf")],
            pd.NA
        )

        # Missing rows remove karo
        chunk = chunk.dropna()

        # Duplicate rows remove karo
        chunk = chunk.drop_duplicates()

        # Target column create karo
        chunk["Target"] = chunk["Label"].apply(
            lambda x: 0
            if str(x).strip().lower() == "benign"
            else 1
        )

        # Timestamp aur original Label remove karo
        chunk = chunk.drop(
            columns=["Timestamp", "Label"],
            errors="ignore"
        )

        # Sirf numeric columns rakho
        numeric_columns = chunk.select_dtypes(
            include=["number"]
        ).columns

        chunk = chunk[numeric_columns]

        # Processed data save karo
        chunk.to_csv(
            output_file,
            mode="w" if first_file else "a",
            header=first_file,
            index=False
        )

        first_file = False
        total_rows += len(chunk)

        print("Processed rows:", total_rows)

print("\n================================")
print("SUCCESS")
print("================================")

print("Total processed rows:", total_rows)
print("Processed dataset:")
print(output_file)