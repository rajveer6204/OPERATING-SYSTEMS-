
"""
OS RESOURCE MANAGEMENT SIMULATOR
Complete Single File Project

Modules:
1. CPU Scheduling: FCFS, SJF, Round Robin, Priority
2. Memory Management: First Fit, Best Fit, Worst Fit
3. Deadlock Management: Banker's Algorithm
4. Disk Scheduling: FCFS, SSTF, SCAN, C-SCAN
5. Performance Report

Run:
python main.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import datetime


# ============================================================
# 1. CPU SCHEDULING ALGORITHMS
# ============================================================

def validate_processes(processes):
    if not processes:
        raise ValueError("Process list cannot be empty.")

    ids = [p["pid"] for p in processes]
    if len(ids) != len(set(ids)):
        raise ValueError("Process IDs must be unique.")

    for p in processes:
        if p["arrival"] < 0:
            raise ValueError("Arrival time cannot be negative.")
        if p["burst"] <= 0:
            raise ValueError("Burst time must be positive.")
        if p["priority"] < 0:
            raise ValueError("Priority cannot be negative.")


def cpu_scheduling(processes, algorithm, quantum=2):
    validate_processes(processes)

    jobs = [dict(p) for p in processes]
    completion = {}
    gantt = []
    current = 0

    if algorithm == "FCFS":
        jobs.sort(key=lambda p: (p["arrival"], p["pid"]))

        for p in jobs:
            if current < p["arrival"]:
                gantt.append(("Idle", current, p["arrival"]))
                current = p["arrival"]

            start = current
            current += p["burst"]
            completion[p["pid"]] = current
            gantt.append((p["pid"], start, current))

    elif algorithm in ("SJF", "Priority"):
        pending = jobs.copy()

        while pending:
            ready = [p for p in pending if p["arrival"] <= current]

            if not ready:
                next_time = min(p["arrival"] for p in pending)
                gantt.append(("Idle", current, next_time))
                current = next_time
                continue

            if algorithm == "SJF":
                chosen = min(
                    ready,
                    key=lambda p: (p["burst"], p["arrival"], p["pid"])
                )
            else:
                chosen = min(
                    ready,
                    key=lambda p: (p["priority"], p["arrival"], p["pid"])
                )

            start = current
            current += chosen["burst"]
            completion[chosen["pid"]] = current
            gantt.append((chosen["pid"], start, current))
            pending.remove(chosen)

    elif algorithm == "Round Robin":
        if quantum <= 0:
            raise ValueError("Time quantum must be positive.")

        jobs.sort(key=lambda p: (p["arrival"], p["pid"]))
        remaining = {p["pid"]: p["burst"] for p in jobs}
        queue = []
        index = 0
        current = 0

        while index < len(jobs) or queue:
            if not queue and index < len(jobs):
                if current < jobs[index]["arrival"]:
                    gantt.append(("Idle", current, jobs[index]["arrival"]))
                    current = jobs[index]["arrival"]

            while index < len(jobs) and jobs[index]["arrival"] <= current:
                queue.append(jobs[index])
                index += 1

            if not queue:
                continue

            p = queue.pop(0)
            pid = p["pid"]
            duration = min(quantum, remaining[pid])

            start = current
            current += duration
            remaining[pid] -= duration

            gantt.append((pid, start, current))

            while index < len(jobs) and jobs[index]["arrival"] <= current:
                queue.append(jobs[index])
                index += 1

            if remaining[pid] > 0:
                queue.append(p)
            else:
                completion[pid] = current

    else:
        raise ValueError("Unknown CPU scheduling algorithm.")

    results = []

    for p in jobs:
        ct = completion[p["pid"]]
        tat = ct - p["arrival"]
        wt = tat - p["burst"]

        results.append({
            "PID": p["pid"],
            "Arrival": p["arrival"],
            "Burst": p["burst"],
            "Priority": p["priority"],
            "Completion": ct,
            "Turnaround": tat,
            "Waiting": wt
        })

    avg_wt = sum(x["Waiting"] for x in results) / len(results)
    avg_tat = sum(x["Turnaround"] for x in results) / len(results)

    return results, gantt, avg_wt, avg_tat


# ============================================================
# 2. MEMORY MANAGEMENT ALGORITHMS
# ============================================================

def memory_allocation(processes, blocks, method):
    if not processes or not blocks:
        raise ValueError("Enter memory blocks and process sizes.")

    if any(x <= 0 for x in processes + blocks):
        raise ValueError("Memory sizes must be positive.")

    free_blocks = blocks.copy()
    results = []

    for i, size in enumerate(processes):
        candidates = [
            j for j, available in enumerate(free_blocks)
            if available >= size
        ]

        if not candidates:
            results.append({
                "Process": f"P{i+1}",
                "Size": size,
                "Block": "Not Allocated",
                "Remaining": "-"
            })
            continue

        if method == "First Fit":
            chosen = candidates[0]
        elif method == "Best Fit":
            chosen = min(candidates, key=lambda j: free_blocks[j])
        elif method == "Worst Fit":
            chosen = max(candidates, key=lambda j: free_blocks[j])
        else:
            raise ValueError("Invalid memory allocation method.")

        free_blocks[chosen] -= size

        results.append({
            "Process": f"P{i+1}",
            "Size": size,
            "Block": f"B{chosen+1}",
            "Remaining": free_blocks[chosen]
        })

    return results


# ============================================================
# 3. DEADLOCK MANAGEMENT - BANKER'S ALGORITHM
# ============================================================

def bankers_algorithm(available, maximum, allocation):
    if not available or not maximum:
        raise ValueError("Input cannot be empty.")

    if len(maximum) != len(allocation):
        raise ValueError("Maximum and Allocation rows must match.")

    resource_count = len(available)
    process_count = len(maximum)

    if any(len(row) != resource_count for row in maximum + allocation):
        raise ValueError("All rows must have the same number of resources.")

    if any(x < 0 for x in available):
        raise ValueError("Available resources cannot be negative.")

    need = []

    for i in range(process_count):
        row = []

        for j in range(resource_count):
            if maximum[i][j] < allocation[i][j]:
                raise ValueError("Allocation cannot exceed Maximum.")

            if maximum[i][j] < 0 or allocation[i][j] < 0:
                raise ValueError("Resource values cannot be negative.")

            row.append(maximum[i][j] - allocation[i][j])

        need.append(row)

    work = available.copy()
    finish = [False] * process_count
    sequence = []

    while True:
        found = False

        for i in range(process_count):
            if not finish[i]:
                if all(need[i][j] <= work[j] for j in range(resource_count)):
                    for j in range(resource_count):
                        work[j] += allocation[i][j]

                    sequence.append(f"P{i}")
                    finish[i] = True
                    found = True

        if not found:
            break

    return all(finish), sequence, need


# ============================================================
# 4. DISK SCHEDULING ALGORITHMS
# ============================================================

def disk_movement(order, head):
    movement = 0
    current = head

    for track in order:
        movement += abs(track - current)
        current = track

    return movement


def validate_disk(requests, head, disk_size):
    if not requests:
        raise ValueError("Enter at least one disk request.")

    if disk_size <= 0:
        raise ValueError("Disk size must be positive.")

    if not 0 <= head < disk_size:
        raise ValueError("Initial head is outside disk range.")

    if any(r < 0 or r >= disk_size for r in requests):
        raise ValueError("A disk request is outside disk range.")


def disk_scheduling(requests, head, disk_size, direction="right"):
    validate_disk(requests, head, disk_size)

    lower = sorted(r for r in requests if r < head)
    upper = sorted(r for r in requests if r >= head)

    results = {}

    # FCFS
    order = requests.copy()
    results["FCFS"] = {
        "order": order,
        "movement": disk_movement(order, head)
    }

    # SSTF
    pending = requests.copy()
    current = head
    order = []

    while pending:
        chosen = min(pending, key=lambda x: abs(x - current))
        order.append(chosen)
        pending.remove(chosen)
        current = chosen

    results["SSTF"] = {
        "order": order,
        "movement": disk_movement(order, head)
    }

    # SCAN
    if direction == "right":
        order = upper.copy()
        if head != disk_size - 1:
            order.append(disk_size - 1)
        order.extend(lower[::-1])
    else:
        order = lower[::-1]
        if head != 0:
            order.append(0)
        order.extend(upper)

    results["SCAN"] = {
        "order": order,
        "movement": disk_movement(order, head)
    }

    # C-SCAN
    if direction == "right":
        order = upper.copy()
        if head != disk_size - 1:
            order.append(disk_size - 1)
        if lower:
            order.append(0)
            order.extend(lower)
    else:
        order = lower[::-1]
        if head != 0:
            order.append(0)
        if upper:
            order.append(disk_size - 1)
            order.extend(upper[::-1])

    results["C-SCAN"] = {
        "order": order,
        "movement": disk_movement(order, head)
    }

    return results


# ============================================================
# 5. PERFORMANCE REPORT
# ============================================================

def generate_report(cpu_text, memory_text, deadlock_text, disk_text):
    folder = Path("reports")
    folder.mkdir(parents=True, exist_ok=True)

    path = folder / "performance_report.txt"

    content = f"""
