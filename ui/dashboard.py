
"""
OS Resource Management Simulator
Complete Main GUI Dashboard
"""

import tkinter as tk
from tkinter import messagebox

from modules.memory import allocate_memory

from modules.scheduling import (
    fcfs_scheduling,
    sjf_scheduling,
    round_robin_scheduling,
    priority_scheduling
)

from modules.deadlock import bankers_algorithm
from modules.storage import compare_disk_algorithms
from modules.reporting import generate_performance_report


class OSResourceSimulator:

    def __init__(self, root):
        self.root = root
        self.root.title("OS Resource Management Simulator")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        self.root.configure(bg="#F1F5F9")

        self.create_dashboard()

    # ---------------- MAIN DASHBOARD ----------------

    def create_dashboard(self):

        self.sidebar = tk.Frame(
            self.root,
            bg="#172554",
            width=230
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="OS SIMULATOR",
            font=("Arial", 19, "bold"),
            bg="#172554",
            fg="white"
        ).pack(pady=(30, 5))

        tk.Label(
            self.sidebar,
            text="Resource Management",
            font=("Arial", 10),
            bg="#172554",
            fg="#BFDBFE"
        ).pack(pady=(0, 35))

        menu_items = [
            ("Dashboard", self.show_dashboard),
            ("CPU Scheduling", self.show_scheduling),
            ("Memory Management", self.show_memory),
            ("Deadlock Management", self.show_deadlock),
            ("Disk Scheduling", self.show_storage),
            ("Performance Report", self.show_report)
        ]

        for title, command in menu_items:
            tk.Button(
                self.sidebar,
                text=title,
                command=command,
                font=("Arial", 11),
                bg="#1E3A8A",
                fg="white",
                activebackground="#3B82F6",
                activeforeground="white",
                relief="flat",
                anchor="w",
                padx=20,
                pady=13,
                cursor="hand2"
            ).pack(fill="x", padx=12, pady=4)

        self.content = tk.Frame(
            self.root,
            bg="#F1F5F9"
        )
        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.show_dashboard()

    # ---------------- COMMON FUNCTIONS ----------------

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def create_heading(self, title, subtitle):

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
        ).pack(anchor="w", padx=30, pady=(0, 20))

    # ---------------- DASHBOARD PAGE ----------------

    def show_dashboard(self):

        self.clear_content()

        self.create_heading(
            "Dashboard",
            "Operating System Resource Management Overview"
        )

        cards = [
            ("CPU SCHEDULING", "4 Algorithms"),
            ("MEMORY MANAGEMENT", "3 Algorithms"),
            ("DEADLOCK MANAGEMENT", "Banker's Algorithm"),
            ("DISK SCHEDULING", "4 Algorithms")
        ]

        card_frame = tk.Frame(
            self.content,
            bg="#F1F5F9"
        )
        card_frame.pack(fill="x", padx=20, pady=10)

        for index, (title, value) in enumerate(cards):

            card = tk.Frame(
                card_frame,
                bg="white",
                padx=20,
                pady=25,
                highlightbackground="#CBD5E1",
                highlightthickness=1
            )

            card.grid(
                row=index // 2,
                column=index % 2,
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
            ).pack(anchor="w", pady=(12, 0))

        card_frame.columnconfigure(0, weight=1)
        card_frame.columnconfigure(1, weight=1)

        tk.Label(
            self.content,
            text="Welcome to OS Resource Management Simulator",
            font=("Arial", 15, "bold"),
            bg="#F1F5F9",
            fg="#172554"
        ).pack(anchor="w", padx=30, pady=25)

        tk.Label(
            self.content,
            text=(
                "Use the sidebar to explore CPU scheduling, memory "
                "allocation, deadlock management, disk scheduling "
                "and performance reports."
            ),
            font=("Arial", 11),
            bg="#F1F5F9",
            fg="#475569",
            wraplength=750,
            justify="left"
        ).pack(anchor="w", padx=30)

    # ---------------- CPU SCHEDULING ----------------

    def show_scheduling(self):

        self.clear_content()

        self.create_heading(
            "CPU Scheduling",
            "Compare FCFS, SJF, Round Robin and Priority algorithms"
        )

        self.output_box = tk.Text(
            self.content,
            height=20,
            font=("Consolas", 10),
            bg="white",
            fg="#172554",
            wrap="none"
        )

        self.output_box.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        tk.Button(
            self.content,
            text="Run Scheduling Algorithms",
            command=self.run_scheduling,
            bg="#2563EB",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=12
        ).pack(pady=15)

    def run_scheduling(self):

        processes = [
            {"pid": "P1", "arrival": 0, "burst": 5, "priority": 2},
            {"pid": "P2", "arrival": 1, "burst": 3, "priority": 1},
            {"pid": "P3", "arrival": 2, "burst": 2, "priority": 3}
        ]

        algorithms = [
            ("FCFS", fcfs_scheduling),
            ("SJF", sjf_scheduling),
            ("Round Robin", lambda p: round_robin_scheduling(p, 2)),
            ("Priority", priority_scheduling)
        ]

        self.output_box.delete("1.0", tk.END)

        try:
            for name, algorithm in algorithms:

                results, gantt_chart = algorithm(processes)

                self.output_box.insert(
                    tk.END,
                    f"\n{name}\n" + "-" * 55 + "\n"
                )

                for row in results:
                    self.output_box.insert(
                        tk.END,
                        f"{row}\n"
                    )

                self.output_box.insert(
                    tk.END,
                    f"Gantt Chart: {gantt_chart}\n"
                )

        except Exception as error:
            messagebox.showerror("Scheduling Error", str(error))

    # ---------------- MEMORY MANAGEMENT ----------------

    def show_memory(self):

        self.clear_content()

        self.create_heading(
            "Memory Management",
            "First Fit, Best Fit and Worst Fit Allocation"
        )

        input_frame = tk.Frame(
            self.content,
            bg="#F1F5F9"
        )
        input_frame.pack(fill="x", padx=30, pady=10)

        tk.Label(
            input_frame,
            text="Memory Blocks:",
            font=("Arial", 11, "bold"),
            bg="#F1F5F9"
        ).grid(row=0, column=0, sticky="w", pady=10)

        self.memory_blocks_entry = tk.Entry(
            input_frame,
            width=45,
            font=("Arial", 11)
        )
        self.memory_blocks_entry.insert(
            0, "100, 500, 200, 300, 600"
        )
        self.memory_blocks_entry.grid(
            row=0, column=1, padx=10
        )

        tk.Label(
            input_frame,
            text="Process Sizes:",
            font=("Arial", 11, "bold"),
            bg="#F1F5F9"
        ).grid(row=1, column=0, sticky="w", pady=10)

        self.process_sizes_entry = tk.Entry(
            input_frame,
            width=45,
            font=("Arial", 11)
        )
        self.process_sizes_entry.insert(
            0, "212, 417, 112, 426"
        )
        self.process_sizes_entry.grid(
            row=1, column=1, padx=10
        )

        tk.Button(
            input_frame,
            text="Run Memory Algorithms",
            command=self.run_memory,
            bg="#2563EB",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10
        ).grid(row=2, column=1, sticky="w", pady=15)

        self.memory_output = tk.Text(
            self.content,
            height=18,
            font=("Consolas", 10),
            bg="white",
            fg="#172554"
        )

        self.memory_output.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

    def run_memory(self):

        try:
            blocks = [
                int(x.strip())
                for x in self.memory_blocks_entry.get().split(",")
            ]

            processes = [
                int(x.strip())
                for x in self.process_sizes_entry.get().split(",")
            ]

            if not blocks or not processes:
                raise ValueError(
                    "Enter memory blocks and process sizes."
                )

            if any(x <= 0 for x in blocks + processes):
                raise ValueError(
                    "All sizes must be positive numbers."
                )

            self.memory_output.delete("1.0", tk.END)

            methods = ["First Fit", "Best Fit", "Worst Fit"]

            for method in methods:

                results = allocate_memory(
                    processes, blocks, method
                )

                self.memory_output.insert(
                    tk.END,
                    "\n" + "=" * 55 + "\n"
                )

                self.memory_output.insert(
                    tk.END,
                    method.upper() + " MEMORY ALLOCATION\n"
                )

                self.memory_output.insert(
                    tk.END,
                    "=" * 55 + "\n"
                )

                for result in results:
                    self.memory_output.insert(
                        tk.END,
                        str(result) + "\n"
                    )

            self.memory_output.insert(
                tk.END,
                "\nMemory allocation completed successfully."
            )

        except ValueError as error:
            messagebox.showerror("Input Error", str(error))

        except Exception as error:
            messagebox.showerror("Memory Error", str(error))

    # ---------------- DEADLOCK MANAGEMENT ----------------

    def show_deadlock(self):

        self.clear_content()

        self.create_heading(
            "Deadlock Management",
            "Banker's Algorithm - Safe State Detection"
        )

        self.deadlock_output = tk.Text(
            self.content,
            height=20,
            font=("Consolas", 11),
            bg="white",
            fg="#172554"
        )

        self.deadlock_output.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        tk.Button(
            self.content,
            text="Run Banker's Algorithm",
            command=self.run_deadlock,
            bg="#2563EB",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=12
        ).pack(pady=15)

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

            self.deadlock_output.delete("1.0", tk.END)

            self.deadlock_output.insert(
                tk.END,
                "BANKER'S ALGORITHM\n"
            )

            self.deadlock_output.insert(
                tk.END,
                "=" * 45 + "\n\n"
            )

            self.deadlock_output.insert(
                tk.END,
                "NEED MATRIX\n"
            )

            for i, row in enumerate(need):
                self.deadlock_output.insert(
                    tk.END,
                    f"P{i}: {row}\n"
                )

            self.deadlock_output.insert(
                tk.END,
                f"\nAvailable Resources: {available}\n"
            )

            if safe:
                self.deadlock_output.insert(
                    tk.END,
                    "\nSYSTEM STATUS: SAFE STATE\n"
                )

                self.deadlock_output.insert(
                    tk.END,
                    "Safe Sequence: " + " -> ".join(sequence) + "\n"
                )

                self.deadlock_output.insert(
                    tk.END,
                    "No deadlock detected.\n"
                )

            else:
                self.deadlock_output.insert(
                    tk.END,
                    "\nSYSTEM STATUS: UNSAFE STATE\n"
                )

                self.deadlock_output.insert(
                    tk.END,
                    "No safe sequence exists.\n"
                )

        except Exception as error:
            messagebox.showerror("Deadlock Error", str(error))

    # ---------------- DISK SCHEDULING ----------------

    def show_storage(self):

        self.clear_content()

        self.create_heading(
            "Disk Scheduling",
            "FCFS, SSTF, SCAN and C-SCAN Algorithms"
        )

        input_frame = tk.Frame(
            self.content,
            bg="#F1F5F9"
        )
        input_frame.pack(fill="x", padx=30, pady=10)

        fields = [
            ("Disk Requests:", "98, 183, 37, 122, 14, 124, 65, 67"),
            ("Initial Head:", "53"),
            ("Disk Size:", "200")
        ]

        self.disk_entries = []

        for row, (label, default) in enumerate(fields):

            tk.Label(
                input_frame,
                text=label,
                font=("Arial", 11, "bold"),
                bg="#F1F5F9"
            ).grid(row=row, column=0, sticky="w", pady=8)

            entry = tk.Entry(
                input_frame,
                width=45,
                font=("Arial", 11)
            )

            entry.insert(0, default)
            entry.grid(row=row, column=1, padx=10)

            self.disk_entries.append(entry)

        tk.Button(
            input_frame,
            text="Run Disk Scheduling",
            command=self.run_storage,
            bg="#2563EB",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10
        ).grid(row=3, column=1, sticky="w", pady=12)

        self.storage_output = tk.Text(
            self.content,
            height=18,
            font=("Consolas", 10),
            bg="white",
            fg="#172554"
        )

        self.storage_output.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

    def run_storage(self):

        try:
            requests = [
                int(x.strip())
                for x in self.disk_entries[0].get().split(",")
            ]

            head = int(self.disk_entries[1].get())
            disk_size = int(self.disk_entries[2].get())

            results = compare_disk_algorithms(
                requests,
                head,
                disk_size
            )

            self.storage_output.delete("1.0", tk.END)

            self.storage_output.insert(
                tk.END,
                "DISK SCHEDULING COMPARISON\n"
            )

            self.storage_output.insert(
                tk.END,
                "=" * 55 + "\n"
            )

            for name, result in results.items():

                self.storage_output.insert(
                    tk.END,
                    f"\n{name}\n"
                )

                self.storage_output.insert(
                    tk.END,
                    f"Service Order: {result['order']}\n"
                )

                self.storage_output.insert(
                    tk.END,
                    f"Total Head Movement: {result['movement']}\n"
                )

        except Exception as error:
            messagebox.showerror(
                "Disk Scheduling Error",
                str(error)
            )

    # ---------------- PERFORMANCE REPORT ----------------

    def show_report(self):

        self.clear_content()

        self.create_heading(
            "Performance Report",
            "Generate a comparison report of all OS algorithms"
        )

        tk.Label(
            self.content,
            text="Click below to generate the performance report.",
            font=("Arial", 12),
            bg="#F1F5F9"
        ).pack(pady=25)

        tk.Button(
            self.content,
            text="Generate Performance Report",
            command=self.run_report,
            bg="#2563EB",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=12
        ).pack(pady=10)

        self.report_output = tk.Text(
            self.content,
            height=18,
            font=("Consolas", 10),
            bg="white",
            fg="#172554"
        )

        self.report_output.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

    def run_report(self):

        try:
            processes = [
                {"pid": "P1", "arrival": 0, "burst": 5, "priority": 2},
                {"pid": "P2", "arrival": 1, "burst": 3, "priority": 1},
                {"pid": "P3", "arrival": 2, "burst": 2, "priority": 3}
            ]

            # CPU Scheduling Report
            cpu_text = ""

            algorithms = [
                ("FCFS", fcfs_scheduling),
                ("SJF", sjf_scheduling),
                ("Round Robin", lambda p: round_robin_scheduling(p, 2)),
                ("Priority", priority_scheduling)
            ]

            for name, algorithm in algorithms:

                results, gantt = algorithm(processes)

                cpu_text += f"\n{name}\n"

                for result in results:
                    cpu_text += str(result) + "\n"

                cpu_text += f"Gantt Chart: {gantt}\n"

            # Memory Management Report
            blocks = [100, 500, 200, 300, 600]
            sizes = [212, 417, 112, 426]

            memory_text = ""

            for method in ["First Fit", "Best Fit", "Worst Fit"]:

                memory_text += f"\n{method}\n"

                results = allocate_memory(
                    sizes, blocks, method
                )

                for result in results:
                    memory_text += str(result) + "\n"

            # Disk Scheduling Report
            disk_results = compare_disk_algorithms(
                [98, 183, 37, 122, 14, 124, 65, 67],
                53,
                200
            )

            # Generate Report File
            path = generate_performance_report(
                cpu_text,
                memory_text,
                disk_results
            )

            self.report_output.delete("1.0", tk.END)

            self.report_output.insert(
                tk.END,
                "REPORT GENERATED SUCCESSFULLY!\n\n"
            )

            self.report_output.insert(
                tk.END,
                f"Saved at: {path}\n\n"
            )

            self.report_output.insert(
                tk.END,
                "CPU SCHEDULING RESULTS\n"
            )

            self.report_output.insert(
                tk.END,
                cpu_text + "\n"
            )

            self.report_output.insert(
                tk.END,
                "MEMORY MANAGEMENT RESULTS\n"
            )

            self.report_output.insert(
                tk.END,
                memory_text + "\n"
            )

            self.report_output.insert(
                tk.END,
                "DISK SCHEDULING RESULTS\n"
            )

            for name, result in disk_results.items():

                self.report_output.insert(
                    tk.END,
                    f"\n{name}: {result['movement']} tracks"
                )

            messagebox.showinfo(
                "Report Generated",
                f"Performance report saved successfully:\n{path}"
            )

        except Exception as error:
            messagebox.showerror("Report Error", str(error))


# ---------------- APPLICATION START ----------------

def main():

    root = tk.Tk()
    app = OSResourceSimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
