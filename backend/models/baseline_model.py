import pandas as pd
import os
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import shap
import matplotlib.pyplot as plt


if __name__ == "__main__":
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

    explainer = shap.Explainer(model, X_train.sample(min(100, len(X_train)), random_state=42))
    shap_values = explainer(X_test.sample(min(50, len(X_test)), random_state=42))

    print("SHAP values shape:", shap_values.values.shape)

    if len(shap_values.values.shape) == 3:
        importance_scores = abs(shap_values.values).mean(axis=(0, 2))
    else:
        importance_scores = abs(shap_values.values).mean(axis=0)

    importance = pd.DataFrame({
        "feature": X.columns,
        "importance": importance_scores
    }).sort_values("importance", ascending=False)
    print("Top 5 important features:")
    print(importance.head())

    top_features = importance.head(10)
    plt.figure(figsize=(10, 6))
    plt.barh(top_features["feature"], top_features["importance"], color="#d85a30")
    plt.xlabel("SHAP Importance (average impact)")
    plt.title("Top 10 Features - Attack Detection (Multi-class)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("shap_importance_chart.png", dpi=150)
    print("Chart saved as shap_importance_chart.png")


def predict(input_df):
    """
    Member 4 isko call karega.
    input_df: pandas DataFrame jisme wahi feature columns hon jo training mein use hue the.
    """
    import joblib as _joblib
    _model = _joblib.load(os.path.join(os.path.dirname(__file__), "model.pkl"))
    _encoder = _joblib.load(os.path.join(os.path.dirname(__file__), "label_encoder.pkl"))
    _cols = _joblib.load(os.path.join(os.path.dirname(__file__), "feature_columns.pkl"))
    input_df = input_df[_cols]
    input_df = input_df.replace([float("inf"), float("-inf")], 0).fillna(0)
    pred_encoded = _model.predict(input_df)
    pred_label = _encoder.inverse_transform(pred_encoded)
    return pred_label
