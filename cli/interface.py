def show_services(services):
    print("\nDetected services:\n")

    for i, service in enumerate(services, 1):
        print(f"{i}. {service['path']}")
        print(f"   Language: {service['language']}")
        print(f"   Command: {service.get('command')}\n")


def get_user_choice(n):
    choice = input("Choose service (number/all): ")

    if choice.lower() == "all":
        return "all"

    try:
        idx = int(choice)
        if 1 <= idx <= n:
            return idx - 1
    except:
        pass

    print("Invalid choice")
    return None