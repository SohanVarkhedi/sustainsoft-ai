import psutil

def get_running_applications():
    apps = set()

    for process in psutil.process_iter(['name']):
        try:
            name = process.info['name']

            if name and name.endswith(".exe"):
                apps.add(name.lower())

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return sorted(apps)


if __name__ == "__main__":
    applications = get_running_applications()

    print("\nRunning Applications:\n")

    for app in applications:
        print(app)

    print(f"\nTotal Applications Detected: {len(applications)}")