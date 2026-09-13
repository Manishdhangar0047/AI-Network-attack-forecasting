from flask import Flask, jsonify
from flask_cors import CORS
from forecasting.forecast_engine import run_forecast

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "backend running"})

@app.route("/predict", methods=["GET", "POST"])
def predict():
    result = run_forecast()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)