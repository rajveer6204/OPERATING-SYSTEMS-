
import os
import subprocess
import sys

def child_process():
    print("\n--- CHILD PROCESS ---")
    print("Child Process ID:", os.getpid())
    print("Parent Process ID:", os.getppid())

    # Execute a harmless Linux command
    try:
        result = subprocess.run(
            ["echo", "Hello from the child process!"],
            capture_output=True,
            text=True,
            check=True
        )
        print("Linux command output:", result.stdout.strip())
    except (OSError, subprocess.CalledProcessError) as e:
        print("Command execution error:", e)

def main():
    print("=== SYSTEM CALLS AND PROCESS CREATION ===")
    print("Main Process ID:", os.getpid())
    print("Parent Process ID:", os.getppid())

    # Create a child process using an approved Python method
    process = subprocess.Popen(
        [sys.executable, __file__, "--child"]
    )

    # Create, write, read, and close a controlled test file
    file_path = "system_test.txt"

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("System calls assignment test file.\n")
            file.write("File write and read operations successful.\n")
        print("\nFile created and written successfully.")

        with open(file_path, "r", encoding="utf-8") as file:
            print("File contents:")
            print(file.read(), end="")
        print("File closed successfully.")

    except OSError as e:
        print("File operation error:", e)

    # Inspect an approved Linux device interface
    try:
        with open("/dev/null", "w", encoding="utf-8") as device:
            device.write("Harmless test data")
        print("\n/dev/null inspected successfully.")
    except OSError as e:
        print("\nDevice interface unavailable:", e)

    # Handle an invalid file path
    try:
        with open("missing_folder/missing.txt", "r") as file:
            file.read()
    except OSError as e:
        print("\nExpected error handled clearly:", e)

    # Wait for the child process to complete
    return_code = process.wait()
    print("\nChild process completed with exit code:", return_code)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--child":
        child_process()
    else:
        main()
