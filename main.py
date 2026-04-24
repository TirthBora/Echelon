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

    non_root_services = [s for s in ordered_services if not s.get("is_root")]

    if non_root_services:
        for s in non_root_services:
            print(f"{s['path']} -> {s['command']}")
        run_parallel(non_root_services)
    else:
        safe_services = [
            s
            for s in ordered_services
            if not (s.get("is_root") and "main.py" in str(s.get("command")))
        ]

        if safe_services:
            for s in safe_services:
                print(f"{s['path']} -> {s['command']}")
            run_parallel(safe_services)
        else:
            print("No safe services to run.")


if __name__ == "__main__":
    main()
