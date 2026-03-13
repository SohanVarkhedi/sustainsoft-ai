import os
import joblib
import pandas as pd

from backend.monitor.process_scanner import get_running_applications
from backend.monitor.resource_monitor import monitor_application
from backend.scoring.sustainability_score import calculate_sustainability_score, efficiency_label
from backend.models.data_logger import log_analysis


MODEL_PATH = "ml/models/sustainsoft_regressor.joblib"

model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)


def main():

    print("\nRunning Applications:\n")

    apps = get_running_applications()

    for app in apps:
        print(app)

    app_name = input("\nEnter application name to analyze: ")

    # Monitor application resources
    stats = monitor_application(app_name)

    # Formula-based sustainability score
    score = calculate_sustainability_score(
        stats["cpu_usage"],
        stats["ram_usage_mb"],
        stats["process_count"],
        stats["disk_io_mb"]
    )

    efficiency = efficiency_label(score)

    # Log data to dataset
    log_analysis(stats, score)

    # ML prediction
    ml_score = None

    if model:
        features = pd.DataFrame([{
            "cpu_usage": stats["cpu_usage"],
            "ram_usage_mb": stats["ram_usage_mb"],
            "process_count": stats["process_count"],
            "disk_io_mb": stats["disk_io_mb"]
        }])

        ml_score = round(model.predict(features)[0], 2)

    # Output results
    print("\nApplication Analysis")
    print("-----------------------")

    print(f"Application: {stats['application']}")
    print(f"CPU Usage: {stats['cpu_usage']} %")
    print(f"RAM Usage: {stats['ram_usage_mb']} MB")
    print(f"Processes: {stats['process_count']}")
    print(f"Disk IO: {stats['disk_io_mb']} MB")

    print("\nFormula Sustainability Score:", score, "/ 10")

    if ml_score is not None:
        print("ML Predicted Score:", ml_score, "/ 10")

    print("Efficiency Level:", efficiency)


if __name__ == "__main__":
    main()