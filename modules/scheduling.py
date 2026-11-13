
# ==========================================
# OS RESOURCE MANAGEMENT SIMULATOR
# MODULE: CPU PROCESS SCHEDULING
# ==========================================


# Common input validation
def validate_processes(processes):

    if not processes:
        raise ValueError("At least one process is required")

    ids = []

    for p in processes:

        for key in ["pid", "arrival", "burst"]:
            if key not in p:
                raise ValueError(f"Missing {key} in process")

        if p["pid"] in ids:
            raise ValueError("Process IDs must be unique")

        ids.append(p["pid"])

        if p["arrival"] < 0:
            raise ValueError("Arrival time cannot be negative")

        if p["burst"] <= 0:
            raise ValueError("Burst time must be greater than zero")


# ==========================================
# 1. FCFS SCHEDULING
# FIRST COME FIRST SERVE
# ==========================================

def fcfs_scheduling(processes):

    validate_processes(processes)

    processes = sorted(
        processes,
        key=lambda p: p["arrival"]
    )

    current_time = 0
    results = []
    gantt_chart = []

    for p in processes:

        start = max(current_time, p["arrival"])
        completion = start + p["burst"]

        waiting = start - p["arrival"]
        turnaround = completion - p["arrival"]

        results.append({
            "pid": p["pid"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "start": start,
            "completion": completion,
            "waiting": waiting,
            "turnaround": turnaround
        })

        gantt_chart.append({
            "pid": p["pid"],
            "start": start,
            "end": completion
        })

        current_time = completion

    return results, gantt_chart


# ==========================================
# 2. SJF SCHEDULING
# SHORTEST JOB FIRST (NON-PREEMPTIVE)
# ==========================================

def sjf_scheduling(processes):

    validate_processes(processes)

    remaining = processes.copy()
    results = []
    gantt_chart = []
    current_time = 0

    while remaining:

        available = [
            p for p in remaining
            if p["arrival"] <= current_time
        ]

        if not available:

            current_time = min(
                p["arrival"] for p in remaining
            )

            continue

        selected = min(
            available,
            key=lambda p: (p["burst"], p["arrival"])
        )

        start = current_time
        completion = start + selected["burst"]

        waiting = start - selected["arrival"]
        turnaround = completion - selected["arrival"]

        results.append({
            "pid": selected["pid"],
            "arrival": selected["arrival"],
            "burst": selected["burst"],
            "start": start,
            "completion": completion,
            "waiting": waiting,
            "turnaround": turnaround
        })

        gantt_chart.append({
            "pid": selected["pid"],
            "start": start,
            "end": completion
        })

        current_time = completion
        remaining.remove(selected)

    return results, gantt_chart


# ==========================================
# 3. ROUND ROBIN SCHEDULING
# ==========================================

def round_robin_scheduling(processes, quantum):

    validate_processes(processes)

    if quantum <= 0:
        raise ValueError("Time quantum must be positive")

    remaining = {
        p["pid"]: p["burst"] for p in processes
    }

    completed = {}
    ready_queue = []
    results = []
    gantt_chart = []

    pending = sorted(
        processes,
        key=lambda p: p["arrival"]
    )

    current_time = 0
    index = 0

    while len(completed) < len(processes):

        while (
            index < len(pending)
            and pending[index]["arrival"] <= current_time
        ):

            ready_queue.append(pending[index]["pid"])
            index += 1

        if not ready_queue:

            current_time = pending[index]["arrival"]
            continue

        pid = ready_queue.pop(0)

        start = current_time

        execution = min(
            quantum,
            remaining[pid]
        )

        current_time += execution
        remaining[pid] -= execution

        gantt_chart.append({
            "pid": pid,
            "start": start,
            "end": current_time
        })

        while (
            index < len(pending)
            and pending[index]["arrival"] <= current_time
        ):

            ready_queue.append(pending[index]["pid"])
            index += 1

        if remaining[pid] > 0:

            ready_queue.append(pid)

        else:

            completed[pid] = current_time

    for p in processes:

        completion = completed[p["pid"]]

        turnaround = completion - p["arrival"]
        waiting = turnaround - p["burst"]

        results.append({
            "pid": p["pid"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "start": None,
            "completion": completion,
            "waiting": waiting,
            "turnaround": turnaround
        })

    return results, gantt_chart


# ==========================================
# 4. PRIORITY SCHEDULING
# NON-PREEMPTIVE
# SMALLER NUMBER = HIGHER PRIORITY
# ==========================================

def priority_scheduling(processes):

    validate_processes(processes)

    for p in processes:

        if "priority" not in p:
            raise ValueError("Priority is required")

    remaining = processes.copy()

    results = []
    gantt_chart = []
    current_time = 0

    while remaining:

        available = [
            p for p in remaining
            if p["arrival"] <= current_time
        ]

        if not available:

            current_time = min(
                p["arrival"] for p in remaining
            )

            continue

        selected = min(
            available,
            key=lambda p: (p["priority"], p["arrival"])
        )

        start = current_time
        completion = start + selected["burst"]

        waiting = start - selected["arrival"]
        turnaround = completion - selected["arrival"]

        results.append({
            "pid": selected["pid"],
            "arrival": selected["arrival"],
            "burst": selected["burst"],
            "start": start,
            "completion": completion,
            "waiting": waiting,
            "turnaround": turnaround
        })

        gantt_chart.append({
            "pid": selected["pid"],
            "start": start,
            "end": completion
        })

        current_time = completion
        remaining.remove(selected)

    return results, gantt_chart


# ==========================================
# 5. DISPLAY RESULTS
# ==========================================

def display_results(name, results, gantt_chart):

    print("\n========================================")
    print(name)
    print("========================================")

    print("\nPID\tAT\tBT\tCT\tWT\tTAT")

    for p in results:

        print(
            f"{p['pid']}\t"
            f"{p['arrival']}\t"
            f"{p['burst']}\t"
            f"{p['completion']}\t"
            f"{p['waiting']}\t"
            f"{p['turnaround']}"
        )

    avg_waiting = sum(
        p["waiting"] for p in results
    ) / len(results)

    avg_turnaround = sum(
        p["turnaround"] for p in results
    ) / len(results)

    print("\nGANTT CHART")

    for item in gantt_chart:
        print(f"| {item['pid']} ", end="")

    if gantt_chart:

        print("|")
        print(gantt_chart[0]["start"], end="")

        for item in gantt_chart:
            print(f" ---- {item['end']}", end="")

    print("\n")

    print("Average Waiting Time:", round(avg_waiting, 2))

    print(
        "Average Turnaround Time:",
        round(avg_turnaround, 2)
    )


# ==========================================
# 6. MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    processes = [
        {"pid": "P1", "arrival": 0, "burst": 5, "priority": 2},
        {"pid": "P2", "arrival": 1, "burst": 3, "priority": 1},
        {"pid": "P3", "arrival": 2, "burst": 2, "priority": 3}
    ]

    print("\nOS RESOURCE MANAGEMENT SIMULATOR")
    print("CPU PROCESS SCHEDULING MODULE")

    # FCFS
    result, chart = fcfs_scheduling(processes)
    display_results("FCFS SCHEDULING", result, chart)

    # SJF
    result, chart = sjf_scheduling(processes)
    display_results("SJF SCHEDULING", result, chart)

    # Round Robin
    result, chart = round_robin_scheduling(
        processes, quantum=2
    )
    display_results("ROUND ROBIN SCHEDULING", result, chart)

    # Priority
    result, chart = priority_scheduling(processes)
    display_results("PRIORITY SCHEDULING", result, chart)
