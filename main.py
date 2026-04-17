from scanner.detect_project import detect_project
from engine.command_builder import get_command
from runner.executor import run_parallel

def main():
    print("Scanning project...\n")

    services=detect_project()

    if not services:
        print("No recognizable services found.")
        return 
    selected_services=[]

    for i,service in enumerate(services):
        print(f"\nService {i+1}:")
        print(f"Path: {service['path']}")
        print(f"Language: {service['language']}")

        command=get_command(service)

        if command:
            print(f"Command: {command}")
            choice =input("Run this service? (y/n): ")
            if choice.lower()=="y":
                selected_services.append(service)
        else:
            print("No command Available.")
    if selected_services:
        print("\nStarting selected services...\n")
        run_parallel(selected_services)
    else:
        print("No services selected.")

if __name__ =="__main__":
    main()