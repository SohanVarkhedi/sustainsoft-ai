import csv
import os
from datetime import datetime

LOG_DIR = "data/logs"
LOG_FILE = os.path.join(LOG_DIR, "sustainsoft_dataset.csv")


def log_analysis(stats, score):

    # Ensure directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "application",
                "cpu_usage",
                "ram_usage_mb",
                "process_count",
                "disk_io_mb",
                "sustainability_score",
                "timestamp"
            ])

        writer.writerow([
            stats["application"],
            stats["cpu_usage"],
            stats["ram_usage_mb"],
            stats["process_count"],
            stats["disk_io_mb"],
            score,
            datetime.now()
        ])