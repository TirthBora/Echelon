import subprocess


def start_process(command, path="."):
    try:
        process = subprocess.Popen(command, shell=True, cwd=path)
        return process
    except Exception as e:
        print(f"Error starting process: {e}")
        return None


def run_parallel(services):
    processes = []

    for service in services:
        command = service.get("command")

        if not command:
            continue

        print(f"\nStarting {service['language']} service in {service['path']}")
        print(f"Command: {command}\n")

        process = start_process(command, service["path"])

        if process:
            processes.append(process)
    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        print("\nStopping all services...")
        for p in processes:
            p.terminate()
