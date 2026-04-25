import subprocess
import webbrowser
import time
import re
import threading

from ai.suggestion_engine import suggest_fix
from ai.auto_fix import auto_fix, handle_port_conflict
from ai.ai_engine import ask_ai
from ai.ai_helper import build_error_prompt


def start_process(command, path="."):
    try:
        return subprocess.Popen(
            command,
            shell=True,
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
    except Exception as e:
        print(f"[Echelon] Failed to start process: {e}")
        return None


PORT_PATTERNS = [
    r"http://localhost:(\d+)",
    r"http://127\.0\.0\.1:(\d+)",
    r"localhost:(\d+)",
    r"port (\d+)",
    r"running on .*:(\d+)",
    r"listening on .*:(\d+)"
]


def extract_port(output):
    output = output.lower()
    for pattern in PORT_PATTERNS:
        match = re.search(pattern, output)
        if match:
            return int(match.group(1))
    return None


DEFAULT_PORTS = {
    "react": 3000,
    "vite": 5173,
    "nextjs": 3000,
    "vue": 5173,
    "angular": 4200,
    "fastapi": 8000,
    "flask": 5000,
    "django": 8000,
    "express": 3000,
    "nestjs": 3000,
    "static": 5500
}


def get_default_port(framework):
    return DEFAULT_PORTS.get(framework)


def open_browser(port):
    url = f"http://localhost:{port}"
    print(f"\n[Echelon] Opening: {url}\n")
    webbrowser.open(url)


def monitor_process(process, service):
    opened = False
    detected_port = None

    try:
        fallback = get_default_port(service.get("framework"))
        if fallback:
            open_browser(fallback)
            opened = True
            detected_port = fallback

        for line in iter(process.stdout.readline, ''):
            if not line:
                break

            print(line, end="")

            
            port = extract_port(line)

            if port and port != detected_port:
                print(f"\n[Echelon] Detected actual port {port}\n")
                open_browser(port)
                detected_port = port
                opened = True

        stderr = process.stderr.read()

        if stderr:
            handle_error(stderr, service)

    except Exception as e:
        print(f"[Echelon] Monitor error: {e}")


def handle_error(stderr, service):
    print(f"\n[Echelon] Error in {service['path']}:\n{stderr}")

    fixed = auto_fix(stderr, service["path"])

    if fixed == "port":
        service = handle_port_conflict(service)
        print("\n[Echelon] Retrying with new port...\n")
        restart_service(service)
        return

    if fixed:
        print("\n[Echelon] Retrying after fix...\n")
        restart_service(service)
        return

    suggest_fix(stderr)

    print("\n[Echelon] Asking AI...\n")

    prompt = build_error_prompt(stderr, service)
    ai_response = ask_ai(prompt)

    print("\n===== AI Suggestion =====\n")
    print(ai_response)
    print("\n=============\n")


def restart_service(service):
    new_process = start_process(service["command"], service["path"])
    if new_process:
        threading.Thread(
            target=monitor_process,
            args=(new_process, service),
            daemon=True
        ).start()


def run_parallel(services):
    processes = []

    for service in services:
        command = service.get("command")
        if not command:
            continue

        print(f"\n[Echelon] Starting {service['language']} in {service['path']}")
        print(f"Command: {command}\n")

        process = start_process(command, service["path"])

        if process:
            processes.append(process)

            threading.Thread(
                target=monitor_process,
                args=(process, service),
                daemon=True
            ).start()

    try:
        for p in processes:
            p.wait()

    except KeyboardInterrupt:
        print("\n[Echelon] Stopping all services...")

        for p in processes:
            p.terminate()


def run_command(command, path="."):
    process = start_process(command, path)

    if process:
        monitor_process(process, {"path": path, "framework": None})