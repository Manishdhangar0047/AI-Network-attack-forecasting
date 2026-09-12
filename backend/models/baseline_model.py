import pandas as pd
import os
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import shap

dataset_path = os.path.join("..", "sample_dataset", "network_traffic_sample.csv")
df = pd.read_csv(dataset_path)

print("Rows:", len(df))
print("Label distribution:")
print(df["Label"].value_counts())

df["Label_binary"] = df["Label"].apply(lambda x: 0 if str(x).strip() == "Benign" else 1)

X = df.select_dtypes(include=["number"]).drop(columns=["Label_binary"], errors="ignore")
y = df["Label_binary"]

X = X.replace([float("inf"), float("-inf")], 0)
X = X.fillna(0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
print("Accuracy:", model.score(X_test, y_test))

explainer = shap.Explainer(model, X_train.sample(min(100, len(X_train)), random_state=42))
shap_values = explainer(X_test.sample(min(50, len(X_test)), random_state=42))
print("SHAP values shape:", shap_values.values.shape)

importance = pd.DataFrame({
    "feature": X.columns,
    "importance": abs(shap_values.values).mean(axis=0)
}).sort_values("importance", ascending=False)
print("Top 5 important features:")
print(importance.head())
import matplotlib.pyplot as plt

top_features = importance.head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_features["feature"], top_features["importance"], color="#d85a30")
plt.xlabel("SHAP Importance (average impact)")
plt.title("Top 10 Features - Attack Detection")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("shap_importance_chart.png", dpi=150)
print("Chart saved as shap_importance_chart.png")
