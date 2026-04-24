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
    filtered_services = [s for s in ordered_services if not s.get("is_root")]

    if not filtered_services:
        print("No runnable services found.")
        return

    print("Detected services:\n")

    for i, s in enumerate(filtered_services, 1):
        print(f"{i}. {s['path']}")
        print(f"   Type: {classify_service(s)}")
        print(f"   Command: {s['command']}\n")

    print("Options:")
    print(" - Enter number (1,2,...) to run specific service")
    print(" - Enter 'all' to run all services")
    print(" - Enter 'backend' or 'frontend'\n")

    raw_input = input("echelon> ").strip().lower()

    if raw_input.startswith("run"):
        choice = raw_input.replace("run", "").strip()
    else:
        choice = raw_input

    if not choice:
        print("Please enter a command (e.g., run 1, run all)")
        return

    selected_services = []

    if choice == "all":
        selected_services = filtered_services

    elif choice == "backend":
        selected_services = [
            s for s in filtered_services if classify_service(s) == "backend"
        ]

    elif choice == "frontend":
        selected_services = [
            s for s in filtered_services if classify_service(s) == "frontend"
        ]

    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(filtered_services):
                selected_services = [filtered_services[idx]]
            else:
                print("Invalid selection")
                return
        except:
            print("Invalid input")
            return

    if not selected_services:
        print("No services selected.")
        return

    print("\nRunning selected services:\n")

    for s in selected_services:
        print(f"{s['path']} -> {s['command']}")

    run_parallel(selected_services)


if __name__ == "__main__":
    main()