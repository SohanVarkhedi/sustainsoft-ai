from flask import Flask, jsonify, request, send_from_directory
import joblib
import os
import pandas as pd

from backend.monitor.process_scanner import get_running_applications
from backend.monitor.resource_monitor import monitor_application
from backend.scoring.sustainability_score import calculate_sustainability_score, efficiency_label
from backend.models.data_logger import log_analysis


app = Flask(__name__)

# Load ML model
MODEL_PATH = "ml/models/sustainsoft_regressor.joblib"

model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)


# Serve frontend
@app.route("/")
def home():
    return send_from_directory(
        r"C:\Users\sohan\Desktop\sustainsoft-ai\frontend",
        "sustainsoft.html"
    )


# List running applications
@app.route("/apps", methods=["GET"])
def list_apps():
    apps = get_running_applications()
    return jsonify(apps)


# Analyze application
@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json
    app_name = data["application"]

    stats = monitor_application(app_name)

    score = calculate_sustainability_score(
        stats["cpu_usage"],
        stats["ram_usage_mb"],
        stats["process_count"],
        stats["disk_io_mb"]
    )

    efficiency = efficiency_label(score)

    # Save data to dataset
    log_analysis(stats, score)

    ml_score = None

    if model:
        features = pd.DataFrame([{
            "cpu_usage": stats["cpu_usage"],
            "ram_usage_mb": stats["ram_usage_mb"],
            "process_count": stats["process_count"],
            "disk_io_mb": stats["disk_io_mb"]
        }])

        ml_score = round(model.predict(features)[0], 2)

    return jsonify({
        "application": stats["application"],
        "cpu_usage": stats["cpu_usage"],
        "ram_usage_mb": stats["ram_usage_mb"],
        "process_count": stats["process_count"],
        "disk_io_mb": stats["disk_io_mb"],
        "formula_score": score,
        "ml_score": ml_score,
        "efficiency": efficiency
    })


if __name__ == "__main__":
    app.run(debug=True)