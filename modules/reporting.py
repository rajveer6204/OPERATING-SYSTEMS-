
"""
OS Resource Management Simulator
Performance Comparison and Report Generation
"""

import os
from datetime import datetime


def generate_comparison_report():
    """Compare the performance of OS algorithms."""

    # CPU Scheduling results from our scheduling module
    scheduling_results = [
        {
            "name": "FCFS",
            "waiting": 3.33,
            "turnaround": 6.67
        },
        {
            "name": "SJF",
            "waiting": 3.00,
            "turnaround": 6.33
        },
        {
            "name": "Round Robin",
            "waiting": 4.00,
            "turnaround": 7.33
        },
        {
            "name": "Priority",
            "waiting": 3.33,
            "turnaround": 6.67
        }
    ]

    # Memory Management results
    memory_results = [
        {"name": "First Fit", "allocated": 3},
        {"name": "Best Fit", "allocated": 4},
        {"name": "Worst Fit", "allocated": 3}
    ]

    # Disk Scheduling results
    disk_results = [
        {"name": "FCFS", "movement": 640},
        {"name": "SSTF", "movement": 236},
        {"name": "SCAN", "movement": 331},
        {"name": "C-SCAN", "movement": 382}
    ]

    lines = []

    lines.append("=" * 55)
    lines.append("OS RESOURCE MANAGEMENT SIMULATOR")
    lines.append("PERFORMANCE COMPARISON REPORT")
    lines.append("=" * 55)

    lines.append(
        "Generated On: " +
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )

    # CPU Scheduling comparison
    lines.append("\n1. CPU SCHEDULING COMPARISON")
    lines.append("-" * 55)
    lines.append(
        f"{'Algorithm':<18}{'Avg Waiting':<16}{'Avg Turnaround'}"
    )

    for result in scheduling_results:
        lines.append(
            f"{result['name']:<18}"
            f"{result['waiting']:<16.2f}"
            f"{result['turnaround']:.2f}"
        )

    best_scheduling = min(
        scheduling_results,
        key=lambda x: x["waiting"]
    )

    lines.append(
        "\nBest Average Waiting Time: "
        + best_scheduling["name"]
    )

    # Memory Management comparison
    lines.append("\n2. MEMORY MANAGEMENT COMPARISON")
    lines.append("-" * 55)
    lines.append(f"{'Algorithm':<18}{'Processes Allocated'}")

    for result in memory_results:
        lines.append(
            f"{result['name']:<18}{result['allocated']}"
        )

    best_memory = max(
        memory_results,
        key=lambda x: x["allocated"]
    )

    lines.append(
        "\nBest Allocation Result: "
        + best_memory["name"]
    )

    # Disk Scheduling comparison
    lines.append("\n3. DISK SCHEDULING COMPARISON")
    lines.append("-" * 55)
    lines.append(f"{'Algorithm':<18}{'Head Movement'}")

    for result in disk_results:
        lines.append(
            f"{result['name']:<18}{result['movement']} tracks"
        )

    best_disk = min(
        disk_results,
        key=lambda x: x["movement"]
    )

    lines.append(
        "\nLowest Head Movement: "
        + best_disk["name"]
    )

    # Final summary
    lines.append("\n4. OVERALL PERFORMANCE SUMMARY")
    lines.append("-" * 55)
    lines.append(
        f"CPU Scheduling: {best_scheduling['name']} "
        "has the lowest average waiting time."
    )
    lines.append(
        f"Memory Management: {best_memory['name']} "
        "allocated the most processes."
    )
    lines.append(
        f"Disk Scheduling: {best_disk['name']} "
        "has the lowest head movement."
    )

    lines.append("\n" + "=" * 55)
    lines.append("END OF REPORT")
    lines.append("=" * 55)

    return "\n".join(lines)


def save_report(report):
    """Save the performance report inside reports folder."""

    os.makedirs("reports", exist_ok=True)

    file_path = os.path.join(
        "reports",
        "performance_report.txt"
    )

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(report)

    return file_path


def main():
    print("\nOS RESOURCE MANAGEMENT SIMULATOR")
    print("PERFORMANCE REPORT MODULE")

    report = generate_comparison_report()

    print(report)

    file_path = save_report(report)

    print("\nReport successfully saved!")
    print("File Location:", file_path)


if __name__ == "__main__":
    main()
