import psutil
import time


def monitor_application(app_name):
    cpu_total = 0
    ram_total = 0
    process_count = 0
    read_bytes = 0
    write_bytes = 0

    processes = []

    # Step 1: Collect all processes matching the application
    for process in psutil.process_iter(['name', 'memory_info', 'io_counters']):
        try:
            name = process.info['name']

            if name and name.lower() == app_name.lower():
                processes.append(process)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Step 2: Initialize CPU measurement
    for p in processes:
        try:
            p.cpu_percent(None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Wait for sampling window
    time.sleep(1)

    # Step 3: Measure CPU usage
    for p in processes:
        try:
            cpu_total += p.cpu_percent(None)

            ram_total += p.memory_info().rss

            io = p.io_counters()
            if io:
                read_bytes += io.read_bytes
                write_bytes += io.write_bytes

            process_count += 1

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Convert values
    ram_mb = ram_total / (1024 * 1024)
    disk_io_mb = (read_bytes + write_bytes) / (1024 * 1024)

    return {
        "application": app_name,
        "cpu_usage": round(cpu_total, 2),
        "ram_usage_mb": round(ram_mb, 2),
        "process_count": process_count,
        "disk_io_mb": round(disk_io_mb, 2)
    }


if __name__ == "__main__":
    app = input("Enter application name (example: chrome.exe): ")

    stats = monitor_application(app)

    print("\nApplication Analysis\n")
    print("-------------------------")

    print(f"Application: {stats['application']}")
    print(f"CPU Usage: {stats['cpu_usage']} %")
    print(f"RAM Usage: {stats['ram_usage_mb']} MB")
    print(f"Processes: {stats['process_count']}")
    print(f"Disk IO: {stats['disk_io_mb']} MB")