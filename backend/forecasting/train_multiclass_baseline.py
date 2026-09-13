# backend/forecasting/train_multiclass_baseline.py
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv("../../sample_dataset/network_traffic_sample.csv")

X = df.select_dtypes(include=["number"])
y = df["Label"]  # multi-class — original attack type labels

X = X.replace([float("inf"), float("-inf")], 0).fillna(0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
print("Multi-class accuracy:", model.score(X_test, y_test))

joblib.dump(model, "baseline_multiclass.pkl")
print("Feature columns order:", list(X.columns))