============================================================
             OS RESOURCE MANAGEMENT SIMULATOR
                    PERFORMANCE REPORT
============================================================

Generated On: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}

---------------- CPU SCHEDULING ----------------

{cpu_text}

---------------- MEMORY MANAGEMENT ----------------

{memory_text}

---------------- DEADLOCK MANAGEMENT ----------------

{deadlock_text}

---------------- DISK SCHEDULING ----------------

{disk_text}

============================================================
                       END OF REPORT
============================================================
"""

    path.write_text(content, encoding="utf-8")
    return str(path)


# ============================================================
# 6. MAIN GUI APPLICATION
# ============================================================

class OSResourceSimulator:

    def __init__(self, root):
        self.root = root
        self.root.title("OS Resource Management Simulator")
        self.root.geometry("1150x750")
        self.root.minsize(950, 650)
        self.root.configure(bg="#F1F5F9")

        self.last_cpu = ""
        self.last_memory = ""
        self.last_deadlock = ""
        self.last_disk = ""

        self.create_dashboard()

    # ---------------- DASHBOARD ----------------

    def create_dashboard(self):
        self.sidebar = tk.Frame(
            self.root, bg="#172554", width=235
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="OS SIMULATOR",
            font=("Arial", 20, "bold"),
            bg="#172554",
            fg="white"
        ).pack(pady=(30, 5))

        tk.Label(
            self.sidebar,
            text="Resource Management",
            font=("Arial", 10),
            bg="#172554",
            fg="#BFDBFE"
        ).pack(pady=(0, 30))

        menu = [
            ("Dashboard", self.show_dashboard),
            ("CPU Scheduling", self.show_cpu),
            ("Memory Management", self.show_memory),
            ("Deadlock Management", self.show_deadlock),
            ("Disk Scheduling", self.show_disk),
            ("Performance Report", self.show_report)
        ]

        for title, command in menu:
            tk.Button(
                self.sidebar,
                text=title,
                command=command,
                font=("Arial", 11),
                bg="#1E3A8A",
                fg="white",
                activebackground="#3B82F6",
                relief="flat",
                anchor="w",
                padx=18,
                pady=13,
                cursor="hand2"
            ).pack(fill="x", padx=10, pady=4)

        self.content = tk.Frame(self.root, bg="#F1F5F9")
        self.content.pack(side="right", fill="both", expand=True)

        self.show_dashboard()

    # ---------------- COMMON GUI FUNCTIONS ----------------

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def heading(self, title, subtitle):
        tk.Label(
            self.content,
            text=title,
            font=("Arial", 25, "bold"),
            bg="#F1F5F9",
            fg="#172554"
        ).pack(anchor="w", padx=30, pady=(25, 5))

        tk.Label(
            self.content,
            text=subtitle,
            font=("Arial", 11),
            bg="#F1F5F9",
            fg="#64748B"
        ).pack(anchor="w", padx=30, pady=(0, 15))

    def make_output(self):
        box = tk.Text(
            self.content,
            font=("Consolas", 10),
            bg="white",
            fg="#172554",
            wrap="word"
        )
        box.pack(fill="both", expand=True, padx=30, pady=10)
        return box

    def make_button(self, title, command):
        tk.Button(
            self.content,
            text=title,
            command=command,
            bg="#2563EB",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=12,
            cursor="hand2"
        ).pack(pady=12)

    # ========================================================
    # DASHBOARD PAGE
    # ========================================================

    def show_dashboard(self):
        self.clear_content()
        self.heading(
            "Dashboard",
            "Operating System Resource Management Overview"
        )

        cards = [
            ("CPU SCHEDULING", "4 Algorithms"),
            ("MEMORY MANAGEMENT", "3 Algorithms"),
            ("DEADLOCK MANAGEMENT", "Banker's Algorithm"),
            ("DISK SCHEDULING", "4 Algorithms")
        ]

        frame = tk.Frame(self.content, bg="#F1F5F9")
        frame.pack(fill="x", padx=20, pady=10)

        for i, (title, value) in enumerate(cards):
            card = tk.Frame(
                frame,
                bg="white",
                padx=20,
                pady=25,
                highlightbackground="#CBD5E1",
                highlightthickness=1
            )
            card.grid(
                row=i // 2,
                column=i % 2,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            tk.Label(
                card,
                text=title,
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#475569"
            ).pack(anchor="w")

            tk.Label(
                card,
                text=value,
                font=("Arial", 19, "bold"),
                bg="white",
                fg="#2563EB"
            ).pack(anchor="w", pady=10)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        tk.Label(
            self.content,
            text="Welcome to OS Resource Management Simulator",
            font=("Arial", 16, "bold"),
            bg="#F1F5F9",
            fg="#172554"
        ).pack(anchor="w", padx=30, pady=25)

        tk.Label(
            self.content,
            text="Explore CPU scheduling, memory allocation, deadlock "
                 "management, disk scheduling and performance reports.",
            font=("Arial", 11),
            bg="#F1F5F9",
            fg="#475569",
            wraplength=750,
            justify="left"
        ).pack(anchor="w", padx=30)

    # ========================================================
    # CPU SCHEDULING PAGE
    # ========================================================

    def show_cpu(self):
        self.clear_content()
        self.heading(
            "CPU Scheduling",
            "FCFS, SJF, Round Robin and Priority Algorithms"
        )

        frame = tk.Frame(self.content, bg="#F1F5F9")
        frame.pack(fill="x", padx=30)

        tk.Label(
            frame,
            text="Round Robin Time Quantum:",
            bg="#F1F5F9",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=0, padx=5, pady=10)

        self.quantum_entry = tk.Entry(frame, width=10)
        self.quantum_entry.insert(0, "2")
        self.quantum_entry.grid(row=0, column=1)

        self.cpu_output = self.make_output()
        self.make_button("Run CPU Scheduling", self.run_cpu)

    def run_cpu(self):
        try:
            quantum = int(self.quantum_entry.get())

            processes = [
                {"pid": "P1", "arrival": 0, "burst": 5, "priority": 2},
                {"pid": "P2", "arrival": 1, "burst": 3, "priority": 1},
                {"pid": "P3", "arrival": 2, "burst": 2, "priority": 3}
            ]

            text = ""

            for name in ["FCFS", "SJF", "Round Robin", "Priority"]:
                results, gantt, avg_wt, avg_tat = cpu_scheduling(
                    processes, name, quantum
                )

                text += f"\n{name}\n{'-' * 55}\n"

                for row in results:
                    text += str(row) + "\n"

                text += f"Gantt Chart: {gantt}\n"
                text += f"Average Waiting Time: {avg_wt:.2f}\n"
                text += f"Average Turnaround Time: {avg_tat:.2f}\n"

            self.last_cpu = text
            self.cpu_output.delete("1.0", tk.END)
            self.cpu_output.insert(tk.END, text)

        except Exception as error:
            messagebox.showerror("CPU Scheduling Error", str(error))

    # ========================================================
    # MEMORY MANAGEMENT PAGE
    # ========================================================

    def show_memory(self):
        self.clear_content()
        self.heading(
            "Memory Management",
            "First Fit, Best Fit and Worst Fit Allocation"
        )

        frame = tk.Frame(self.content, bg="#F1F5F9")
        frame.pack(fill="x", padx=30)

        tk.Label(
            frame, text="Memory Blocks:", bg="#F1F5F9"
        ).grid(row=0, column=0, sticky="w", pady=8)

        self.blocks_entry = tk.Entry(frame, width=45)
        self.blocks_entry.insert(0, "100,500,200,300,600")
        self.blocks_entry.grid(row=0, column=1, padx=10)

        tk.Label(
            frame, text="Process Sizes:", bg="#F1F5F9"
        ).grid(row=1, column=0, sticky="w", pady=8)

        self.sizes_entry = tk.Entry(frame, width=45)
        self.sizes_entry.insert(0, "212,417,112,426")
        self.sizes_entry.grid(row=1, column=1, padx=10)

        self.memory_output = self.make_output()
        self.make_button("Run Memory Algorithms", self.run_memory)

    def run_memory(self):
        try:
            blocks = [
                int(x.strip())
                for x in self.blocks_entry.get().split(",")
            ]

            processes = [
                int(x.strip())
                for x in self.sizes_entry.get().split(",")
            ]

            text = ""

            for method in ["First Fit", "Best Fit", "Worst Fit"]:
                results = memory_allocation(processes, blocks, method)

                text += f"\n{method.upper()}\n{'-' * 55}\n"

                for row in results:
                    text += str(row) + "\n"

            self.last_memory = text
            self.memory_output.delete("1.0", tk.END)
            self.memory_output.insert(tk.END, text)

        except Exception as error:
            messagebox.showerror("Memory Error", str(error))

    # ========================================================
    # DEADLOCK MANAGEMENT PAGE
    # ========================================================

    def show_deadlock(self):
        self.clear_content()
        self.heading(
            "Deadlock Management",
            "Banker's Algorithm - Safe State Detection"
        )

        self.deadlock_output = self.make_output()
        self.make_button(
            "Run Banker's Algorithm",
            self.run_deadlock
        )

    def run_deadlock(self):
        available = [3, 3, 2]

        maximum = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3]
        ]

        allocation = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2]
        ]

        try:
            safe, sequence, need = bankers_algorithm(
                available, maximum, allocation
            )

            text = "BANKER'S ALGORITHM\n"
            text += "=" * 50 + "\n\n"
            text += "NEED MATRIX\n"

            for i, row in enumerate(need):
                text += f"P{i}: {row}\n"

            text += f"\nAvailable Resources: {available}\n"

            if safe:
                text += "\nSYSTEM STATUS: SAFE STATE\n"
                text += "Safe Sequence: " + " -> ".join(sequence) + "\n"
                text += "No deadlock detected.\n"
            else:
                text += "\nSYSTEM STATUS: UNSAFE STATE\n"
                text += "No safe sequence exists.\n"

            self.last_deadlock = text
            self.deadlock_output.delete("1.0", tk.END)
            self.deadlock_output.insert(tk.END, text)

        except Exception as error:
            messagebox.showerror("Deadlock Error", str(error))

    # ========================================================
    # DISK SCHEDULING PAGE
    # ========================================================

    def show_disk(self):
        self.clear_content()
        self.heading(
            "Disk Scheduling",
            "FCFS, SSTF, SCAN and C-SCAN Algorithms"
        )

        frame = tk.Frame(self.content, bg="#F1F5F9")
        frame.pack(fill="x", padx=30)

        fields = [
            ("Disk Requests:", "98,183,37,122,14,124,65,67"),
            ("Initial Head:", "53"),
            ("Disk Size:", "200")
        ]

        self.disk_entries = []

        for i, (label, default) in enumerate(fields):
            tk.Label(
                frame, text=label, bg="#F1F5F9"
            ).grid(row=i, column=0, sticky="w", pady=8)

            entry = tk.Entry(frame, width=45)
            entry.insert(0, default)
            entry.grid(row=i, column=1, padx=10)
            self.disk_entries.append(entry)

        tk.Label(
            frame, text="SCAN Direction:", bg="#F1F5F9"
        ).grid(row=3, column=0, sticky="w", pady=8)

        self.direction = tk.StringVar(value="right")

        ttk.Combobox(
            frame,
            textvariable=self.direction,
            values=["right", "left"],
            state="readonly",
            width=12
        ).grid(row=3, column=1, sticky="w")

        self.disk_output = self.make_output()
        self.make_button("Run Disk Scheduling", self.run_disk)

    def run_disk(self):
        try:
            requests = [
                int(x.strip())
                for x in self.disk_entries[0].get().split(",")
            ]

            head = int(self.disk_entries[1].get())
            disk_size = int(self.disk_entries[2].get())

            results = disk_scheduling(
                requests, head, disk_size, self.direction.get()
            )

            text = "DISK SCHEDULING COMPARISON\n"
            text += "=" * 55 + "\n"

            for name, result in results.items():
                text += f"\n{name}\n"
                text += f"Service Order: {result['order']}\n"
                text += f"Total Head Movement: {result['movement']}\n"

            self.last_disk = text
            self.disk_output.delete("1.0", tk.END)
            self.disk_output.insert(tk.END, text)

        except Exception as error:
            messagebox.showerror("Disk Scheduling Error", str(error))

    # ========================================================
    # PERFORMANCE REPORT PAGE
    # ========================================================

    def show_report(self):
        self.clear_content()
        self.heading(
            "Performance Report",
            "Generate Complete OS Algorithm Comparison Report"
        )

        self.report_output = self.make_output()
        self.make_button(
            "Generate Performance Report",
            self.run_report
        )

    def run_report(self):
        try:
            processes = [
                {"pid": "P1", "arrival": 0, "burst": 5, "priority": 2},
                {"pid": "P2", "arrival": 1, "burst": 3, "priority": 1},
                {"pid": "P3", "arrival": 2, "burst": 2, "priority": 3}
            ]

            # Generate CPU data if not already run
            if not self.last_cpu:
                for name in ["FCFS", "SJF", "Round Robin", "Priority"]:
                    results, gantt, avg_wt, avg_tat = cpu_scheduling(
                        processes, name, 2
                    )
                    self.last_cpu += (
                        f"\n{name}\n{results}\n"
                        f"Gantt Chart: {gantt}\n"
                        f"Average WT: {avg_wt:.2f}\n"
                        f"Average TAT: {avg_tat:.2f}\n"
                    )

            # Generate memory data if not already run
            if not self.last_memory:
                blocks = [100, 500, 200, 300, 600]
                sizes = [212, 417, 112, 426]

                for method in ["First Fit", "Best Fit", "Worst Fit"]:
                    self.last_memory += (
                        f"\n{method}\n"
                        f"{memory_allocation(sizes, blocks, method)}\n"
                    )

            # Generate deadlock data if not already run
            if not self.last_deadlock:
                safe, sequence, need = bankers_algorithm(
                    [3, 3, 2],
                    [
                        [7, 5, 3], [3, 2, 2], [9, 0, 2],
                        [2, 2, 2], [4, 3, 3]
                    ],
                    [
                        [0, 1, 0], [2, 0, 0], [3, 0, 2],
                        [2, 1, 1], [0, 0, 2]
                    ]
                )

                self.last_deadlock = (
                    f"Status: {'SAFE' if safe else 'UNSAFE'}\n"
                    f"Safe Sequence: {sequence}\n"
                    f"Need Matrix: {need}\n"
                )

            # Generate disk data if not already run
            if not self.last_disk:
                disk_results = disk_scheduling(
                    [98, 183, 37, 122, 14, 124, 65, 67],
                    53,
                    200
                )

                for name, result in disk_results.items():
                    self.last_disk += (
                        f"\n{name}: {result['movement']} tracks\n"
                    )

            path = generate_report(
                self.last_cpu,
                self.last_memory,
                self.last_deadlock,
                self.last_disk
            )

            display_text = (
                "REPORT GENERATED SUCCESSFULLY!\n\n"
                f"Saved at: {path}\n\n"
                "CPU SCHEDULING\n"
                f"{self.last_cpu}\n"
                "MEMORY MANAGEMENT\n"
                f"{self.last_memory}\n"
                "DEADLOCK MANAGEMENT\n"
                f"{self.last_deadlock}\n"
                "DISK SCHEDULING\n"
                f"{self.last_disk}"
            )

            self.report_output.delete("1.0", tk.END)
            self.report_output.insert(tk.END, display_text)

            messagebox.showinfo(
                "Report Generated",
                f"Performance report saved successfully:\n{path}"
            )

        except Exception as error:
            messagebox.showerror("Report Error", str(error))


# ============================================================
# APPLICATION START
# ============================================================

def main():
    root = tk.Tk()
    app = OSResourceSimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
