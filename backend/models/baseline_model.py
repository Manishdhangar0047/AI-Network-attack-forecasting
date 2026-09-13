import pandas as pd
import os
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import shap
import matplotlib.pyplot as plt

dataset_path = os.path.join("..", "sample_dataset", "network_traffic_sample.csv")
df = pd.read_csv(dataset_path)

print("Rows:", len(df))
print("Label distribution:")
print(df["Label"].value_counts())

X = df.select_dtypes(include=["number"])
y_raw = df["Label"]

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y_raw)

X = X.replace([float("inf"), float("-inf")], 0)
X = X.fillna(0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
print("Accuracy:", model.score(X_test, y_test))

joblib.dump(model, "model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")
joblib.dump(X.columns.tolist(), "feature_columns.pkl")
print("Saved: model.pkl, label_encoder.pkl, feature_columns.pkl")


def predict(input_df):
    input_df = input_df[X.columns]
    input_df = input_df.replace([float("inf"), float("-inf")], 0).fillna(0)
    pred_encoded = model.predict(input_df)
    pred_label = label_encoder.inverse_transform(pred_encoded)
    return pred_label


df["Label_binary"] = df["Label"].apply(lambda x: 0 if str(x).strip() == "Benign" else 1)
X_train_bin, X_test_bin, y_train_bin, y_test_bin = train_test_split(
    X, df["Label_binary"], test_size=0.2, random_state=42
)
binary_model = LogisticRegression(max_iter=1000)
binary_model.fit(X_train_bin, y_train_bin)

explainer = shap.Explainer(binary_model, X_train_bin.sample(min(100, len(X_train_bin)), random_state=42))
shap_values = explainer(X_test_bin.sample(min(50, len(X_test_bin)), random_state=42))

importance = pd.DataFrame({
    "feature": X.columns,
    "importance": abs(shap_values.values).mean(axis=0)
}).sort_values("importance", ascending=False)
print("Top 5 important features:")
print(importance.head())

top_features = importance.head(10)
plt.figure(figsize=(10, 6))
plt.barh(top_features["feature"], top_features["importance"], color="#d85a30")
plt.xlabel("SHAP Importance (average impact)")
plt.title("Top 10 Features - Attack Detection")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("shap_importance_chart.png", dpi=150)
print("Chart saved as shap_importance_chart.png")
