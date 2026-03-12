from backend.monitor.process_scanner import get_running_applications
from backend.monitor.resource_monitor import monitor_application
from backend.scoring.sustainability_score import calculate_sustainability_score, efficiency_label
from backend.models.data_logger import log_analysis


def main():

    print("\nRunning Applications:\n")

    apps = get_running_applications()

    for app in apps:
        print(app)

    app_name = input("\nEnter application name to analyze: ")

    stats = monitor_application(app_name)

    score = calculate_sustainability_score(
        stats["cpu_usage"],
        stats["ram_usage_mb"],
        stats["process_count"],
        stats["disk_io_mb"]
    )
    log_analysis(stats, score)
    efficiency = efficiency_label(score)

    print("\nApplication Analysis\n")
    print("-----------------------")

    print(f"Application: {stats['application']}")
    print(f"CPU Usage: {stats['cpu_usage']} %")
    print(f"RAM Usage: {stats['ram_usage_mb']} MB")
    print(f"Processes: {stats['process_count']}")
    print(f"Disk IO: {stats['disk_io_mb']} MB")

    print("\nSustainability Score:", score, "/ 10")
    print("Efficiency Level:", efficiency)


if __name__ == "__main__":
    main()