import pandas as pd
import os

# Dataset folder ka path
dataset_path = os.path.join("..", "..", "dataset")

# CSV files find karo
files = [f for f in os.listdir(dataset_path) if f.endswith(".csv")]

print("Total CSV files:", len(files))

# Pehli CSV read karo
file_path = os.path.join(dataset_path, files[0])
df = pd.read_csv(file_path)

print("\nFile:", files[0])
print("Rows:", len(df))
print("Columns:", len(df.columns))

# Label column
label_column = "Label"

# Normal traffic
normal_data = df[df[label_column] == "Benign"]

# Attack traffic
attack_data = df[df[label_column] != "Benign"]

print("\n===== NORMAL TRAFFIC =====")
print("Normal rows:", len(normal_data))
print(normal_data.head())

print("\n===== ATTACK TRAFFIC =====")
print("Attack rows:", len(attack_data))
print(attack_data.head())

# Label distribution
print("\n===== LABEL DISTRIBUTION =====")
print(df[label_column].value_counts())