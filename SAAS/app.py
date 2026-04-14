"""
app.py — Flask-додаток для відображення прогнозу повітряних тривог.

Ендпоінти:
  GET  /              — головна сторінка (HTML)
  GET  /api/predict   — старий ендпоінт (для сумісності), повертає весь JSON
  POST /api/forecast  — новий ендпоінт з фільтрацією по регіону
  POST /api/refresh   — перезапускає predict.py та повертає оновлені результати
"""

import json
import os
import subprocess
import sys
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_PATH = os.path.join(BASE_DIR, "data", "results.json")
PREDICT_SCRIPT = os.path.join(BASE_DIR, "predict.py")


def load_results():

    if not os.path.exists(RESULT_PATH):
        return None
    with open(RESULT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def home():
    return render_template("index.html")


def force_run_prediction():

    python_path = sys.executable
    subprocess.run(
        [python_path, PREDICT_SCRIPT],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        timeout=300
    )

@app.route("/api/predict")
def predict():
    """
    GET /api/predict
    """
    force_run_prediction()
    data = load_results()
    if data is None:
        return jsonify({"error": "Прогнози ще не згенеровані"}), 500
    return jsonify(data)


@app.route("/api/forecast", methods=["POST"])
def forecast():
    """
    POST /api/forecast
    """
    force_run_prediction()
    data = load_results()
    if data is None:
        return jsonify({"error": "Прогнози ще не згенеровані"}), 500

    body = request.get_json(silent=True) or {}
    region = body.get("region", "all")


    if region and region.lower() != "all":
        all_forecasts = data.get("regions_forecast", {})


        matched = {k: v for k, v in all_forecasts.items() if k.lower() == region.lower()}

        if not matched:
            available = list(all_forecasts.keys())
            return jsonify({
                "error": f"Регіон '{region}' не знайдений",
                "available_regions": available
            }), 404


        filtered = {
            "last_model_train_time": data.get("last_model_train_time"),
            "last_prediction_time": data.get("last_prediction_time"),
            "model_name": data.get("model_name"),
            "total_regions": 1,
            "regions_forecast": matched
        }
        return jsonify(filtered)


    return jsonify(data)


@app.route("/api/refresh", methods=["POST"])
def refresh():
    """
    POST /api/refresh
    """
    try:
        force_run_prediction()
        data = load_results()
        if data is None:
            return jsonify({"error": "Файл результатів не створено"}), 500

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": f"Помилка запуску: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
