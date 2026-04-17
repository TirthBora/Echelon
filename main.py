from scanner.detect_project import detect_project, classify_service
from engine.command_builder import get_command
from runner.executor import run_parallel, run_command


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
        print(f"{s['path']} → {s['command']}")

    if len(ordered_services) == 1:
        run_command(ordered_services[0]["command"], ordered_services[0]["path"])
    else:
        run_parallel(ordered_services)


if __name__ == "__main__":
    main()
