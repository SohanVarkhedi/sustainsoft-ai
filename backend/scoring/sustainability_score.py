def calculate_sustainability_score(cpu, ram_mb, processes, disk_io_mb, total_ram=16000):

    ram_ratio = ram_mb / total_ram

    cpu_pressure = cpu / 100
    ram_pressure = ram_ratio
    process_pressure = processes / 50
    disk_pressure = disk_io_mb / 5000

    resource_pressure = (
        0.35 * cpu_pressure +
        0.35 * ram_pressure +
        0.15 * process_pressure +
        0.15 * disk_pressure
    )

    score = 10 * (1 - resource_pressure)

    if score < 0:
        score = 0

    return round(score, 2)


def efficiency_label(score):

    if score >= 8:
        return "Efficient"

    elif score >= 5:
        return "Moderate"

    else:
        return "Resource Heavy"

if __name__ == "__main__":

    score = calculate_sustainability_score(
        cpu=15.6,
        ram_mb=2271,
        processes=12,
        disk_io_mb=1930
    )

    print("Sustainability Score:", score)
    print("Efficiency:", efficiency_label(score))