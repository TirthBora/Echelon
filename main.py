from scanner.detect_project import detect_project
from engine.command_builder import get_command
from runner.executor import run_command

def main():
    print("Scanning project...\n")

    services=detect_project()

    if not services:
        print("No recognizable services found.")
        return 
    for i,service in enumerate(services):
        print(f"\nService {i+1}:")
        print(f"Path: {service['path']}")
        print(f"Language: {service['language']}")

        command=get_command(service)

        if command:
            print(f"Command: {command}")
            choice =input("Run this service? (y/n): ")
            if choice.lower()=="y":
                run_command(command,service["path"])
        else:
            print("No command Available.")

if __name__ =="__main__":
    main()