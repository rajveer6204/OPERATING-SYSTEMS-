
import threading
import multiprocessing
from collections import deque


# ---------- Scheduling Metrics ----------
def calculate_metrics(processes, quantum):
    # Process format: [PID, Arrival Time, Burst Time, Priority]
    results = {}

    def show_results(name, gantt):
        print(f"\n--- {name} ---")
        print("Gantt Chart:")
        for pid, start, end in gantt:
            print(f"| {pid} [{start}-{end}] ", end="")
        print("|")

        for pid, start, end in gantt:
            if pid == "IDLE":
                print(f"CPU Idle: {start} to {end}")

    # FCFS scheduling
    time = 0
    gantt = []
    for pid, at, bt, priority in sorted(processes, key=lambda p: p[1]):
        if time < at:
            gantt.append(("IDLE", time, at))
            time = at
        start = time
        time += bt
        results[pid] = {
            "CT": time,
            "TAT": time - at,
            "WT": time - at - bt,
            "RT": start - at
        }
        gantt.append((pid, start, time))

    show_results("FCFS Scheduling", gantt)
    print("PID\tCT\tTAT\tWT\tRT")
    for pid, at, bt, priority in processes:
        print(pid, *results[pid].values(), sep="\t")

    print("Average TAT:", sum(r["TAT"] for r in results.values()) / len(results))
    print("Average WT:", sum(r["WT"] for r in results.values()) / len(results))
    print("Average RT:", sum(r["RT"] for r in results.values()) / len(results))

    # Round Robin scheduling
    print("\n--- Round Robin Scheduling ---")
    remaining = {p[0]: p[2] for p in processes}
    first_start = {}
    rr_results = {}
    gantt = []
    jobs = sorted(processes, key=lambda p: p[1])
    ready = deque()
    time = 0
    i = 0

    while i < len(jobs) or ready:
        if not ready and i < len(jobs) and time < jobs[i][1]:
            gantt.append(("IDLE", time, jobs[i][1]))
            time = jobs[i][1]

        while i < len(jobs) and jobs[i][1] <= time:
            ready.append(jobs[i])
            i += 1

        if not ready:
            continue

        p = ready.popleft()
        pid, at, bt, priority = p
        first_start.setdefault(pid, time)
        start = time
        run = min(quantum, remaining[pid])
        time += run
        remaining[pid] -= run
        gantt.append((pid, start, time))

        while i < len(jobs) and jobs[i][1] <= time:
            ready.append(jobs[i])
            i += 1

        if remaining[pid] > 0:
            ready.append(p)
        else:
            rr_results[pid] = {
                "CT": time,
                "TAT": time - at,
                "WT": time - at - bt,
                "RT": first_start[pid] - at
            }

    show_results("Round Robin Scheduling", gantt)
    print("PID\tCT\tTAT\tWT\tRT")
    for pid, at, bt, priority in processes:
        print(pid, *rr_results[pid].values(), sep="\t")

    n = len(processes)
    print("Average TAT:", sum(r["TAT"] for r in rr_results.values()) / n)
    print("Average WT:", sum(r["WT"] for r in rr_results.values()) / n)
    print("Average RT:", sum(r["RT"] for r in rr_results.values()) / n)


# ---------- Multithreading ----------
def thread_work(name, count):
    print(f"Thread {name}, ID: {threading.get_ident()}")
    total = sum(range(1, count + 1))
    print(f"Thread {name} completed work: sum = {total}")


# ---------- Inter-Process Communication ----------
def sender(queue):
    message = "Hello from Sender Process"
    print("Sender Process: Sending:", message)
    queue.put(message)


def receiver(queue):
    message = queue.get()
    print("Receiver Process: Received:", message)


if __name__ == "__main__":
    processes = [
        ("P1", 0, 5, 2),
        ("P2", 1, 3, 1),
        ("P3", 2, 4, 3),
        ("P4", 8, 2, 2)
    ]

    quantum = 2
    calculate_metrics(processes, quantum)

    print("\n--- Multithreading Demo ---")
    t1 = threading.Thread(target=thread_work, args=("T1", 5))
    t2 = threading.Thread(target=thread_work, args=("T2", 10))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("Both threads completed.")

    print("\n--- IPC using Multiprocessing Queue ---")
    queue = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=sender, args=(queue,))
    p2 = multiprocessing.Process(target=receiver, args=(queue,))

    p1.start()
    p1.join()
    p2.start()
    p2.join()
    queue.close()
    print("IPC communication completed.")
