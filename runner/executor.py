import subprocess
from ai.suggestion_engine import suggest_fix
from ai.auto_fix import auto_fix
from ai.ai_engine import ask_ai
from ai.ai_helper import build_error_prompt


def start_process(command, path="."):
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
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
            processes.append((process, service))

    try:
        for p, service in processes:
            stdout, stderr = p.communicate()

            if stdout:
                print(stdout)

            if stderr:
                print(f"\nError in {service['path']}:\n{stderr}")

                fixed = auto_fix(stderr, service["path"])

                if fixed:
                    print("\nRetrying service...\n")
                    new_process = start_process(service["command"], service["path"])

                    if new_process:
                        new_process.wait()
                else:
                    suggest_fix(stderr)

                    print("\nTrying AI explanation...\n")

                    prompt = build_error_prompt(stderr, service)
                    ai_response = ask_ai(prompt)

                    print("AI Suggestion:\n")
                    print(ai_response)

    except KeyboardInterrupt:
        print("\nStopping all services...")

        for p, _ in processes:
            p.terminate()
