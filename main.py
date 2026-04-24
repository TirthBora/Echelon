from scanner.detect_project import detect_project, classify_service
from engine.command_builder import get_command
from runner.executor import run_parallel


def main():
    print("Scanning project...\n")

    services = detect_project()

    if not services:
        print("No recognizable services found.")
        return

    backend_services = []
    frontend_services = []

    for service in services:
        service_type = classify_service(service)
        command = get_command(service)

        if not command:
            continue

        service["command"] = command

        if service_type == "backend":
            backend_services.append(service)
        elif service_type == "frontend":
            frontend_services.append(service)

    ordered_services = backend_services + frontend_services

    if not ordered_services:
        print("No runnable services found.")
        return

    print("Auto-running detected services...\n")

    for s in ordered_services:
        if s.get("is_root"):
            print(f"Skipping root project: {s['path']}")
            continue

        print(f"{s['path']} -> {s['command']}")

    filtered_services = [s for s in ordered_services if not s.get("is_root")]

    run_parallel(filtered_services)


if __name__ == "__main__":
    main()