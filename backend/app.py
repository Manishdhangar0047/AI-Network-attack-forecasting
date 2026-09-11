"""
Backend server - SIH26153 project
Ye Flask API server hai. Frontend isse baat karega.

Chalane ke liye: python app.py
Phir browser mein http://localhost:5000 pe check kar sakte ho ki server chal raha hai.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ye zaroori hai taaki frontend (alag port pe chalne wala) backend ko call kar sake


@app.route("/", methods=["GET"])
def home():
    """Simple check - server chal raha hai ya nahi"""
    return jsonify({"status": "Backend chal raha hai!"})


@app.route("/predict", methods=["POST"])
def predict():
    """
    Frontend yahan file bhejega (CSV/PCAP).
    Abhi ye sirf dummy response bhej raha hai - jab Member 2,3,4 apna
    model/forecasting/explainability code likh lenge, tab isme unke
    functions call karenge.
    """
    # Step 1: file receive karo
    if "file" not in request.files:
        return jsonify({"error": "Koi file nahi mili"}), 400

    uploaded_file = request.files["file"]

    # TODO (Member 1): yahan feature_extraction.py ka function call karo
    # features = extract_features(uploaded_file)

    # TODO (Member 2/3): yahan world_model.py se prediction lo
    # prediction = world_model.predict(features)

    # TODO (Member 4): yahan forecast_engine.py se K-step forecast + MITRE stage lo
    # forecast_result = forecast_engine.run(prediction)

    # TODO (Member 3): yahan shap_explain.py se explanation lo
    # explanation = shap_explain.get_top_features(features)

    # Abhi ke liye dummy data bhej rahe hain - isse frontend test kar sakte ho
    dummy_response = {
        "filename": uploaded_file.filename,
        "infiltration_probability": [0.1, 0.15, 0.4, 0.7, 0.85],
        "predicted_stage": "Lateral Movement",
        "top_features": ["failed_login_count", "syn_flag_ratio", "packet_iat_variance"]
    }

    return jsonify(dummy_response)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
